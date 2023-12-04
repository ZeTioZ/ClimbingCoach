from tkinter import Event
from typing import Callable

import numpy as np
from PIL import Image

from enums.event_type import EventType
from enums.flux_reader_event_type import FluxReaderEventType
from events.flux_reader_event import FluxReaderEvent
from gui.component.interactive_image import InteractiveImage
from interfaces.listener import Listener
from objects.box import Box
from objects.route import Route
from database.queries.route_queries import create_route, get_route_by_name
from utils.click_utils import find_selected_hold
from utils.draw_utils import box_visualizer, draw_path, path_box_visualizer
from utils.serializer_utils import deserialize_route


class ImageDriver(Listener):
	image: np.ndarray = None

	def __init__(self, i_image: InteractiveImage):
		super().__init__([
			FluxReaderEventType.HOLDS_PROCESSED_EVENT
		])

		self.i_image = i_image
		self.i_image.bind_right_click(self.click_right)
		self.i_image.bind_left_click(self.click_left)
		self.holds: list[Box] = []
		self.route: Route = Route()

		print(f"Image driver created: said {id(self)}")

	def get_interactive_image(self):
		"""Return the interactive image."""
		return self.i_image

	def draw_holds_and_path(self, image: np.ndarray | None = None, holds: list[Box] | None = None) -> Image:
		"""Draw the holds on the image."""
		if image is None:
			image = self.image
		if holds is None:
			holds = self.holds

		drawn_image = box_visualizer(image, holds)
		drawn_image = path_box_visualizer(drawn_image, self.route.get_route())
		drawn_image = draw_path(drawn_image, self.route.get_route())

		return Image.fromarray(drawn_image)

	def route_add_box(self, box: Box):
		"""Add a box to the path."""
		print(f"Add box to route {box}: said {id(self)}")
		self.route.add_step(box)

	def route_remove_box(self, box: Box):
		"""Remove a box from the path."""
		self.route.remove_step(box)
		if self.route.is_hold_in_route(box):
			self.route.remove_step(box)
		else:
			print(f"The box is not in the route: {box}: said {id(self)}")

	def route_remove_box_by_index(self, index: int):
		"""Remove a box from the path."""
		if index < len(self.route.get_route()):
			self.route_remove_box(self.route.get_route()[index])
		else:
			print(f"The index is out of range: {index} > {len(self.route.get_route())}: said {id(self)}")
			print(f"Route: {self.route.get_route()}")

	def route_clear(self):
		"""Clear the path."""
		self.route.clear()
		self.display_holds()

	def route_set_name(self, name: str):
		"""Set the name of the path."""
		self.route.set_name(name)
	
	def load_route(self, name: str):
		"""Load the path."""
		route_db = get_route_by_name(name)
		self.route = deserialize_route(route_db.holds)
		self.display_holds()

	def save_route(self):
		"""Save the path."""
		if self.route.is_name_set():
			create_route(self.route, "", 2)
		else:
			raise AttributeError("The name of the route is not set.")

	def click_right(self, event):
		"""Called when the image is clicked."""
		selected_box = self.__click(event)
		if selected_box is not None and self.route.is_hold_in_route(selected_box):
			self.route_remove_box(selected_box)
			self.i_image.change_image(self.draw_holds_and_path())
			if self.__click_callback is not None:
				self.__click_callback()

	def click_left(self, event):
		"""Called when the image is clicked."""
		selected_box = self.__click(event)
		if selected_box is not None:
			self.route_add_box(selected_box)
			self.i_image.change_image(self.draw_holds_and_path())
			if self.__click_callback is not None:
				self.__click_callback()

	def __click(self, event) -> Box | None:
		"""Called when the image is clicked."""
		if self.image is None:
			return
		default_x = int(self.i_image.default_size_width * event.x / self.i_image.winfo_width())
		default_y = int(self.i_image.default_size_height * event.y / self.i_image.winfo_height())
		return find_selected_hold(self.holds, default_x, default_y)

	__click_callback = None

	def bind_click(self, callback: Callable[[None], None]):
		self.__click_callback = callback

	# LISTENER
	def update(self, event: Event, event_types: [EventType], *args, **kwargs):
		"""Called when the event notify the observer."""
		if not isinstance(event, FluxReaderEvent):
			return

		if FluxReaderEventType.HOLDS_PROCESSED_EVENT in event_types:
			self.image = args[1]
			self.__on_hold_received(args[0], args[1])

		if FluxReaderEventType.GET_FRAME_EVENT in event_types:
			self.image = args[0]

	def __on_hold_received(self, holds: list[Box], frame: np.ndarray):
		"""Called when the holds are received."""
		self.holds = holds
		self.image = frame
		self.display_holds(holds=holds)

	# UTILS
	def change_image(self, holds: list[Box] = None, image: np.ndarray = None):
		"""Change the image."""
		if holds is None:
			holds = self.holds
		self.i_image.change_image(self.draw_holds_and_path(self.image, holds))

	#TODO : update holds
	#def __refresh_holds(self)
