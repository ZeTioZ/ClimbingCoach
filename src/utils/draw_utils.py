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


def skeleton_visualizer(image: np.ndarray, skeleton, color: tuple = (0, 255, 0), thickness: int = 2):
    cv2.line(image, pt1=(int(skeleton.main1.x), int(skeleton.main1.y)), pt2=(int(skeleton.coude1.x), int(skeleton.coude1.y)), color=color, thickness=thickness)
    cv2.line(image, pt1=(int(skeleton.coude1.x), int(skeleton.coude1.y)), pt2=(int(skeleton.epaule1.x), int(skeleton.epaule1.y)), color=color, thickness=thickness)
    cv2.line(image, pt1=(int(skeleton.epaule1.x), int(skeleton.epaule1.y)), pt2=(int(skeleton.bassin1.x), int(skeleton.bassin1.y)), color=color, thickness=thickness)
    cv2.line(image, pt1=(int(skeleton.bassin1.x), int(skeleton.bassin1.y)), pt2=(int(skeleton.genou1.x), int(skeleton.genou1.y)), color=color, thickness=thickness)
    cv2.line(image, pt1=(int(skeleton.genou1.x), int(skeleton.genou1.y)), pt2=(int(skeleton.pied1.x), int(skeleton.pied1.y)), color=color, thickness=thickness)
    cv2.line(image, pt1=(int(skeleton.main2.x), int(skeleton.main2.y)), pt2=(int(skeleton.coude2.x), int(skeleton.coude2.y)), color=color, thickness=thickness)
    cv2.line(image, pt1=(int(skeleton.coude2.x), int(skeleton.coude2.y)), pt2=(int(skeleton.epaule2.x), int(skeleton.epaule2.y)), color=color, thickness=thickness)
    cv2.line(image, pt1=(int(skeleton.epaule2.x), int(skeleton.epaule2.y)), pt2=(int(skeleton.bassin2.x), int(skeleton.bassin2.y)), color=color, thickness=thickness)
    cv2.line(image, pt1=(int(skeleton.bassin2.x), int(skeleton.bassin2.y)), pt2=(int(skeleton.genou2.x), int(skeleton.genou2.y)), color=color, thickness=thickness)
    cv2.line(image, pt1=(int(skeleton.genou2.x), int(skeleton.genou2.y)), pt2=(int(skeleton.pied2.x), int(skeleton.pied2.y)), color=color, thickness=thickness)
    cv2.line(image, pt1=(int(skeleton.bassin1.x), int(skeleton.bassin1.y)), pt2=(int(skeleton.bassin2.x), int(skeleton.bassin2.y)), color=color, thickness=thickness)
    cv2.line(image, pt1=(int(skeleton.epaule1.x), int(skeleton.epaule1.y)), pt2=(int(skeleton.epaule2.x), int(skeleton.epaule2.y)), color=color, thickness=thickness)
    return image
