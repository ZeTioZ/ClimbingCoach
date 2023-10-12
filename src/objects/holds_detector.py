import cv2
import os

from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog

MODEL_DIRECTORY = "./resources/model/"
VIDEOS_DIRECTORY = "./resources/videos/"

class HoldsDetector:
    """
    HoldsDetector class for detecting holds in an image using the Detectron2 library.

    Args:
        model_device: The device on which to run the model (default: 'cuda', other options: 'cpu').
        score_thresh_test: The score threshold for the model (default: 0.8).
    """
    def __init__(self, model_device='cuda', score_thresh_test=0.8):
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

    def detect_holds(self, image) -> dict:
        """
        Detects objects in the given image using the Faster R-CNN model from the model zoo.

        Args:
            image: A numpy array representing the image.

        Returns:
            A dictionary containing the predicted classes and bounding boxes of the detected objects.
        """
        outputs = self.predictor(image)
        return outputs

    def visualize_detections(self, image, outputs, wait_key=0):
        """
        Visualizes the detected objects in the given image.

        Args:
            image: A numpy array representing the image.
            outputs: A dictionary containing the predicted classes and bounding boxes of the detected objects.
        """
        v = Visualizer(image[:, :, ::-1], metadata=self.metadata)
        for box in outputs["instances"].pred_boxes.to('cpu'):
            v.draw_box(box)
            # TODO: Create box objects from the predicted boxes and add them to the holds list
        v = v.get_output()
        cv2.imshow("Holds", v.get_image()[:, :, ::-1])
        cv2.waitKey(wait_key)

def test_holds_detector():
    """
    Tests the HoldsDetector class by detecting objects in the test image and visualizing the detections.
    """
    detector = HoldsDetector()
    video = cv2.VideoCapture(os.path.join(VIDEOS_DIRECTORY, "test.mp4"))

    if (video.isOpened() == False): 
        print("Error opening video stream or file")

    success, image = video.read()
    while success:
        success, image = video.read()
        if (success == False):
            break
        outputs = detector.predictor(image)
        detector.visualize_detections(image, outputs, wait_key=1)

if __name__ == "__main__":
    test_holds_detector()