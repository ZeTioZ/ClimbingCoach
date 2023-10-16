import numpy as np

from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg


"""
Loads a model from a file and predicts objects in images.
"""
class ModelLoader:
    def __init__(self, merge_from_file, model, model_device: str = 'cuda', score_thresh_test: float = 0.8):
        """
        Initializes the ModelLoader.

        :param merge_from_file: The path to the config file to merge with the default config.
        :param model: The path to the model file.
        :param model_device: The device to use for the model.
        :param score_thresh_test: The score threshold for the model.
        """
        self.cfg = get_cfg()
        self.cfg.merge_from_file(merge_from_file)
        self.cfg.MODEL.WEIGHTS = model
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = score_thresh_test
        self.cfg.MODEL.DEVICE=model_device
        self.predictor = DefaultPredictor(self.cfg)

    
    def predict(self, image: np.ndarray) -> dict:
        """
        Predicts objects in the given image.

        :param image: The image to predict objects in.
        :return: A dictionary containing the predictions.
        """
        outputs = self.predictor(image)
        return outputs