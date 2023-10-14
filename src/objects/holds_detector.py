import cv2
import os
import numpy as np

from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog


MODEL_DIRECTORY = "./resources/model/"
VIDEOS_DIRECTORY = "./resources/videos/"


class HoldsDetector:
    """
    HoldsDetector class for detecting holds in an image using the Detectron2 library.
    Model source: https://github.com/xiaoxiae/Indoor-Climbing-Hold-and-Route-Segmentation

    Args:
        model_device: The device on which to run the model (default: 'cuda', other options: 'cpu').
        score_thresh_test: The score threshold for the model (default: 0.8).
    """
    def __init__(self, model_device: str = 'cuda', score_thresh_test: float = 0.8):
        """
        Initializes the HoldsDetector object with the configuration file for the model.
        """
        self.cfg = get_cfg()
        self.cfg.merge_from_file(os.path.join(MODEL_DIRECTORY, "experiment_config.yml"))
        self.cfg.MODEL.WEIGHTS = os.path.join(MODEL_DIRECTORY, "model_final.pth")
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = score_thresh_test
        self.cfg.MODEL.DEVICE=model_device
        self.predictor = DefaultPredictor(self.cfg)
        
        MetadataCatalog.get("meta").thing_classes = ["hold", "volume"]
        self.metadata = MetadataCatalog.get("meta")


    def detect_holds(self, image: np.ndarray) -> dict:
        """
        Detects objects in the given image using the model.

        :param image: A numpy array representing the image.
        :return: A dictionary containing the predicted classes and bounding boxes of the detected objects.
        """
        outputs = self.predictor(image)
        return outputs
