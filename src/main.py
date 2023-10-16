import cv2, os

from libs.model_loader import ModelLoader
from utils.detectron2_converter_utils import convert_image_box_output
from utils.draw_utils import skeleton_visualizer, box_visualizer, refresh

from utils.skeleton_scanner import SkeletonScanner
from objects.skeleton import Skeleton
from detectron2 import model_zoo

MODELS_DIRECTORY = "./resources/models/"
VIDEOS_DIRECTORY = "./resources/videos/"


def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Left button down at ({}, {})".format(x, y))


def test_holds_detector():
    """
    Tests the HoldsDetector class by detecting objects in the test image and visualizing the detections.
    """
    holds_detector = ModelLoader(os.path.join(MODELS_DIRECTORY, "experiment_config.yml"), os.path.join(MODELS_DIRECTORY, "model_final.pth"))
    skeleton_detector = ModelLoader(model_zoo.get_config_file("COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml"), model_zoo.get_checkpoint_url("COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml"))
    
    video = cv2.VideoCapture(2)
    if (video.isOpened() == False): 
        print("Error opening video stream or file")

    scanner = SkeletonScanner(2)

    success, image = video.read()
    refresh_indicator = None
    should_refresh = True
    while success:
        success, image = video.read()
        if not success:
            break

        if refresh_indicator is not "no-refresh" and refresh(image, refresh_indicator, 10, 10):
            refresh_indicator = image[10, 10] if should_refresh else "no-refresh"
            outputs = holds_detector.predict(image)
            boxes = convert_image_box_output(outputs)

        image = box_visualizer(image, boxes, color=(0, 255, 0), thickness=1)
        skeleton = scanner.generateSkeleton(image)[1]
        image = skeleton_visualizer(image, skeleton, color=(0, 0, 255), thickness=1)

        if isinstance(skeleton, Skeleton):
            members_to_check = ["main_1", "main_2", "pied_1", "pied_2"]
            for box in boxes:
                for member in skeleton.body.keys():
                    if member in members_to_check:
                        member_position = skeleton.body[member]
                        if box.position_collide(member_position, margin=10):
                            cv2.rectangle(image, (int(box.positions[0].x), int(box.positions[0].y)), (int(box.positions[1].x), int(box.positions[1].y)), (0, 0, 255), 2)
                            cv2.circle(image, (int(member_position.x), int(member_position.y)), 5, (0, 255, 0), 2)
                            members_to_check.remove(member)
                            break

        cv2.imshow("Holds", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def test_skeleton_scanner_file():
    """
    Tests the SkeletonScanner class by generating a skeleton from the test image and visualizing the skeleton.
    """
    skeleton_scanner = SkeletonScanner(os.path.join(VIDEOS_DIRECTORY, "Escalade_Prof.mp4"), frequency=4)
    skeleton_scanner.generateParcours()


def test_skeleton_scanner_webcam():
    """
    Tests the SkeletonScanner class by generating a skeleton from the webcam and visualizing the skeleton.
    """
    skeleton_scanner = SkeletonScanner(0)
    skeleton_scanner.generateParcours()


if __name__ == "__main__":
    cv2.namedWindow("Holds")
    cv2.setMouseCallback("Holds", mouse_callback)
    test_holds_detector()
    # test_skeleton_scanner_file()
    # test_skeleton_scanner_webcam()