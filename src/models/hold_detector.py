from PIL import Image
import os
import numpy as np

from objects.box import Box

from libs.model_loader import ModelLoader
from main import MODELS_DIRECTORY
from utils.draw_utils import box_visualizer
from utils.yolov8_converter_utils import convert_image_box_outputs

class HoldDetector:

    def __init__(self):
        self.__model = ModelLoader(os.path.join(MODELS_DIRECTORY, "holds_model_yolov8l.pt"))
        self.__holds: list[Box] = []


    def get_holds(self) -> list[Box]:
        """Return the holds detected by the model."""
        return self.__holds


    def analyse_image(self, image: Image) -> list[Box]:
        """Analyse the image and store the holds in the class attribute."""

        np_image = np.array(image)

        holds_predictions = self.__model.predict(np_image, classes=[0], device="cpu")
        holds_boxes = convert_image_box_outputs(holds_predictions)

        self.__holds = holds_boxes
        return holds_boxes
    

    def __is_already_analysed(self) -> bool:
        """Return True if the image has already been analysed, False otherwise."""
        return len(self.__holds) > 0


    def apply_model_on_image(self, image: Image, path: list[Box] = []) -> Image:
        """Apply the model on the image."""
        
        np_image = np.array(image)

        if(not self.__is_already_analysed()):
            self.analyse_image(image)

        res_np_image = box_visualizer(np_image, self.__holds)
        res_np_image = box_visualizer(res_np_image, path, (0, 0, 255))

        res_image = Image.fromarray(res_np_image)
        return res_image