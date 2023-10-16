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


def skeleton_visualizer(image: np.ndarray, skeleton, color: tuple = (0, 255, 0), thickness: int = 2):
    if not isinstance(skeleton, Skeleton):
        return image
    cv2.line(image, (int(skeleton.body["main_1"].x), int(skeleton.body["main_1"].y)), (int(skeleton.body["coude_1"].x), int(skeleton.body["coude_1"].y)), color, thickness)
    cv2.line(image, (int(skeleton.body["coude_1"].x), int(skeleton.body["coude_1"].y)), (int(skeleton.body["epaule_1"].x), int(skeleton.body["epaule_1"].y)), color, thickness)
    cv2.line(image, (int(skeleton.body["epaule_1"].x), int(skeleton.body["epaule_1"].y)), (int(skeleton.body["bassin_1"].x), int(skeleton.body["bassin_1"].y)), color, thickness)
    cv2.line(image, (int(skeleton.body["bassin_1"].x), int(skeleton.body["bassin_1"].y)), (int(skeleton.body["genou_1"].x), int(skeleton.body["genou_1"].y)), color, thickness)
    cv2.line(image, (int(skeleton.body["genou_1"].x), int(skeleton.body["genou_1"].y)), (int(skeleton.body["pied_1"].x), int(skeleton.body["pied_1"].y)), color, thickness)

    cv2.line(image, (int(skeleton.body["main_2"].x), int(skeleton.body["main_2"].y)), (int(skeleton.body["coude_2"].x), int(skeleton.body["coude_2"].y)), color, thickness)
    cv2.line(image, (int(skeleton.body["coude_2"].x), int(skeleton.body["coude_2"].y)), (int(skeleton.body["epaule_2"].x), int(skeleton.body["epaule_2"].y)), color, thickness)
    cv2.line(image, (int(skeleton.body["epaule_2"].x), int(skeleton.body["epaule_2"].y)), (int(skeleton.body["bassin_2"].x), int(skeleton.body["bassin_2"].y)), color, thickness)
    cv2.line(image, (int(skeleton.body["bassin_2"].x), int(skeleton.body["bassin_2"].y)), (int(skeleton.body["genou_2"].x), int(skeleton.body["genou_2"].y)), color, thickness)
    cv2.line(image, (int(skeleton.body["genou_2"].x), int(skeleton.body["genou_2"].y)), (int(skeleton.body["pied_2"].x), int(skeleton.body["pied_2"].y)), color, thickness)

    cv2.line(image, (int(skeleton.body["epaule_1"].x), int(skeleton.body["epaule_1"].y)), (int(skeleton.body["epaule_2"].x), int(skeleton.body["epaule_2"].y)), color, thickness)
    cv2.line(image, (int(skeleton.body["bassin_1"].x), int(skeleton.body["bassin_1"].y)), (int(skeleton.body["bassin_2"].x), int(skeleton.body["bassin_2"].y)), color, thickness)
    return image


def refresh(image: np.ndarray, previous_value, x = 100, y = 100) -> bool:
    """
    Returns whether the image got moved or not.
    """
    return np.all(image[x, y] != previous_value) or previous_value is None
