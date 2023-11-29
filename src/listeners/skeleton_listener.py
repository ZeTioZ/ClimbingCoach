import cv2

from enums.flux_reader_event_type import FluxReaderEventType
from events.flux_reader_event import FluxReaderEvent
from interfaces.listener import Listener
from objects.skeleton import Skeleton
from objects.skeletons_record import SkeletonsRecord
from utils.serializer_utils import serialize_skeletons_record, deserialize_skeletons_record


class SkeletonRecordSaverListener(Listener):
	def __init__(self):
		super().__init__([FluxReaderEventType.SKELETONS_PROCESSED_EVENT, FluxReaderEventType.END_OF_FILE_EVENT])
		self.skeleton_record = SkeletonsRecord()

	def update(self, event, event_types, *args, **kwargs):
		if FluxReaderEventType.SKELETONS_PROCESSED_EVENT in event_types and isinstance(event, FluxReaderEvent):
			nbr_frame_to_skip = args[0]
			self.skeleton_record.frame_rate = event.video.get(cv2.CAP_PROP_FPS) / nbr_frame_to_skip
			frame_skipper = args[1]
			skeletons = args[2]

			self.append_skeleton(frame_skipper, skeletons)
		elif FluxReaderEventType.END_OF_FILE_EVENT in event_types:
			self.save_skeletons_record()

	def append_skeleton(self, frame_skipper, skeletons):
		if frame_skipper == 0:
			for skeleton in skeletons:
				if not isinstance(skeleton, Skeleton):
					return
			self.skeleton_record.append(skeletons)

	def save_skeletons_record(self):
		serialized_skeletons = serialize_skeletons_record(self.skeleton_record)
		print("Saved skeletons records to memory.")
		print(deserialize_skeletons_record(serialized_skeletons))
