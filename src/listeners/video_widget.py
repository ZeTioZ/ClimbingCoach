import cv2  # TODO change this to use tkinter

from enums.event_type import EventType
from enums.flux_reader_event_type import FluxReaderEventType
from interfaces.event import Event
from interfaces.listener import Listener
from objects.skeleton import Skeleton
from utils.draw_utils import box_visualizer, skeleton_visualizer


class VideoWidget(Listener):
	def __init__(self, event_types):
		super().__init__(event_types)
		self.last_image = None

	def update(self, event: Event, event_types: [EventType], *args, **kwargs):
		print("update")
		if FluxReaderEventType.FRAME_PROCESSED_EVENT in event_types:
			frame = args[0]
			holds_boxes = args[1]
			floors_boxes = args[2]
			skeletons = args[3]
			frame_skipper = args[4]

			frame_with_holds = box_visualizer(frame, holds_boxes, (0, 255, 0))
			frame_with_floors = box_visualizer(frame_with_holds, floors_boxes, (0, 0, 255))
			frame_with_all = frame_with_floors

			for skeleton in skeletons:
				frame_with_all = skeleton_visualizer(frame_with_floors, skeleton, (255, 0, 0))

				if isinstance(skeleton, Skeleton) and frame_skipper == 0:
					members_to_check = ["main_1", "main_2", "pied_1", "pied_2"]
					for hold_box in holds_boxes:
						for member in skeleton.body.keys():
							if member in members_to_check:
								member_position = skeleton.body[member]
								if hold_box.position_collide(member_position, margin=10):
									cv2.rectangle(frame_with_all, hold_box.positions[0].to_tuple(),
									              hold_box.positions[1].to_tuple(), (0, 0, 255), 2)
									cv2.circle(frame_with_all, member_position.to_tuple(), 5, (0, 255, 0), 1)
									members_to_check.remove(member)
									break
			self.last_image = frame_with_all
			
		if FluxReaderEventType.GET_FRAME_EVENT in event_types:
			frame = args[0]
			print("frame")
			self.last_image = frame