from objects.position import Position
from objects.box import Box
from objects.skeleton import Skeleton


def convert_image_box_outputs(outputs) -> list:
    """
    Converts the output of the model to a list of boxes.

    :param output: A dictionary containing the predicted classes and bounding boxes of the detected objects.
    :return: A list of boxes.
    """
    boxes = []
    for box in outputs[0].boxes:
        box = box.xyxy[0].tolist()
        position_1 = Position(box[0], box[1])
        position_2 = Position(box[2], box[3])
        boxes.append(Box(position_1, position_2))
    return boxes


def convert_image_skeleton_outputs(predictions_outputs) -> list:
    """
    Converts the output of the model to a skeleton.

    :param predictions_outputs: A dictionary containing the predicted elements of the image.
    :return: A list of skeletons.
    """
    skeletons = []
    for skeleton_keypoints in predictions_outputs[0].keypoints.xy:
        keypoints = skeleton_keypoints.tolist()
        if not len(keypoints) == 17: continue
        skeleton = Skeleton(
            main_1 = Position(keypoints[9][0], keypoints[9][1]),
            main_2 = Position(keypoints[10][0], keypoints[10][1]),
            pied_1 = Position(keypoints[15][0], keypoints[15][1]),
            pied_2 = Position(keypoints[16][0], keypoints[16][1]),
            epaule_1 = Position(keypoints[5][0], keypoints[5][1]),
            epaule_2 = Position(keypoints[6][0], keypoints[6][1]),
            coude_1 = Position(keypoints[7][0], keypoints[7][1]),
            coude_2 = Position(keypoints[8][0], keypoints[8][1]),
            bassin_1 = Position(keypoints[11][0], keypoints[11][1]),
            bassin_2 = Position(keypoints[12][0], keypoints[12][1]),
            genou_1 = Position(keypoints[13][0], keypoints[13][1]),
            genou_2 = Position(keypoints[14][0], keypoints[14][1])
        )
        skeletons.append(skeleton)
    return skeletons