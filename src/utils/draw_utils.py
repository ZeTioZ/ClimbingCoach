import cv2
import numpy as np


def box_visualizer(image: np.ndarray, boxes: list, color: tuple = (0, 255, 0), thickness: int = 2):
    """
    Visualizes boxes in the given image.

    :param image: A numpy array representing the image.
    :param boxes: A list containing bounding boxes of the detected objects.
    :param wait_key: The amount of time to wait before closing the image.
    """
    for box in boxes:
        cv2.rectangle(image, (int(box.position1.x), int(box.position1.y)), (int(box.position2.x), int(box.position2.y)), color, thickness)
    return image