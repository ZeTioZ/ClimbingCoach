import cv2

from objects.holds_detector import HoldsDetector
from utils import box_visualizer
from utils import convert_image_box_output

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Left button down at ({}, {})".format(x, y))


def test_holds_detector():
    """
    Tests the HoldsDetector class by detecting objects in the test image and visualizing the detections.
    """
    detector = HoldsDetector("cpu")
    video = cv2.VideoCapture(0)

    if (video.isOpened() == False): 
        print("Error opening video stream or file")

    success, image = video.read()
    while success:
        success, image = video.read()
        if (success == False):
            break
        outputs = detector.predictor(image)
        outputs = convert_image_box_output(outputs)
        
        image = box_visualizer(image, outputs, color=(0, 0, 0), thickness=5)
        cv2.imshow("Holds", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    cv2.namedWindow("Holds")
    cv2.setMouseCallback("Holds", mouse_callback)
    test_holds_detector()