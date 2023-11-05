import cv2, os
from interfaces.observable import Observable

from enums.flux_reader_enum import FluxReaderEnum
from libs.model_loader import ModelLoader
from utils.yolov8_converter_utils import convert_image_box_outputs, convert_image_skeleton_outputs

MODELS_DIRECTORY = "./resources/models/"
VIDEOS_DIRECTORY = "./resources/videos/"


class FluxReaderEvent(Observable):
    def __init__(self, flux: str = "0", width: int = 640, height: int = 480, nbr_frame_to_skip: int = 2):
        self.flux = flux
        self.video = cv2.VideoCapture(self.flux)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        self.nbr_frame_to_skip = nbr_frame_to_skip
        self.holds_boxes = []
        self.floor_boxes = []
        self.skeletons = []
        

    def process(self):
        holds_detector = ModelLoader(os.path.join(MODELS_DIRECTORY, "holds_model_yolov8l.pt"))
        skeleton_detector = ModelLoader(os.path.join(MODELS_DIRECTORY, "yolov8l-pose.pt"))

        video = cv2.VideoCapture(self.flux)
        video.set(cv2.CAP_PROP_FRAME_WIDTH, video.get(cv2.CAP_PROP_FRAME_WIDTH)/4)
        video.set(cv2.CAP_PROP_FRAME_HEIGHT, video.get(cv2.CAP_PROP_FRAME_HEIGHT)/4)

        refresh_holds = False
        refreshed = False
        frame_skipper = 0
        while video.isOpened():
            success, frame = video.read()
            if not success:
                break

            self.notify(FluxReaderEnum.GET_FRAME, frame)

            if refresh_holds or not refreshed:
                refreshed = True
                holds_predictions = holds_detector.predict(frame, classes=[0])
                floor_predictions = holds_detector.predict(frame, classes=[1])
                holds_boxes = convert_image_box_outputs(holds_predictions)
                self.notify(FluxReaderEnum.HOLDS_PROCESSED, holds_boxes)
                floor_boxes = convert_image_box_outputs(floor_predictions)
                self.notify(FluxReaderEnum.FLOOR_PROCESSED, floor_boxes)

            if frame_skipper == 0:
                skeleton_prediction = skeleton_detector.predict(frame, img_size=512)
                skeletons = convert_image_skeleton_outputs(skeleton_prediction)
                self.notify(FluxReaderEnum.SKELETONS_PROCESSED, frame_skipper, skeletons)
            
            self.notify(FluxReaderEnum.FRAME_PROCESSED, frame, holds_boxes, floor_boxes, skeletons, frame_skipper)
            frame_skipper = (frame_skipper + 1) % (self.nbr_frame_to_skip + 1)

        self.notify(FluxReaderEnum.END_OF_FILE, holds_boxes, floor_boxes, skeletons)
        video.release()