import os
import time

import cv2

from enums.flux_reader_event_type import FluxReaderEventType
from gui import utils
from interfaces.event import Event
from libs.model_loader import ModelLoader
from objects.skeleton import Skeleton
from utils.yolov8_converter_utils import convert_image_box_outputs, convert_image_skeleton_outputs


class FluxReaderEvent(Event):
	def __init__(self, flux: int | str = 0, nbr_frame_to_skip: int = 2, looping: bool = True):
		super().__init__()
		self.flux = flux
		self.video = cv2.VideoCapture(self.flux)
		if isinstance(self.flux, int) and self.video.get(cv2.CAP_PROP_FPS) == 0:
			self.video.set(cv2.CAP_PROP_FPS, 30)
		self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
		self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 1920)
		self.cancelled = False
		self.refreshed = False
		self.looping = looping

		self.nbr_frame_to_skip = nbr_frame_to_skip

	def set_cancelled(self, cancelled: bool):
		self.cancelled = cancelled

	def refresh_holds(self):
		self.refreshed = False

	def process(self):
		parent_path = utils.get_parent_path(__file__, 3)
		models_path = os.path.join(parent_path, "resources", "models")
		holds_detector = ModelLoader(os.path.join(models_path, "holds_model_yolov8l.pt"))
		skeleton_detector = ModelLoader(os.path.join(models_path, "yolov8l-pose.pt"))
		skeletons: list[Skeleton] = []

		refresh_holds = False
		self.refreshed = False
		frame_skipper = 0
		while self.video.isOpened() and not self.cancelled:
			success, frame = self.video.read()
			if isinstance(self.flux, str):
				time.sleep(1 / self.video.get(cv2.CAP_PROP_FPS))
			if not success:
				if self.looping and isinstance(self.flux, str):
					self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
					continue
				else:
					break

			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

			self.notify(FluxReaderEventType.GET_FRAME_EVENT, frame)

			if (refresh_holds or not self.refreshed) and (
					super().has_listener(FluxReaderEventType.HOLDS_PROCESSED_EVENT) or super().has_listener(
				FluxReaderEventType.FRAME_PROCESSED_EVENT)):
				self.refreshed = True

				holds_predictions = holds_detector.predict(frame, classes=[0])
				floor_predictions = holds_detector.predict(frame, classes=[1])
				holds_boxes = convert_image_box_outputs(holds_predictions)
				self.notify(FluxReaderEventType.HOLDS_PROCESSED_EVENT, holds_boxes, frame)
				floor_boxes = convert_image_box_outputs(floor_predictions)
				self.notify(FluxReaderEventType.FLOOR_PROCESSED_EVENT, floor_boxes, frame)

			if frame_skipper == 0 and (
					super().has_listener(FluxReaderEventType.SKELETONS_PROCESSED_EVENT) or super().has_listener(
				FluxReaderEventType.FRAME_PROCESSED_EVENT)):
				skeleton_prediction = skeleton_detector.predict(frame, img_size=512)
				skeletons = convert_image_skeleton_outputs(skeleton_prediction)
				self.notify(FluxReaderEventType.SKELETONS_PROCESSED_EVENT, self.nbr_frame_to_skip, skeletons,
				            holds_boxes, frame)

			if super().has_listener(FluxReaderEventType.FRAME_PROCESSED_EVENT):
				self.notify(FluxReaderEventType.FRAME_PROCESSED_EVENT, frame, holds_boxes, floor_boxes, skeletons,
				            frame_skipper)
			frame_skipper = (frame_skipper + 1) % (self.nbr_frame_to_skip + 1)

		self.notify(FluxReaderEventType.END_OF_FILE_EVENT)
		self.video.release()
