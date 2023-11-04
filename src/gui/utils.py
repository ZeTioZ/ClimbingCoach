PRIMARY_COLOR = "#0b7687"
PRIMARY_HOVER_COLOR = "#0a4247"

SECONDARY_COLOR = "#7f6360"
SECONDARY_HOVER_COLOR = "#524141"

LIGHT_GREEN = "#248f6d"
DARK_GREEN = "#1b7254"

def v(x: float|int, view: float|int) -> float:
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