"""Module for tkinter interface of route page."""
import os.path
import pickle
import tkinter as tk
from typing import Callable

import customtkinter
import numpy as np
from PIL import Image

from database.queries import route_queries
from gui.abstract.page import Page
from gui.add_route_page import AddRoutePage
from gui.component.scrollable_button_component import ScrollableButtonComponent
from gui.component.difficulty_component import DifficultyComponent
from gui.app_state import AppState
from gui.utils import FONT, LIGHT_GREEN, DARK_GREEN, PRIMARY_COLOR, PRIMARY_HOVER_COLOR, SECONDARY_COLOR, \
	SECONDARY_HOVER_COLOR, COLOR_DIFFICULTY
from gui.utils import v, uv, iuv, min_max_range, get_ressources_path, get_font_style_default, get_font_style_title
from database.models.route import Route

state = AppState()


class RoutePage(Page):
	"""Class of the route page."""
	active_route_id = 0  # page dans laquelle on est

	def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk):
		super().__init__(parent, app)

		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=7)
		self.grid_rowconfigure(0, weight=0, minsize=uv(80))
		self.grid_rowconfigure(1, weight=1)
		# self.grid_rowconfigure(2, weight=0, minsize=uv(80))

		self.image_max_size = (uv(200), uv(200))  # (width, height)

		self.route_list_title = customtkinter.CTkLabel(self, text="Routes list", font=(FONT, iuv(28), "bold"))
		self.route_list_title.grid(row=0, column=0, sticky="nswe")

		self.route_list_component = self.__create_scrollable_button_component(lambda: self.app.show_page(AddRoutePage))
		self.route_list_component.grid(row=1, column=0, sticky="nswe")
		

		self.route_detail_frame = customtkinter.CTkFrame(self)
		self.route_detail_frame.grid(row=0, column=1, rowspan=2, sticky="nswe")
		self.route_detail_frame.configure(fg_color="transparent")

		self.route_detail_frame.grid_columnconfigure((0, 3), weight=3)
		self.route_detail_frame.grid_columnconfigure((1, 2), weight=1)
		self.route_detail_frame.grid_rowconfigure((0, 1, 2), weight=1)

	def __old_is_active(self):
		"""Set the page active"""
		self.all_routes = route_queries.get_all_routes()

		if len(self.all_routes) > 0:
			for widget in self.route_detail_frame.winfo_children():
				widget.grid_forget()
			for widget in self.route_list_component.winfo_children():
				widget.grid_forget()

			self.current_route = self.__fetch_route_detail()

			# image: np.array = pickle.loads(self.current_path["image"])
			# image_fromarray = Image.fromarray(image)

			# self.path_image = customtkinter.CTkImage(image_fromarray, size=(uv(200), uv(200)))
			self.route_label = customtkinter.CTkLabel(self.route_detail_frame, text="") #
			self.route_label.grid(row=1, column=1, rowspan=1, padx=(uv(0), uv(50))) #
			self.__image_loader()

			self.detail_title_name = customtkinter.CTkLabel(self.route_detail_frame, text=self.current_route["name"],
			                                                font=(FONT, iuv(32), "bold"), fg_color=SECONDARY_COLOR,
			                                                corner_radius=20, width=uv(350))
			self.detail_title_name.grid(row=0, column=0, columnspan=2, sticky="", ipady=uv(10))

			self.route_description = customtkinter.CTkTextbox(self.route_detail_frame, font=(FONT, iuv(16)), wrap=tk.WORD,
			                                                  fg_color="transparent")
			self.route_description.insert("0.0", self.current_route["description"])
			self.route_description.configure(state="disabled")
			self.route_description.grid(row=1, column=0, sticky="nswe", pady=(uv(50), uv(0)), padx=(uv(50), uv(0)))

			self.difficulty_component = self.__create_difficulty_component()
			self.difficulty_component.grid(row=2, column=0, sticky="we", pady=(uv(50), uv(50)))
			self.difficulty_component.set_difficulty(self.current_route["difficulty"])

			self.route_selection_button = customtkinter.CTkButton(self.route_detail_frame, text="Select",
			                                                      command=lambda: self.selection_route())
			self.route_selection_button.grid(row=2, column=1, padx=(uv(0), uv(50)))
		
	def __init_description_elements(self):
		self.route_label = customtkinter.CTkLabel(self.route_detail_frame, text="")
		self.route_label.grid(row=1, column=1, rowspan=1, padx=(uv(0), uv(50)))

		self.detail_title_name = customtkinter.CTkLabel(
			self.route_detail_frame, text="",
			font=(FONT, iuv(32), "bold"), fg_color=SECONDARY_COLOR,
			corner_radius=20, width=uv(350)
		)
		self.detail_title_name.grid(row=0, column=0, columnspan=2, ipady=uv(10))

		self.route_description = customtkinter.CTkTextbox(
			self.route_detail_frame, font=(FONT, iuv(16)), wrap=tk.WORD,
			fg_color="transparent", state="disabled"
		)
		self.route_description.grid(
			row=1, column=0, sticky="nswe", 
			pady=(uv(50), uv(0)), padx=(uv(50), uv(0))
		)

		self.__init_difficulty_component()

		self.route_selection_button = customtkinter.CTkButton(
			self.route_detail_frame, text="Select",
			command = 	lambda: self.selection_route()
		)
		self.route_selection_button.grid(row=2, column=1, padx=(uv(0), uv(50)))

	def __set_route_detail(self, route: Route):
		"""Set the route detail."""
		self.__set_name(route.name)
		self.difficulty_component.set_difficulty(route.difficulty)
		self.__set_description(route.description)

	def __set_name(self, name: str):
		"""Set the name of the route."""
		normalized_title = self.__normalize_title(name)
		self.detail_title_name.configure(text=normalized_title)

	def __set_description(self, description: str):
		"""Set the description of the route."""
		self.route_description.configure(state="normal")
		self.route_description.delete("0.0", "end")
		self.route_description.insert("0.0", description)
		self.route_description.configure(state="disabled")

	def __fetch_route_detail(self):
		"""Fetch the routes detail from the database."""
		return {"name": self.all_routes[self.active_route_id].name,
		        "difficulty": self.all_routes[self.active_route_id].difficulty,
		        "image": self.all_routes[self.active_route_id].image,
		        "description": self.all_routes[self.active_route_id].description
		        }

	def selection_route(self):
		"""Select the route."""
		button_text = self.route_selection_button.cget("text")
		if button_text == "Select":
			self.route_selection_button.configure(text="Selected", fg_color=LIGHT_GREEN, hover_color=DARK_GREEN)
			state.set_route(route_queries.get_route_by_name(self.all_routes[self.active_route_id].name))
		else:
			self.route_selection_button.configure(text="Select", fg_color=PRIMARY_COLOR, hover_color=PRIMARY_HOVER_COLOR)
			state.set_route(None)
		self.app.update_menu()

	def __image_loader(self):
		"""Loads an image from the given route."""
		image: np.array = pickle.loads(self.current_route["image"])
		image_fromarray = Image.fromarray(image)

		image_size = self.__get_image_ration_safe(image_fromarray)

		self.route_image = customtkinter.CTkImage(image_fromarray,
		                                          size=image_size)
		self.route_label.configure(image=self.route_image)

	def __get_image_ration_safe(self, image: Image.Image):
		raw_size = image.size
		return self.__get_image_ration_safe_by_size(raw_size)

	def __get_image_ration_safe_by_size(self, size: tuple[int, int]):
		if size[0] > size[1]:
			rate = self.image_max_size[0] / size[0]
			image_size = (size[0] * rate, size[1] * rate)
		else:
			rate = self.image_max_size[1] / size[1]
			image_size = (size[0] * rate, size[1] * rate)

		return image_size

	def __is_already_in_tab(self, tab: int) -> bool:
		"""Return true if the page is already in the tab."""
		return tab == self.active_route_id

	def __is_user_admin(self) -> bool:
		"""Return true if the user is admin."""
		return state.get_user().role == "admin"

	def __show_user_role_content(self):
		if self.__is_user_admin():
			self.route_list_component.show_adding_button()
		else:
			self.route_list_component.hide_adding_button()

	# Scrollable button component

	def __create_scrollable_button_component(self, add_button_on_click: Callable[[], None] = None):
		"""Initialize the scrollable button component."""
		route_list_frame = ScrollableButtonComponent(self, add_button_on_click, width=uv(150))
		return route_list_frame

	def __refresh_scrollable_button_component(self):
		route_list = self.all_routes
		self.route_list_component.load_button_list([(route.name, lambda index: self.__show_route_detail(index)) for route in route_list])

	# Difficulty component

	def __create_difficulty_component(self):
		difficulty_component = DifficultyComponent(self.route_detail_frame)
		return difficulty_component

	# Page lifecycle

	def set_active(self):
		"""Set the page active"""
		self.__old_is_active()
		self.__show_user_role_content()
		self.__refresh_scrollable_button_component()
		self.route_list_component.set_active_element(self.active_route_id)

	def get_name(self):
		return "Route selection"

	def on_size_change(self, width, height):
		super().on_size_change(width, height)
		self.route_list_component.resize(width, height)

		if len(self.all_routes) > 0:

			max_dim_size = min_max_range(uv(75), uv(1000), v(22, width))
			self.image_max_size = (max_dim_size, max_dim_size)

			if hasattr(self, "route_image"):
				image_size = self.__get_image_ration_safe_by_size(self.route_image.cget("size"))
				self.route_image.configure(size=image_size)
				self.route_label.configure(height=iuv(image_size[1]), width=iuv(image_size[0]))

			font_style_default = get_font_style_default(width, height)
			font_style_title = get_font_style_title(width, height)

			self.route_list_title.configure(font=font_style_title)
			self.route_selection_button.configure(height=v(5, height), width=max_dim_size, font=font_style_default)
			self.route_description.configure(font=font_style_default)

			self.difficulty_component.resize(width, height)

			# self.detail_title_name.configure(font=font_style_title)

	# DB

	def __load_routes(self):
		"""Load the routes from the database."""
		self.all_routes = route_queries.get_all_routes()

	# Utils

	def __normalize_title(self, title: str):
		"""Normalize the title of the wall."""
		if len(title) > 15:
			title_normalized = title[:13] + "..."
		else:
			title_normalized = title
		return title_normalized

	# =====================
	# Description component
	# =====================

	def __show_route_detail(self, active_route_id: int):
		"""Shows the route detail page."""
		if not self.__is_already_in_tab(active_route_id):
			self.active_route_id = active_route_id

			self.__change_select_btn()
		
			self.current_route = self.__fetch_route_detail()

			self.route_label.grid_forget()
			self.__image_loader()
			self.route_label.grid(row=1, column=1, rowspan=1, padx=(uv(0), uv(50)))

			self.__set_name(self.current_route["name"])
			self.difficulty_component.set_difficulty(self.current_route["difficulty"])
			self.__set_description(self.current_route["description"])

	def __is_selected(self) -> bool:
		"""Return true if the page is already selected."""
		current_route = state.get_route()
		list_name = [route.name for route in self.all_routes]
		return current_route is not None\
				and current_route.name in list_name\
				and self.active_route_id == list_name.index(current_route.name)

	def __change_select_btn(self):
		if self.__is_selected():
			self.__set_select_btn_active()
		else:
			self.__set_select_btn_inactive()

	def __set_select_btn_active(self):
		self.route_selection_button.configure(text="Selected", fg_color=LIGHT_GREEN, hover_color=DARK_GREEN)

	def __set_select_btn_inactive(self):
		self.route_selection_button.configure(text="Select", fg_color=PRIMARY_COLOR, hover_color=PRIMARY_HOVER_COLOR)
