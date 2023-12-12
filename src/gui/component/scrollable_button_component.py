import os
from typing import Callable

import customtkinter as ctk
from PIL import Image

from gui.utils import SECONDARY_COLOR, SECONDARY_HOVER_COLOR, get_font_style_default, get_ressources_path, iuv, uv, \
	normalize_title, v


class ScrollableButtonComponent(ctk.CTkScrollableFrame):

	def __init__(self, master, add_button_on_click: Callable[[], None] = None, **kw):
		super().__init__(master, **kw)
		self.__init_components(add_button_on_click)
	
	def __init_components(self, add_button_on_click: Callable[[], None]):
		self.grid_columnconfigure(0, weight=1)

		self.button_list: list[ctk.CTkButton] = []
		if add_button_on_click is not None:
			self.adding_button = self.__create_adding_button(add_button_on_click)
			self.__grid_at_top(self.adding_button)
		else:
			self.adding_button = None
	
	# Load element

	def load_button_list(self, text_and_command_list: list[tuple[str, Callable[[int], None]]]):
		"""
		Load a list of button in the container.
		:param text_and_command_list: list of tuple (text, command)
		"""
		self.__remove_button_list(self.button_list)
		for index, (text, command) in enumerate(text_and_command_list):
			button = self.__create_button(text, command, index)
			self.button_list.append(button)
		self.__grid_all_button()

	def __remove_button_list(self, button_list: list[ctk.CTkButton]):
		"""Remove all buttons from the container."""
		for button in button_list:
			button.grid_forget()
			del button
		button_list.clear()

	def __create_button(self, display_text: str, on_active: Callable[[int], None], index: int):
		"""Creates a button with the given text."""

		def on_click():
			self.refresh_active_element_in_route_list(index)
			on_active(index)

		button = ctk.CTkButton(
			self,
			text = normalize_title(display_text),
			fg_color = "transparent",
			hover_color = SECONDARY_COLOR,
			border_spacing = uv(17),
			command = on_click,
			anchor = "w"
		)

		return button

	# Active element in route list
	
	def set_active_element(self, index: int):
		"""Alias for refresh_active_element_in_route_list."""
		self.refresh_active_element_in_route_list(index)

	def refresh_active_element_in_route_list(self, active_index: int):
		for button in self.button_list:
			self.__set_element_inactive_in_route_list(button=button)
		
		if self.__index_in_button_list_range(active_index):
			self.__set_element_active_in_route_list(index=active_index)

	def __set_element_active_in_route_list(self, index: int | None = None, button: ctk.CTkButton = None):
		if button is None:
			target_button = self.button_list[index]
		else:
			target_button = button

		target_button.configure(
			fg_color=SECONDARY_COLOR, hover_color=SECONDARY_HOVER_COLOR
		)

	def __set_element_inactive_in_route_list(self, index: int | None = None, button: ctk.CTkButton = None):
		if button is None:
			target_button = self.button_list[index]
		else:
			target_button = button
		
		target_button.configure(
			fg_color="transparent", hover_color=SECONDARY_HOVER_COLOR
		)

	def __index_in_button_list_range(self, index: int) -> bool:
		return index >= 0 and index < len(self.button_list)

	# Adding button

	def __create_adding_button(self, on_click: Callable[[], None]) -> ctk.CTkButton:
		get_image_button = ctk.CTkImage(
			Image.open(os.path.join(get_ressources_path(), "images", "add_button.png")), 
			size=(uv(40), uv(40))
		)
		adding_button = ctk.CTkButton(
			self, 
			text="", image = get_image_button,
			corner_radius = uv(1000), width=uv(40), height=uv(40),
			fg_color = "transparent", command = on_click
			#lambda: self.app.show_page(AddRoutePage)
		)
		return adding_button

	def __is_adding_button_exist(self):
		return hasattr(self, "adding_button") and self.adding_button is not None
	
	def show_adding_button(self):
		if self.__is_adding_button_exist():
			self.__grid_at_top(self.adding_button)
		else:
			print("Scrollable button component: adding button doesn't exist.\nPlease define argument add_button_on_click in init of this component.")

	def hide_adding_button(self):
		if self.__is_adding_button_exist():
			self.adding_button.grid_forget()
		else:
			print("Scrollable button component: adding button doesn't exist.\nPlease define argument add_button_on_click in init of this component.")

	# Utils

	def __grid_all_button(self):
		for button in self.button_list:
			button.grid(column=0, padx=uv(10), sticky="ew")

	def __ungrid_all_button(self):
		for button in self.button_list:
			button.grid_forget()

	def __grid_at_top(self, element: ctk.CTkBaseClass):
		self.__ungrid_all_button()
		element.grid(column=0, padx=iuv(10), pady= iuv(10), sticky="ew")
		self.__grid_all_button()

	# Component lifecycle

	def resize(self, width: int, height: int, frame_width: int | None = None):
		font_style_default = get_font_style_default(width, height)

		if frame_width is None:
			target_frame_width = max(uv(250), v(10, width))
		else:
			target_frame_width = frame_width

		self.configure(width=target_frame_width)

		for button in self.button_list:
			button.configure(height=v(5, height), font=font_style_default)