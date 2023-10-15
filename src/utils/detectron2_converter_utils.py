from objects.position import Position
from objects.box import Box


def convert_image_box_output(output: dict()) -> list:
    """
    Converts the output of the model to a list of boxes.

    :param output: A dictionary containing the predicted classes and bounding boxes of the detected objects.
    :return: A list of boxes.
    """
    boxes = []
    for box in output["instances"].pred_boxes.to('cpu'):
        position_1 = Position(box[0], box[1])
        position_2 = Position(box[2], box[3])
        boxes.append(Box(position_1, position_2))
    return boxes
