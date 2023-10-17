import cv2, os

from libs.model_loader import ModelLoader
from utils.yolov8_converter_utils import convert_image_box_outputs, convert_image_skeleton_outputs
from utils.draw_utils import skeleton_visualizer, box_visualizer

from objects.skeleton import Skeleton

MODELS_DIRECTORY = "./resources/models/"
VIDEOS_DIRECTORY = "./resources/videos/"


def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Left button down at ({}, {})".format(x, y))


def test_holds_detector():
    """
    Tests the HoldsDetector class by detecting objects in the test image and visualizing the detections.
    """
    holds_detector = ModelLoader(os.path.join(MODELS_DIRECTORY, "holds_model_yolov8l.pt"))
    skeleton_detector = ModelLoader("yolov8l-pose.pt")

    video = cv2.VideoCapture(os.path.join(VIDEOS_DIRECTORY, "Escalade_Mouvement.mp4"))
    video.set(cv2.CAP_PROP_FRAME_WIDTH, video.get(cv2.CAP_PROP_FRAME_WIDTH)/2)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, video.get(cv2.CAP_PROP_FRAME_WIDTH)/2)

    if (video.isOpened() == False):
        print("Error opening video stream or file")

    success, image = video.read()
    while success:
        success, image = video.read()
        if not success:
            break

        holds_predictions = holds_detector.predict(image)
        holds_boxes = convert_image_box_outputs(holds_predictions)
        image = box_visualizer(image, holds_boxes, color=(0, 255, 0), thickness=1)

        skeleton_prediction = skeleton_detector.predict(image)
        skeletons = convert_image_skeleton_outputs(skeleton_prediction)

        for skeleton in skeletons:
            image = skeleton_visualizer(image, skeleton, color=(0, 0, 255), thickness=1)

            if isinstance(skeleton, Skeleton):
                members_to_check = ["main_1", "main_2", "pied_1", "pied_2"]
                for hold_box in holds_boxes:
                    for member in skeleton.body.keys():
                        if member in members_to_check:
                            member_position = skeleton.body[member]
                            if hold_box.position_collide(member_position, margin=10):
                                cv2.rectangle(image, (int(hold_box.positions[0].x), int(hold_box.positions[0].y)), (int(hold_box.positions[1].x), int(hold_box.positions[1].y)), (0, 0, 255), 2)
                                cv2.circle(image, (int(member_position.x), int(member_position.y)), 5, (0, 255, 0), 1)
                                members_to_check.remove(member)
                                break

        cv2.imshow("Holds", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    # cv2.namedWindow("Holds")
    # cv2.setMouseCallback("Holds", mouse_callback)
    test_holds_detector()