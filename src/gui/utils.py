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


def v(p: float | int, view: float | int) -> float:
	"""
	Return the value as percentage of the view (v for view).
	:param p: The percentage of the view
	:param view: The view (usually the height of the window).
	:return: The value as percentage of the view
	"""
	return p * (view / 100)


def min_max_range(min_range: float | int | None, max_range: float | int | None, value: float | int) -> float:
	if min_range > max_range:
		raise ValueError("min must be less than max")
	if min_range is not None and value < min_range:
		return min_range
	if max_range is not None and value > max_range:
		return max_range
	return value


def uv(value, resolution=1080):
	"""Universal value. Allow using absolute value for the height of the window."""
	if actual_height is None or value is None:
		return value
	return (value / resolution) * actual_height


def iuv(value, resolution=1080):
	"""Integer Universal value. Allow using absolute value for the height of the window."""
	return int(uv(value, resolution))


def get_font_style_default(width: int):
	return FONT, min_max_range(iuv(8), iuv(28), int(v(1.9, width)))


def get_font_style_title(width: int):
	return FONT, min_max_range(iuv(12), iuv(32), int(v(2.5, width))), "bold"


def normalize_title(title: str):
	"""Normalize the title of the wall."""
	if len(title) > 15:
		title_normalized = title[:13] + "..."
	else:
		title_normalized = title
	return title_normalized
