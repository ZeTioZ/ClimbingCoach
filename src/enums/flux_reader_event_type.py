from enums.event_type import EventType


class FluxReaderEventType(EventType):
	"""
	Flux Reader Event Type

	Enumerates the events types of flux reader.
	"""
	GET_FRAME_EVENT = 0,  # This event gives you the current frame. Given args: frame.
	HOLDS_PROCESSED_EVENT = 1,  # This event gives you the current holds boxes. Given args: holds_boxes, frame.
	FLOOR_PROCESSED_EVENT = 2,  # This event gives you the current floor boxes. Given args: floor_boxes, frame.
	SKELETONS_PROCESSED_EVENT = 3,  # This event gives you the current skeletons positions. Given args: nbr_frame_to_skip, skeletons, holds, frame.
	FRAME_PROCESSED_EVENT = 4,  # This event fires only when event 1, 2 and 3 are fired. Given args: frame, holds_boxes, floor_boxes, skeletons, frame_skipper.
	END_OF_FILE_EVENT = 5,  # This event fires when processing is over, returns the last processed frame. Given args:.
