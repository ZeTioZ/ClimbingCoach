import cv2
import time

from gui.app_state import AppState
from enums.flux_reader_event_type import FluxReaderEventType
from events.flux_reader_event import FluxReaderEvent
from interfaces.listener import Listener
from objects.skeleton import Skeleton
from objects.skeletons_record import SkeletonsRecord


class SkeletonRecordSaverListener(Listener):
	def __init__(self):
		super().__init__([FluxReaderEventType.SKELETONS_PROCESSED_EVENT, FluxReaderEventType.END_OF_FILE_EVENT])
		self.skeleton_record = SkeletonsRecord()
		self.start_time = 0

	def update(self, event, event_types, *args, **kwargs):
		if FluxReaderEventType.SKELETONS_PROCESSED_EVENT in event_types and isinstance(event, FluxReaderEvent):
			nbr_frame_to_skip = args[0]
			self.skeleton_record.frame_rate = event.video.get(cv2.CAP_PROP_FPS) / nbr_frame_to_skip
			frame_skipper = args[1]
			skeletons = args[2]

			self.append_skeleton(frame_skipper, skeletons)
		elif FluxReaderEventType.END_OF_FILE_EVENT in event_types:
			self.save_skeletons_record()
			self.event.unregister(self)

	def append_skeleton(self, frame_skipper, skeletons):
		if frame_skipper == 0:
			for skeleton in skeletons:
				if not isinstance(skeleton, Skeleton):
					return
			self.skeleton_record.append(skeletons)

	def start_timer(self):
		self.start_time = time.time()

	def save_skeletons_record(self):
		state = AppState()
		#run_queries.create_run(self.skeleton_record, time.time() - self.start_time, state.get_username(), state.get_route_name())
		return self.skeleton_record, time.time() - self.start_time, state.get_user()
