import os.path

PRIMARY_COLOR = "#0b7687"
PRIMARY_HOVER_COLOR = "#0a4247"

SECONDARY_COLOR = "#7f6360"
SECONDARY_HOVER_COLOR = "#524141"

LIGHT_GREEN = "#248f6d"
DARK_GREEN = "#1b7254"

PARENT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RESSOURCES_PATH = os.path.join(PARENT_PATH, 'resources')

actual_height = 0

def set_height_utils(height):
    global actual_height
    actual_height = height

def v(x: float|int, view: float|int) -> float:
    """Return the value of x in the view. Allow relative sizing."""
    return x * (view/100)

def min_max_range(min: float|int|None, max: float|int|None, value: float|int) -> float:
    if min > max:
        raise ValueError("min must be less than max")
    
    if min is not None: 
        if value < min:
            return min
    if max is not None:
        if value > max:
            return max
    
    return value

def UV(value, resolution=1080):
    """Universal value. Allow using absolute value for the height of the window."""
    if actual_height is None or value is None:
        return value
    return (value/resolution) * actual_height

def IUV(value, resolution=1080):
    """Integer Universal value. Allow using absolute value for the height of the window."""
    return int(UV(value, resolution))