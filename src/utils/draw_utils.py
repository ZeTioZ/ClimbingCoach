import cv2
import numpy as np

from objects.skeleton import Skeleton


def box_visualizer(image: np.ndarray, boxes: list, color: tuple = (0, 255, 0), thickness: int = 2):
    """
    Visualizes boxes in the given image.

    :param image: A numpy array representing the image.
    :param boxes: A list containing bounding boxes of the detected objects.
    :param wait_key: The amount of time to wait before closing the image.
    """
    for box in boxes:
        cv2.rectangle(image, (int(box.positions[0].x), int(box.positions[0].y)), (int(box.positions[1].x), int(box.positions[1].y)), color, thickness)
    return image


def line(image: np.ndarray, skeleton: Skeleton, membre_1: str, membre_2: str, color: tuple = (0, 255, 0), thickness: int = 2):
    if skeleton.exist(membre_1) and skeleton.exist(membre_2):
      cv2.line(image, skeleton.body[membre_1].to_tuple(), skeleton.body[membre_2].to_tuple(), color, thickness)


def skeleton_visualizer(image: np.ndarray, skeleton, color: tuple = (0, 255, 0), thickness: int = 2):
    if not isinstance(skeleton, Skeleton):
        return image

    # Left
    line(image, skeleton, "main_1", "coude_1", color, thickness)
    line(image, skeleton, "coude_1", "epaule_1", color, thickness)
    line(image, skeleton, "epaule_1", "bassin_1", color, thickness)
    line(image, skeleton, "bassin_1", "genou_1", color, thickness)
    line(image, skeleton, "genou_1", "pied_1", color, thickness)
    
    #Right
    line(image, skeleton, "main_2", "coude_2", color, thickness)
    line(image, skeleton, "coude_2", "epaule_2", color, thickness)
    line(image, skeleton, "epaule_2", "bassin_2", color, thickness)
    line(image, skeleton, "bassin_2", "genou_2", color, thickness)
    line(image, skeleton, "genou_2", "pied_2", color, thickness)

    # Body box
    line(image, skeleton, "epaule_1", "epaule_2", color, thickness)
    line(image, skeleton, "bassin_1", "bassin_2", color, thickness)
    return image


def refresh(image: np.ndarray, previous_value, x = 100, y = 100) -> bool:
    """
    Returns whether the image got moved or not.
    """
    return np.all(image[x, y] != previous_value) or previous_value is None
