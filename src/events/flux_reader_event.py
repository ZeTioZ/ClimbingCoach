import cv2, os
from interfaces.event import Event

from enums.flux_reader_event_type import FluxReaderEventType
from libs.model_loader import ModelLoader
from utils.yolov8_converter_utils import convert_image_box_outputs, convert_image_skeleton_outputs

MODELS_DIRECTORY = "./resources/models/"
VIDEOS_DIRECTORY = "./resources/videos/"


class FluxReaderEvent(Event):
    def __init__(self, flux: str = "0", width: int = 640, height: int = 480, nbr_frame_to_skip: int = 2):
        self.flux = flux
        self.video = cv2.VideoCapture(self.flux)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cancelled = False

        self.nbr_frame_to_skip = nbr_frame_to_skip
        self.holds_boxes = []
        self.floor_boxes = []
        self.skeletons = []


    def set_cancelled(self, cancelled: bool):
        self.cancelled = cancelled
        

    def process(self):
        holds_detector = ModelLoader(os.path.join(MODELS_DIRECTORY, "holds_model_yolov8l.pt"))
        skeleton_detector = ModelLoader(os.path.join(MODELS_DIRECTORY, "yolov8l-pose.pt"))

        video = cv2.VideoCapture(self.flux)
        video.set(cv2.CAP_PROP_FRAME_WIDTH, video.get(cv2.CAP_PROP_FRAME_WIDTH)/4)
        video.set(cv2.CAP_PROP_FRAME_HEIGHT, video.get(cv2.CAP_PROP_FRAME_HEIGHT)/4)

        refresh_holds = False
        refreshed = False
        frame_skipper = 0
        while video.isOpened() and not self.cancelled:
            success, frame = video.read()
            if not success:
                break

            self.notify(FluxReaderEventType.GET_FRAME, frame)

            if (refresh_holds or not refreshed) and (super().has_listener(FluxReaderEventType.HOLDS_PROCESSED_EVENT) or super().has_listener(FluxReaderEventType.FRAME_PROCESSED_EVENT)):
                refreshed = True
                holds_predictions = holds_detector.predict(frame, classes=[0])
                floor_predictions = holds_detector.predict(frame, classes=[1])
                holds_boxes = convert_image_box_outputs(holds_predictions)
                self.notify(FluxReaderEventType.HOLDS_PROCESSED_EVENT, holds_boxes)
                floor_boxes = convert_image_box_outputs(floor_predictions)
                self.notify(FluxReaderEventType.FLOOR_PROCESSED_EVENT, floor_boxes)

            if frame_skipper == 0 and (super().has_listener(FluxReaderEventType.SKELETONS_PROCESSED_EVENT) or super().has_listener(FluxReaderEventType.FRAME_PROCESSED_EVENT)):
                skeleton_prediction = skeleton_detector.predict(frame, img_size=512)
                skeletons = convert_image_skeleton_outputs(skeleton_prediction)
                self.notify(FluxReaderEventType.SKELETONS_PROCESSED_EVENT, self.nbr_frame_to_skip, frame_skipper, skeletons)
            
            if super().has_listener(FluxReaderEventType.FRAME_PROCESSED_EVENT):
                self.notify(FluxReaderEventType.FRAME_PROCESSED_EVENT, frame, holds_boxes, floor_boxes, skeletons, frame_skipper)
            frame_skipper = (frame_skipper + 1) % (self.nbr_frame_to_skip + 1)

        self.notify(FluxReaderEventType.END_OF_FILE_EVENT)
        video.release()