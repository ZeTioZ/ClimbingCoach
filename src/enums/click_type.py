from enum import Enum

class ClickType(Enum):
    """
    Click Type Enum
    
    Enum class for the the click types.
    """
    LEFT_CLICK = 1 # arg: x_coord, y_coord
    RIGHT_CLICK = 2 # arg: x_coord, y_coord