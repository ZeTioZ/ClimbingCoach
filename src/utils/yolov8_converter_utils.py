from objects.box import Box
from objects.position import Position
from objects.skeleton import Skeleton


def convert_image_box_outputs(outputs) -> list:
	"""
	Converts the output of the model to a list of boxes.

	:param outputs: A dictionary containing the predicted classes and bounding boxes of the detected objects.
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
	for skeleton_key_points in predictions_outputs[0].keypoints.xy:
		key_points = skeleton_key_points.tolist()
		if len(key_points) != 17:
			continue
		skeleton = Skeleton(
			main_1=Position(key_points[9][0], key_points[9][1]),
			main_2=Position(key_points[10][0], key_points[10][1]),
			pied_1=Position(key_points[15][0], key_points[15][1]),
			pied_2=Position(key_points[16][0], key_points[16][1]),
			epaule_1=Position(key_points[5][0], key_points[5][1]),
			epaule_2=Position(key_points[6][0], key_points[6][1]),
			coude_1=Position(key_points[7][0], key_points[7][1]),
			coude_2=Position(key_points[8][0], key_points[8][1]),
			bassin_1=Position(key_points[11][0], key_points[11][1]),
			bassin_2=Position(key_points[12][0], key_points[12][1]),
			genou_1=Position(key_points[13][0], key_points[13][1]),
			genou_2=Position(key_points[14][0], key_points[14][1])
		)
		skeletons.append(skeleton)
	return skeletons
