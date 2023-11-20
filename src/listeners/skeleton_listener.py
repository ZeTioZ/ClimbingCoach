import cv2

from interfaces.listener import Listener
from objects.skeletons_record import SkeletonsRecord
from enums.flux_reader_event_type import FluxReaderEventType
from objects.skeleton import Skeleton
from utils.serializer import serialize_skeletons_record, deserialize_skeletons_record


class SkeletonRecordSaverListener(Listener):
    def __init__(self):
        self.skeleton_record = SkeletonsRecord()


    def update(self, observable, event_types, *args, **kwargs):
        if FluxReaderEventType.SKELETONS_PROCESSED_EVENT in event_types:
            nbr_frame_to_skip = args[0]
            self.skeleton_record.frame_rate = observable.video.get(cv2.CAP_PROP_FPS) / nbr_frame_to_skip
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