"""Module for tkinter interface of route page."""
import pickle
import tkinter as tk
import os.path
from typing import Callable

import customtkinter
import numpy as np
from PIL import Image

from database.models.route import Route
from database.queries import route_queries
from gui.abstract.page import Page
from gui.add_route_page import AddRoutePage
from gui.app_state import AppState
from gui.component.difficulty_component import DifficultyComponent
from gui.component.image_component import ImageComponent
from gui.component.scrollable_button_component import ScrollableButtonComponent
from gui.utils import FONT, LIGHT_GREEN, DARK_GREEN, PRIMARY_COLOR, PRIMARY_HOVER_COLOR, SECONDARY_COLOR, \
	normalize_title, get_ressources_path
from gui.utils import v, uv, iuv, get_font_style_default, get_font_style_title

state = AppState()


class RoutePage(Page):
	"""Class of the route page."""

	def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk):
		super().__init__(parent, app)

		self.active_route_id = 0

		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=7)
		self.grid_rowconfigure(0, weight=0, minsize=uv(80))
		self.grid_rowconfigure(1, weight=1)

		self.image_max_size = (uv(200), uv(200))  # (width, height)

		self.route_list_title = customtkinter.CTkLabel(self, text="Routes list", font=(FONT, iuv(28), "bold"))
		self.route_list_title.grid(row=0, column=0, sticky="nswe")

		self.route_list_component = self.__create_scrollable_button_component(lambda: self.app.show_page(AddRoutePage))
		self.route_list_component.grid(row=1, column=0, sticky="nswe")

		self.detail_frame = self.__create_description_elements()

	def selection_route(self):
		"""Select the route."""
		button_text = self.route_selection_button.cget("text")
		if button_text == "Select":
			self.route_selection_button.configure(text="Selected", fg_color=LIGHT_GREEN, hover_color=DARK_GREEN)
			state.set_route(route_queries.get_route_by_name(self.all_routes[self.active_route_id].name))
		else:
			self.route_selection_button.configure(text="Select", fg_color=PRIMARY_COLOR,
			                                      hover_color=PRIMARY_HOVER_COLOR)
			state.set_route(None)
		self.app.update_menu()

	def __is_user_admin(self) -> bool:
		"""Return true if the user is admin."""
		return state.get_user().role == "admin"

	def __show_user_role_content(self):
		if self.__is_user_admin():
			self.route_list_component.show_adding_button()
		else:
			self.route_list_component.hide_adding_button()

	def __image_loader(self, image_to_load) -> np.ndarray:
		"""Loads an image from the given route."""
		image: np.ndarray = pickle.loads(image_to_load)
		return image

	# Scrollable button component

	def __create_scrollable_button_component(self, add_button_on_click: Callable[[], None] = None):
		"""Initialize the scrollable button component."""
		route_list_frame = ScrollableButtonComponent(self, add_button_on_click, width=uv(150))
		return route_list_frame

	def __refresh_scrollable_button_component(self):
		if self.all_routes is not None:
			self.route_list_component.load_button_list(
				[(route.name, lambda index: self.__show_route_detail(index)) for route in self.all_routes])

	# Page lifecycle

	def set_active(self):
		"""Set the page active"""
		self.all_routes = self.__load_routes()
		self.__show_user_role_content()
		self.refresh_description()
		self.__refresh_scrollable_button_component()
		self.route_list_component.set_active_element(self.active_route_id)

	def get_name(self):
		return "Route selection"

	def on_size_change(self, width, height):
		super().on_size_change(width, height)
		self.route_list_component.resize(width, height)
		self.detail_component_resize(width, height)

		font_style_title = get_font_style_title(width)
		self.route_list_title.configure(font=font_style_title)

	# DB

	def __load_routes(self) -> list[Route]:
		"""Load the routes from the database."""
		return route_queries.get_all_routes()
	
	# Delete

	def delete_route(self):
		"""Delete the route."""
		route_queries.delete_route_by_name(self.all_routes[self.active_route_id].name)
		self.all_routes = self.__load_routes()
		self.__refresh_scrollable_button_component()
		self.refresh_description()

	# =====================
	# Description component
	# =====================

	def __create_description_elements(self) -> customtkinter.CTkFrame:

		detail_frame = customtkinter.CTkFrame(self)
		detail_frame.grid(row=0, column=1, rowspan=2, sticky="nswe")
		detail_frame.configure(fg_color="transparent")

		detail_frame.grid_columnconfigure((0, 3), weight=3)
		detail_frame.grid_columnconfigure((1, 2), weight=1)

		detail_frame.grid_rowconfigure((0, 1, 2), weight=1)

		self.image_componant = ImageComponent(detail_frame)
		self.image_componant.grid(row=1, column=1, rowspan=1, padx=(uv(0), uv(50)))

		self.detail_title_name = customtkinter.CTkLabel(
			detail_frame, text="",
			font=(FONT, iuv(32), "bold"), fg_color=SECONDARY_COLOR,
			corner_radius=20, width=uv(350)
		)
		self.detail_title_name.grid(row=0, column=0, columnspan=2, ipady=uv(10))

		self.description = customtkinter.CTkTextbox(
			detail_frame, font=(FONT, iuv(16)), wrap=tk.WORD,
			fg_color="transparent", state="disabled"
		)
		self.description.grid(
			row=1, column=0, sticky="nswe",
			pady=(uv(50), uv(0)), padx=(uv(50), uv(0))
		)

		self.difficulty_component = DifficultyComponent(detail_frame)
		self.difficulty_component.grid(row=2, column=0, sticky="we", pady=(uv(50), uv(50)))

		self.route_selection_button = customtkinter.CTkButton(
			detail_frame, text="Select",
			command=lambda: self.selection_route()
		)
		self.route_selection_button.grid(row=2, column=1, padx=(uv(0), uv(20)))

		bin_img = customtkinter.CTkImage(Image.open(os.path.join(get_ressources_path(), "images", "bin.png")),
								   			size=(uv(30), uv(30)))
		self.delete_button = customtkinter.CTkButton(
			detail_frame, 
			text="",
			image=bin_img,
			width=uv(30),
			command= self.delete_route
		)
		self.delete_button.grid(row=2, column=2, padx=(uv(0), uv(50)))

		return detail_frame

	# Show detail

	def __show_route_detail(self, active_route_id: int):
		"""Shows the route detail page."""
		self.active_route_id = active_route_id

		self.__change_select_btn()

		self.current_route = self.__fetch_route_detail()

		self.set_image(self.__image_loader(self.current_route["image"]))
		self.set_name(self.current_route["name"])
		self.set_difficulty(self.current_route["difficulty"])
		self.set_description(self.current_route["description"])

	def __change_select_btn(self):
		if self.__is_selected():
			self.__set_select_btn_active()
		else:
			self.__set_select_btn_inactive()

	def __is_selected(self) -> bool:
		"""Return true if the page is already selected."""
		current_route = state.get_route()
		list_name = [route.name for route in self.all_routes]
		return current_route is not None \
			and current_route.name in list_name \
			and self.active_route_id == list_name.index(current_route.name)

	def __set_select_btn_active(self):
		self.route_selection_button.configure(text="Selected", fg_color=LIGHT_GREEN, hover_color=DARK_GREEN)

	def __set_select_btn_inactive(self):
		self.route_selection_button.configure(text="Select", fg_color=PRIMARY_COLOR, hover_color=PRIMARY_HOVER_COLOR)

	# Fetch detail

	def __fetch_route_detail(self):
		"""Fetch the routes detail from the database."""
		return {"name": self.all_routes[self.active_route_id].name,
		        "difficulty": self.all_routes[self.active_route_id].difficulty,
		        "image": self.all_routes[self.active_route_id].image,
		        "description": self.all_routes[self.active_route_id].description
		        }

	# Set detail

	def set_route_detail(self, route: Route):
		"""Set the route detail."""
		self.set_name(route.name)
		self.set_difficulty(route.difficulty)
		self.set_description(route.description)

	def set_name(self, name: str):
		"""Set the name of the route."""
		normalized_title = normalize_title(name)
		self.detail_title_name.configure(text=normalized_title)

	def set_description(self, content: str):
		"""Set the description of the route."""
		self.description.configure(state="normal")
		self.description.delete("0.0", "end")
		self.description.insert("0.0", content)
		self.description.configure(state="disabled")

	def set_difficulty(self, difficulty: int):
		self.difficulty_component.set_difficulty(difficulty)

	def set_image(self, image: Image.Image | np.ndarray):
		self.image_componant.set_image(image)

	# Lifecycle

	def refresh_description(self):
		"""Set the page active"""
		if isinstance(self.active_route_id, int) and len(self.all_routes) > self.active_route_id >= 0:
			self.__show_route_detail(self.active_route_id)

	def detail_component_resize(self, width: int, height: int):
		self.image_componant.resize(width, height)
		self.difficulty_component.resize(width, height)

		font_style_default = get_font_style_default(width)
		self.description.configure(font=font_style_default)
		self.route_selection_button.configure(height=v(5, height), width=v(22, width), font=font_style_default)
		self.delete_button.configure(height=v(5, height), width=v(5, width), font=font_style_default)
		self.delete_button.cget("image").configure(size=(v(2, width), v(2, width)))

