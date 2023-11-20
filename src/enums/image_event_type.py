from enums import EnumType


class ImageEventType(EnumType):
    """
    Image Event Type Enum

    Enum class for the the image event types.
    """
    CLICK_EVENT = 0
    DOUBLE_CLICK_EVENT = 1
    DRAG_EVENT = 2
    DROP_EVENT = 3