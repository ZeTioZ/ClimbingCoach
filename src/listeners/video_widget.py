import cv2 # TODO change this to use tkinter

from objects.skeleton import Skeleton

from enums.flux_reader_enum import FluxReaderEnum
from interfaces.observer import Observer
from utils.draw_utils import box_visualizer, skeleton_visualizer

class VideoWidget(Observer):
    def __init__(self, video_widget):
        self.video_widget = video_widget


    def update(self, observable, event_type, *args, **kwargs): # TODO change this to use tkinter
        if event_type != FluxReaderEnum.FRAME_PROCESSED:
            return
        
        frame = args[0]
        holds_boxes = args[1]
        floors_boxes = args[2]
        skeletons = args[3]
        frame_skipper = args[4]

        for hold_box in holds_boxes:
            frame_with_holds = box_visualizer(frame, hold_box, (0, 255, 0))
        for floor_box in floors_boxes:
            frame_with_floors = box_visualizer(frame_with_holds, floor_box, (0, 0, 255))
        for skeleton in skeletons:
            frame_with_all = skeleton_visualizer(frame_with_floors, skeleton, (255, 0, 0))

            if isinstance(skeleton, Skeleton) and frame_skipper == 0:
                members_to_check = ["main_1", "main_2", "pied_1", "pied_2"]
                for hold_box in holds_boxes:
                    for member in skeleton.body.keys():
                        if member in members_to_check:
                            member_position = skeleton.body[member]
                            if hold_box.position_collide(member_position, margin=10):
                                cv2.rectangle(frame_with_all, (int(hold_box.positions[0].x), int(hold_box.positions[0].y)), (int(hold_box.positions[1].x), int(hold_box.positions[1].y)), (0, 0, 255), 2)
                                cv2.circle(frame_with_all, (int(member_position.x), int(member_position.y)), 5, (0, 255, 0), 1)
                                members_to_check.remove(member)
                                break