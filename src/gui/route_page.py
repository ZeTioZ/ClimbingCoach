"""Module for tkinter interface of route page."""
import os.path
import pickle
import tkinter as tk

import customtkinter
import numpy as np
from PIL import Image

from database.queries import route_queries
from gui.abstract.page import Page
from gui.add_route_page import AddRoutePage
from gui.app_state import AppState
from gui.utils import FONT, LIGHT_GREEN, DARK_GREEN, PRIMARY_COLOR, PRIMARY_HOVER_COLOR, SECONDARY_COLOR, \
	SECONDARY_HOVER_COLOR, COLOR_DIFFICULTY
from gui.utils import v, uv, iuv, min_max_range, get_ressources_path

state = AppState()


class RoutePage(Page):
	"""Class of the route page."""
	choose_index = 0  # page dans laquelle on est

	def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk):
		super().__init__(parent, app)

		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=7)
		self.grid_rowconfigure(0, weight=0, minsize=uv(80))
		self.grid_rowconfigure(1, weight=1)
		self.grid_rowconfigure(2, weight=0, minsize=uv(80))

		self.image_max_size = (uv(200), uv(200))  # (width, height)

		self.route_list_title = customtkinter.CTkLabel(self, text="Routes list", font=(FONT, iuv(28), "bold"))
		self.route_list_title.grid(row=0, column=0, sticky="nswe")

		self.route_list_frame = customtkinter.CTkScrollableFrame(self, width=uv(150))
		self.route_list_frame.grid(row=1, column=0, sticky="nswe")
		self.route_list_frame.grid_columnconfigure(0, weight=1)

		self.route_detail_frame = customtkinter.CTkFrame(self)
		self.route_detail_frame.grid(row=0, column=1, rowspan=2, sticky="nswe")
		self.route_detail_frame.configure(fg_color="transparent")

		self.route_detail_frame.grid_columnconfigure((0, 3), weight=3)
		self.route_detail_frame.grid_columnconfigure((1, 2), weight=1)
		self.route_detail_frame.grid_rowconfigure((0, 1, 2), weight=1)

	def set_active(self):
		"""Set the page active"""
		self.all_routes = route_queries.get_all_routes()

		if len(self.all_routes) > 0:
			for widget in self.route_detail_frame.winfo_children():
				widget.grid_forget()
			for widget in self.route_list_frame.winfo_children():
				widget.grid_forget()

			self.current_route = self.__fetch_route_detail()

			# image: np.array = pickle.loads(self.current_path["image"])
			# image_fromarray = Image.fromarray(image)

			# self.path_image = customtkinter.CTkImage(image_fromarray, size=(uv(200), uv(200)))
			self.route_label = customtkinter.CTkLabel(self.route_detail_frame, text="")
			self.route_label.grid(row=1, column=1, rowspan=1, padx=(uv(0), uv(50)))
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

			self.detail_difficulty = customtkinter.CTkFrame(self.route_detail_frame, fg_color="transparent")
			self.detail_difficulty.grid_columnconfigure((1, 2, 3, 4, 5), weight=1)
			self.detail_difficulty.grid_columnconfigure((0, 6), weight=2)
			self.detail_difficulty.grid(row=2, column=0, sticky="we", pady=(uv(50), uv(50)))

			self.difficulty: list[customtkinter.CTkFrame] = []

			for i in range(5):
				self.difficulty.append(
					customtkinter.CTkFrame(self.detail_difficulty, fg_color="green", corner_radius=uv(1000),
					                       width=uv(25),
					                       height=uv(25), border_color="white"))
				self.difficulty[i].grid(row=0, column=i + 1, padx=uv(5))

			self.__set_difficulty(self.current_route["difficulty"])

			self.route_selection_button = customtkinter.CTkButton(self.route_detail_frame, text="Select",
			                                                      command=lambda: self.selection_route())
			self.route_selection_button.grid(row=2, column=1, padx=(uv(0), uv(50)))
		# get all routes in db
		route_name_list = self.all_routes

		self.button_list: list[customtkinter.CTkButton] = []
		for route in route_name_list:
			self.route_button = self.create_button(route.name, route_name_list.index(route))
			self.button_list.append(self.route_button)

		self.user = state.get_user()
		if self.user.role == "admin":
			get_image_button = customtkinter.CTkImage(
				Image.open(os.path.join(get_ressources_path(), "images", "add_button.png")), size=(uv(40), uv(40)))
			self.create_route_button = customtkinter.CTkButton(self.route_list_frame, text="", image=get_image_button,
			                                                   corner_radius=uv(10000000), width=uv(40), height=uv(40),
			                                                   fg_color="transparent",
			                                                   command=lambda: self.app.show_page(AddRoutePage))
			self.create_route_button.grid(row=0, column=0, pady=uv(10))

	def __set_name(self, name: str):
		"""Set the name of the route."""
		self.detail_title_name.configure(text=name)

	def __set_difficulty(self, difficulty: int):
		"""Set the difficulty of the route."""

		if difficulty < 1 or difficulty > 5:
			raise ValueError("difficulty must be in [1..5]")

		for i in range(5):
			if i <= difficulty - 1:
				self.difficulty[i].configure(fg_color=COLOR_DIFFICULTY[i], border_width=0)
			else:
				self.difficulty[i].configure(fg_color="transparent", border_width=uv(2))

	def __set_description(self, description: str):
		"""Set the description of the route."""
		self.route_description.configure(state="normal")
		self.route_description.delete("0.0", "end")
		self.route_description.insert("0.0", description)
		self.route_description.configure(state="disabled")

	def __fetch_route_detail(self):
		"""Fetch the routes detail from the database."""
		return {"name": self.all_routes[self.choose_index].name,
		        "difficulty": self.all_routes[self.choose_index].difficulty,
		        "image": self.all_routes[self.choose_index].image,
		        "description": self.all_routes[self.choose_index].description
		        }

	def create_button(self, display_text, index):
		"""Creates a button with the given text."""

		is_first = index == 0

		self.button = customtkinter.CTkButton(
			self.route_list_frame,
			text=display_text,
			fg_color=SECONDARY_COLOR if self.choose_index == index else "transparent",
			hover_color=SECONDARY_COLOR,
			border_spacing=uv(17),
			command=lambda: self.show_route_detail(index),
			anchor="w"
		)

		self.button.grid(row=index + 1, column=0, padx=uv(10), sticky="ew")
		return self.button

	def selection_route(self):
		"""Select the route."""
		button_text = self.route_selection_button.cget("text")
		if button_text == "Select":
			self.route_selection_button.configure(text="Selected", fg_color=LIGHT_GREEN, hover_color=DARK_GREEN)
			state.set_route(self.choose_index)
		else:
			self.route_selection_button.configure(text="Select", fg_color=PRIMARY_COLOR, hover_color=PRIMARY_HOVER_COLOR)
			state.set_route(None)
		self.app.update_menu()

	def show_route_detail(self, wall_chosen):
		"""Shows the route detail page."""
		if not self.button_list or self.__is_already_in_tab(wall_chosen):
			return

		for button in self.button_list:
			button.configure(fg_color="transparent")

		self.choose_index = wall_chosen
		if wall_chosen == state.get_wall():
			self.__set_select_btn_active()
		self.__change_select_btn()

		self.button_list[wall_chosen].configure(fg_color=SECONDARY_COLOR, hover_color=SECONDARY_HOVER_COLOR)

		self.current_route = self.__fetch_route_detail()

		self.route_label.grid_forget()
		self.__image_loader()
		self.route_label.grid(row=1, column=1, rowspan=1, padx=(uv(0), uv(50)))

		self.__set_name(self.current_route["name"])
		self.__set_difficulty(self.current_route["difficulty"])
		self.__set_description(self.current_route["description"])

	# afficher a droite
	# self.path_label.grid_forget()
	# self.trail_label.configure(image=self.__image_loader("trail_" + str(trail_chosen+1)),size=(300, 300))
	# self.__image_loader("path_" + str(path_chosen + 1))
	# self.path_label.grid(row=1, column=1)

	def __change_select_btn(self):
		if self.__is_already_selected():
			self.__set_select_btn_active()
		else:
			self.__set_select_btn_inactive()

	def __set_select_btn_active(self):
		self.route_selection_button.configure(text="Selected", fg_color=LIGHT_GREEN, hover_color=DARK_GREEN)

	def __set_select_btn_inactive(self):
		self.route_selection_button.configure(text="Select", fg_color=PRIMARY_COLOR, hover_color=PRIMARY_HOVER_COLOR)

	def __is_already_in_tab(self, tab: int) -> bool:
		"""Return true if the page is already in the tab."""
		return tab == self.choose_index

	def __is_already_selected(self) -> bool:
		"""Return true if the page is already selected."""
		return self.choose_index == state.get_route()

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

	# def __get_image_path(self, image_name: str):
	# 	"""Return the path of the icon passed in parameter."""
	# 	parent_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
	# 	path = os.path.join(parent_path, 'resources', 'images', image_name)
	# 	if os.path.exists(path):
	# 		return path
	# 	return os.path.join(parent_path, 'resources', 'images', 'trail_1.jpg')

	def on_size_change(self, width, height):
		super().on_size_change(width, height)

		if len(self.all_routes) > 0:

			max_dim_size = min_max_range(uv(75), uv(1000), v(22, width))
			self.image_max_size = (max_dim_size, max_dim_size)

			if hasattr(self, "route_image"):
				image_size = self.__get_image_ration_safe_by_size(self.route_image.cget("size"))
				self.route_image.configure(size=image_size)
				self.route_label.configure(height=iuv(image_size[1]), width=iuv(image_size[0]))

			font_style_default = (FONT, min_max_range(iuv(8), iuv(28), int(v(1.9, width))))
			font_style_title = (FONT, min_max_range(iuv(12), iuv(32), int(v(2.5, width))), "bold")

			self.route_list_title.configure(font=font_style_title)
			self.route_selection_button.configure(height=v(5, height), width=max_dim_size, font=font_style_default)
			self.route_description.configure(font=font_style_default)

			# TODO: change diff image size
			size_difficulty = min_max_range(uv(15), uv(100), v(2.5, width))
			for i in range(5):
				self.difficulty[i].configure(width=size_difficulty, height=size_difficulty)

			for button in self.button_list:
				button.configure(height=v(5, height), width=max_dim_size, font=font_style_default)

	def get_name(self):
		return "Route selection"

# # Overwriting section
# def set_active(self):
# 	super().set_active()

# 	self.__change_select_btn()
