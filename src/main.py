import cv2, os

from libs.model_loader import ModelLoader
from utils.yolov8_converter_utils import convert_image_box_outputs, convert_image_skeleton_outputs
from utils.draw_utils import skeleton_visualizer, box_visualizer
from utils.serializer import serialize_skeletons_record, deserialize_skeletons_record

from objects.skeletons_record import SkeletonsRecord
from objects.skeleton import Skeleton

MODELS_DIRECTORY = "./resources/models/"
VIDEOS_DIRECTORY = "./resources/videos/"


def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Left button down at ({}, {})".format(x, y))


def test_holds_detector(nbr_frame_to_skip: int = 2):
    """
    Tests the HoldsDetector class by detecting objects in the test image and visualizing the detections.
    """
    holds_detector = ModelLoader(os.path.join(MODELS_DIRECTORY, "holds_model_yolov8l.pt"))
    skeleton_detector = ModelLoader(os.path.join(MODELS_DIRECTORY, "yolov8l-pose.pt"))

    video = cv2.VideoCapture(os.path.join(VIDEOS_DIRECTORY, "Escalade_Fixe.mp4"))
    video.set(cv2.CAP_PROP_FRAME_WIDTH, video.get(cv2.CAP_PROP_FRAME_WIDTH)/4)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, video.get(cv2.CAP_PROP_FRAME_HEIGHT)/4)

    refresh_holds = False
    refreshed = False
    frame_skipper = 0
    skeletons_record = SkeletonsRecord()
    while video.isOpened():
        success, image = video.read()
        if not success:
            break

        if refresh_holds or not refreshed:
            refreshed = True
            holds_predictions = holds_detector.predict(image, classes=[0])
            floor_predictions = holds_detector.predict(image, classes=[1])
            holds_boxes = convert_image_box_outputs(holds_predictions)
            floor_boxes = convert_image_box_outputs(floor_predictions)

        image = box_visualizer(image, holds_boxes, color=(0, 255, 0), thickness=1)
        image = box_visualizer(image, floor_boxes, color=(0, 255, 0), thickness=1)

        if frame_skipper == 0:
            skeleton_prediction = skeleton_detector.predict(image, img_size=512)
            skeletons = convert_image_skeleton_outputs(skeleton_prediction)
            skeletons_record.append(skeletons)
        
        for skeleton in skeletons:
            image = skeleton_visualizer(image, skeleton, color=(0, 0, 255), thickness=1)

            if isinstance(skeleton, Skeleton) and frame_skipper == 0:
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
        frame_skipper = (frame_skipper + 1) % (nbr_frame_to_skip + 1)

        cv2.imshow("Holds", image)
        if cv2.waitKey(int((1000/video.get(cv2.CAP_PROP_FPS))-5)) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    cv2.namedWindow("Holds")
    cv2.setMouseCallback("Holds", mouse_callback)
    test_holds_detector(3)
