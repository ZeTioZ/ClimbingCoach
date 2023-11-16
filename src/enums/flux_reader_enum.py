from enum import Enum


class FluxReaderEnum(Enum):
    """
    Flux Reader Enum

    Enumerates the events types of flux reader.
    """
    GET_FRAME = 0, # This event gives you the current frame. Given args: frame.
    HOLDS_PROCESSED = 1, # This event gives you the current holds boxes. Given args: holds_boxes.
    FLOOR_PROCESSED = 2, # This event gives you the current floor boxes. Given args: floor_boxes.
    SKELETONS_PROCESSED = 3, # This event gives you the current skeletons positions. Given args: nbr_frame_to_skip, frame_skipper, skeletons.
    FRAME_PROCESSED = 4, # This event fires only when event 1, 2 and 3 are fired. Given args: frame, holds_boxes, floor_boxes, skeletons; frame_skipper.
    END_OF_FILE = 5, # This event fires when processing is over, returns the last processed frame. Given args: holds_boxes, floor_boxes, skeletons.