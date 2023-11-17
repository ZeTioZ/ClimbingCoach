from PIL import Image
import os
import numpy as np

from libs.model_loader import ModelLoader
from main import MODELS_DIRECTORY
from utils.draw_utils import box_visualizer
from utils.yolov8_converter_utils import convert_image_box_outputs

def apply_model_on_image(image: Image) -> Image:
    """Apply the model on the image."""
    
    holds_detector = ModelLoader(os.path.join(MODELS_DIRECTORY, "holds_model_yolov8l.pt"))

    np_image = np.array(image)

    holds_predictions = holds_detector.predict(np_image, classes=[0])
    holds_boxes = convert_image_box_outputs(holds_predictions)

    res_np_image = box_visualizer(np_image, holds_boxes)

    res_image = Image.fromarray(res_np_image)

    return res_image