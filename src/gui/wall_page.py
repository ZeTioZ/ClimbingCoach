"""Module for tkinter interface of wall page."""
import os.path
import pickle
from typing import Callable
import numpy as np
import tkinter as tk
import customtkinter

from PIL import Image

from gui.create_wall import CreateWall
from gui.abstract.page import Page
from gui.app_state import AppState
from gui.utils import FONT, LIGHT_GREEN, DARK_GREEN, PRIMARY_COLOR, PRIMARY_HOVER_COLOR, SECONDARY_COLOR, \
	SECONDARY_HOVER_COLOR, COLOR_DIFFICULTY, get_font_style_default, get_font_style_title, normalize_title
from gui.utils import v, uv, iuv, min_max_range, get_ressources_path
from database.queries import wall_queries
from database.models.wall import Wall
from gui.component.image_component import ImageComponent
from gui.component.difficulty_component import DifficultyComponent
from database.models.route import Route
from gui.component.scrollable_button_component import ScrollableButtonComponent

state = AppState()


class WallPage(Page):
	"""Class of the wall page."""

	def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk):
		super().__init__(parent, app)

		self.active_id = 0

		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=7)
		self.grid_rowconfigure(0, weight=0, minsize=uv(80))
		self.grid_rowconfigure(1, weight=1)

		self.image_max_size = (uv(200), uv(200))  # (width, height)

		self.element_list_component = self.__create_scrollable_button_component(lambda: self.app.show_page(CreateWall))
		self.element_list_component.grid(row=1, column=0, sticky="nswe")

		self.wall_list_title = customtkinter.CTkLabel(self, text="Walls list", font=(FONT, iuv(28), "bold"))
		self.wall_list_title.grid(row=0, column=0, sticky="nswe")

		self.detail_frame = self.__create_description_elements()

	def __is_user_admin(self) -> bool:
		"""Return true if the user is admin."""
		return state.get_user().role == "admin"

	def __show_user_role_content(self):
		if self.__is_user_admin():
			self.element_list_component.show_adding_button()
		else:
			self.element_list_component.hide_adding_button()

	def selection_wall(self):
		"""Select the wall."""
		button_text = self.selection_button.cget("text")
		if button_text == "Select":
			self.selection_button.configure(
				text="Selected", fg_color=LIGHT_GREEN, 
				hover_color=DARK_GREEN
			)
			state.set_wall(self.all_walls[self.active_id])
		else:
			self.selection_button.configure(
				text="Select", fg_color=PRIMARY_COLOR,
				hover_color=PRIMARY_HOVER_COLOR
			)
			state.set_wall(None)
		self.app.update_menu()

	def __image_loader(self, image_to_load) -> np.ndarray:
		"""Loads an image from the given route."""
		image: np.ndarray = pickle.loads(image_to_load)
		return image

	# Scrollable button component

	def __create_scrollable_button_component(self, add_button_on_click: Callable[[], None] = None):
		"""Initialize the scrollable button component."""
		element_list_frame = ScrollableButtonComponent(self, add_button_on_click, width=uv(150))
		return element_list_frame

	def __refresh_scrollable_button_component(self):
		if self.all_walls is not None:
			self.element_list_component.load_button_list([(wall.name, lambda index: self.__show_detail(index)) for wall in self.all_walls])

	# Life cycle
	
	def get_name(self):
		return "Wall selection"
	
	def set_active(self):
		"""Set the page active."""
		self.all_walls = self.__load_wall()
		self.__show_user_role_content()
		self.refresh_description()
		self.__refresh_scrollable_button_component()
		self.element_list_component.set_active_element(self.active_id)

	def on_size_change(self, width, height):
		super().on_size_change(width, height)
		self.element_list_component.resize(width, height)
		self.detail_component_resize(width, height)

		font_style_title = get_font_style_title(width, height)
		self.wall_list_title.configure(font=font_style_title)

	# DB

	def __load_wall(self) -> list[Wall]:
		"""Load the walls from the database."""
		return wall_queries.get_all_walls()

	# =====================
	# Description component
	# =====================

	def __create_description_elements(self):

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

		self.selection_button = customtkinter.CTkButton(
			detail_frame, text="Select",
			command = lambda: self.selection_wall()
		)
		self.selection_button.grid(row=2, column=1, padx=(uv(0), uv(50)))

	# Show detail

	def __show_detail(self, active_id: int):
		"""Shows the route detail page."""
		self.active_id = active_id

		self.__change_select_btn()
	
		self.current_elem = self.__fetch_detail()

		self.set_image(self.__image_loader(self.current_elem["image"]))
		self.set_name(self.current_elem["name"])
		self.set_difficulty(self.current_elem["difficulty"])
		self.set_description(self.current_elem["description"])

	def __change_select_btn(self):
		if self.__is_selected():
			self.__set_select_btn_active()
		else:
			self.__set_select_btn_inactive()

	def __is_selected(self) -> bool:
		"""Return true if the page is already selected."""
		current_elem = state.get_wall()
		list_name = [wall.name for wall in self.all_walls]
		return current_elem is not None\
				and current_elem.name in list_name\
				and self.active_id == list_name.index(current_elem.name)

	def __set_select_btn_active(self):
		self.selection_button.configure(text="Selected", fg_color=LIGHT_GREEN, hover_color=DARK_GREEN)

	def __set_select_btn_inactive(self):
		self.selection_button.configure(text="Select", fg_color=PRIMARY_COLOR, hover_color=PRIMARY_HOVER_COLOR)

	# Fetch detail

	def __fetch_detail(self):
		"""Fetch the routes detail from the database."""
		return {"name": self.all_walls[self.active_id].name,
		        "difficulty": self.all_walls[self.active_id].difficulty,
		        "image": self.all_walls[self.active_id].image,
		        "description": self.all_walls[self.active_id].description
		        }

	# Set detail

	def set_detail(self, element: Wall | Route):
		"""Set the route detail."""
		self.set_name(element.name)
		self.set_difficulty(element.difficulty)
		self.set_description(element.description)

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

	# Life cycle

	def refresh_description(self):
		"""Set the page active"""
		if self.active_id is not None:
			self.__show_detail(self.active_id)
	
	def detail_component_resize(self, width: int, height: int):

		self.image_componant.resize(width, height)
		self.difficulty_component.resize(width, height)
		
		font_style_default = get_font_style_default(width, height)
		self.description.configure(font=font_style_default)
		self.selection_button.configure(height=v(5, height), width=v(22, width), font=font_style_default)

	
