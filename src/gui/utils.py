import os.path

from PIL import Image
from customtkinter import CTkImage

PRIMARY_COLOR = "#0b7687"
PRIMARY_HOVER_COLOR = "#0a4247"

SECONDARY_COLOR = "#7f6360"
SECONDARY_HOVER_COLOR = "#524141"

LIGHT_GREEN = "#248f6d"
DARK_GREEN = "#1b7254"

COLOR_DIFFICULTY = ["#5bbc67", "#98bc5b", "#bcaf5b", "#bc8d5b", "#bc5b5b"]

FONT = "Helvetica"

EMPTY_IMAGE = CTkImage(Image.frombytes("RGBA", (1, 1), b"\x00\x00\x00\x00"))

actual_height = 0


def get_parent_path(path: str, level: int = 1) -> str:
	"""Return the parent path of the path."""
	for _ in range(level):
		path = os.path.dirname(path)
	return path


def get_ressources_path() -> str:
	"""Return the path to the ressources folder."""
	parent_path = get_parent_path(__file__, 3)
	ressources_path = os.path.join(parent_path, 'resources')
	return ressources_path


def set_height_utils(height):
	global actual_height
	actual_height = height


def v(x: float | int, view: float | int) -> float:
	"""Return the value of x in the view. Allow relative sizing."""
	return x * (view / 100)


def min_max_range(min: float | int | None, max: float | int | None, value: float | int) -> float:
	if min > max:
		raise ValueError("min must be less than max")

	if min is not None and value < min:
		return min
	if max is not None and value > max:
		return max

	return value


def uv(value, resolution=1080):
	"""Universal value. Allow using absolute value for the height of the window."""
	if actual_height is None or value is None:
		return value
	return (value / resolution) * actual_height


def iuv(value, resolution=1080):
	"""Integer Universal value. Allow using absolute value for the height of the window."""
	return int(uv(value, resolution))
