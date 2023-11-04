from interfaces.observer import Observer
from objects.skeletons_record import SkeletonsRecord
from enums.flux_reader_enum import FluxReaderEnum
from objects.skeleton import Skeleton
from utils.serializer import serialize_skeletons_record, deserialize_skeletons_record


class SkeletonRecordSaverListener(Observer):
    def __init__(self):
        self.skeleton_record = SkeletonsRecord()


    def update(self, observable, event_type, *args, **kwargs):
        if event_type == FluxReaderEnum.SKELETONS_PROCESSED:
            frame_skipper = args[0]
            skeletons = args[1]

            self.append_skeleton(frame_skipper, skeletons)
        elif event_type == FluxReaderEnum.END_OF_FILE:
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