import time

import cv2

from database.queries import run_queries
from enums.flux_reader_event_type import FluxReaderEventType
from events.flux_reader_event import FluxReaderEvent
from gui.app_state import AppState
from interfaces.listener import Listener
from objects.skeleton import Skeleton
from objects.skeletons_record import SkeletonsRecord


class SkeletonRecordSaverListener(Listener):
	def __init__(self):
		super().__init__([FluxReaderEventType.SKELETONS_PROCESSED_EVENT, FluxReaderEventType.END_OF_FILE_EVENT])
		self.skeleton_record = SkeletonsRecord()
		self.hit_holds = []
		self.start_time = 0                                                                                                                                

	def update(self, event, event_types, *args, **kwargs):
		if FluxReaderEventType.SKELETONS_PROCESSED_EVENT in event_types and isinstance(event, FluxReaderEvent):
			nbr_frame_to_skip = args[0]
			skeletons = args[1]
			holds = args[2]
			self.skeleton_record.frame_rate = event.video.get(cv2.CAP_PROP_FPS) / nbr_frame_to_skip
			self.append_skeleton(skeletons, holds)
		elif FluxReaderEventType.END_OF_FILE_EVENT in event_types:
			self.save_skeletons_record()
			event.unregister(self)

	def append_skeleton(self, skeletons, holds):
		for skeleton in skeletons:
			if not isinstance(skeleton, Skeleton):
				return
			members_to_check = ["main_1", "main_2", "pied_1", "pied_2"]
			for hold in holds:
				for member in skeleton.body.keys():
					if member in members_to_check:
						member_position = skeleton.body[member]
						if hold.position_collide(member_position, margin=10) and hold not in self.hit_holds:
							self.hit_holds.append(hold)
							members_to_check.remove(member)
							break
		self.skeleton_record.append(skeletons)

	def start_timer(self):
		self.start_time = time.time()

	def save_skeletons_record(self):
		state = AppState()
		print(state.get_route())
		run_queries.create_run(self.skeleton_record, self.hit_holds, int(time.time() - self.start_time),
		                       state.get_user().username, state.get_route().name)
