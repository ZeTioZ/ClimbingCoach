"""Module for tkinter interface of trail page."""
import os.path
import tkinter as tk

import customtkinter
from PIL import Image

from gui.abstract.page import Page
from gui.app_state import AppState
from gui.utils import FONT, LIGHT_GREEN, DARK_GREEN, PRIMARY_COLOR, PRIMARY_HOVER_COLOR, SECONDARY_COLOR, \
	SECONDARY_HOVER_COLOR, COLOR_DIFFICULTY
from gui.utils import v, uv, iuv, min_max_range

state = AppState()

RID_TITLE = 1
RID_DESCR = 2
RID_DIFFICULTY = 3

CID_LEFT = 1
CID_RIGHT = 2


class TrailPage(Page):
	"""Class of the trail page."""
	choose_index = 0  # Current page we're in

	def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk):
		super().__init__(parent, app)

		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=7)
		self.grid_rowconfigure(0, weight=0, minsize=uv(80))
		self.grid_rowconfigure(1, weight=1)

		self.trail_list_frame = customtkinter.CTkScrollableFrame(self, width=uv(150))
		self.trail_list_frame.grid(row=1, column=0, sticky="nswe")
		self.trail_list_frame.grid_columnconfigure(0, weight=1)

		self.trail_list_title = customtkinter.CTkLabel(self, text="Trail list", font=(FONT, iuv(28), "bold"))
		self.trail_list_title.grid(row=0, column=0, sticky="nswe")

		self.trail_detail_frame = customtkinter.CTkFrame(self)
		self.trail_detail_frame.grid(row=0, column=1, rowspan=2, sticky="nswe")
		self.trail_detail_frame.configure(fg_color="transparent")

		self.trail_detail_frame.grid_columnconfigure((CID_RIGHT, CID_LEFT), weight=3)
		self.trail_detail_frame.grid_columnconfigure((0, 3), weight=1)
		self.trail_detail_frame.grid_rowconfigure((0, 4), weight=0)
		self.trail_detail_frame.grid_rowconfigure((RID_TITLE, RID_DIFFICULTY), weight=1)
		self.trail_detail_frame.grid_rowconfigure(RID_DESCR, weight=3)

		current_trail = self.__fletch_trail_detail()

		self.trail_image = customtkinter.CTkImage(Image.open(self.__get_trail_image_path(current_trail["image"])),
		                                          size=(uv(200), uv(200)))
		self.trail_label = customtkinter.CTkLabel(self.trail_detail_frame, text="", image=self.trail_image)
		self.trail_label.grid(row=RID_DESCR, rowspan=1, column=CID_RIGHT, sticky="we")

		self.trail_selection_button = customtkinter.CTkButton(self.trail_detail_frame, text="Select",
		                                                      command=lambda: self.selection_trail())
		self.trail_selection_button.grid(row=RID_DIFFICULTY, column=CID_RIGHT, sticky="n")

		self.detail_title_name = customtkinter.CTkLabel(self.trail_detail_frame, text=current_trail["name"],
		                                                font=(FONT, iuv(32), "bold"), fg_color=SECONDARY_COLOR,
		                                                corner_radius=20, width=uv(350))
		self.detail_title_name.grid(row=RID_TITLE, column=CID_LEFT, columnspan=2, sticky="", ipady=uv(10))

		self.detail_description = customtkinter.CTkTextbox(self.trail_detail_frame, font=(FONT, iuv(16)), wrap=tk.WORD,
		                                                   fg_color="transparent")
		self.detail_description.insert(tk.END, current_trail["description"])
		self.detail_description.configure(state=tk.DISABLED)
		self.detail_description.grid(row=RID_DESCR, column=CID_LEFT, sticky="nswe", pady=(uv(50), uv(0)))

		self.detail_difficulty = customtkinter.CTkFrame(self.trail_detail_frame, fg_color="transparent")
		self.detail_difficulty.grid_columnconfigure((1, 2, 3, 4, 5), weight=1)
		self.detail_difficulty.grid_columnconfigure((0, 6), weight=2)
		self.detail_difficulty.grid(row=RID_DIFFICULTY, column=CID_LEFT, sticky="nwe")

		self.difficulty: list[customtkinter.CTkFrame] = []

		for i in range(5):
			self.difficulty.append(
				customtkinter.CTkFrame(self.detail_difficulty, fg_color="green", corner_radius=uv(1000), width=uv(25),
				                       height=uv(25), border_color="white"))
			self.difficulty[i].grid(row=0, column=i + 1)

		self.__set_difficulty(current_trail["difficulty"])

		# get all the trails in the db
		test_list = self.__fetch_trail_list()

		self.button_list: list[customtkinter.CTkButton] = []
		for trail in test_list:
			self.trail_button = self.create_button(trail, test_list.index(trail))
			self.button_list.append(self.trail_button)

	def __set_description(self, description: str):
		"""Set the description of the trail."""
		self.detail_description.configure(state=tk.NORMAL)
		self.detail_description.delete("1.0", tk.END)
		self.detail_description.insert(tk.END, description)
		self.detail_description.configure(state=tk.DISABLED)

	def __set_difficulty(self, difficulty: int):
		"""Set the difficulty of the trail."""

		if difficulty < 0 or difficulty > 4:
			raise ValueError("difficulty must be in [0..4]")

		for i in range(5):
			if i <= difficulty:
				self.difficulty[i].configure(fg_color=COLOR_DIFFICULTY[i], border_width=0)
			else:
				self.difficulty[i].configure(fg_color="transparent", border_width=uv(2))

	def __set_title(self, title: str):
		"""Set the title of the page."""
		self.detail_title_name.configure(text=title)

	def __fetch_trail_list(self):
		"""Fetch the trail list from the database."""
		return [f"Path {i}" for i in range(1, 13)]
		# return [f"Piste {run}" for run in route_queries.get_all_routes()]

	def __fletch_trail_detail(self):
		"""Fetch the trail detail from the database."""
		return {"title": f"Piste {self.choose_index + 1}",
		        "name": f"Piste {self.choose_index + 1}",
		        "difficulty": self.choose_index % 5,  # in [0..4]
		        "image": f"trail_{self.choose_index + 1}.jpg",
		        "description": f"{self.choose_index}Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed euismod, nisl eget ultricies ultrices, nunc nisl ultricies nunc, nec aliquam nisl nunc eget nisl. Nulla facilisi. Nu"
		        }

	def create_button(self, display_text, index):
		"""Creates a button with the given text."""

		is_first = index == 0

		self.button = customtkinter.CTkButton(
			self.trail_list_frame,
			text=display_text,
			fg_color=SECONDARY_COLOR if is_first else "transparent",
			hover_color=SECONDARY_COLOR,
			border_spacing=uv(17),
			command=lambda: self.show_trail_detail(index),
			anchor="w"
		)

		self.button.grid(row=index, column=0, padx=uv(10), sticky="ew")
		return self.button

	def selection_trail(self):
		"""Select the trail."""
		button_text = self.trail_selection_button.cget("text")
		if button_text == "Select":
			self.trail_selection_button.configure(text="Selected", fg_color=LIGHT_GREEN, hover_color=DARK_GREEN)
			state.set_trail(self.choose_index)
		else:
			self.trail_selection_button.configure(text="Select", fg_color=PRIMARY_COLOR,
			                                      hover_color=PRIMARY_HOVER_COLOR)
			state.set_trail(None)
		self.app.update_menu()

		# faire le back-end pour enregistrer le choix de l'utilisateur

	def show_trail_detail(self, trail_chosen):
		"""Shows the trail detail page."""
		if not self.button_list or trail_chosen == self.choose_index:
			return

		for button in self.button_list:
			button.configure(fg_color="transparent")

		self.choose_index = trail_chosen
		if trail_chosen == state.get_trail():
			self.trail_selection_button.configure(text="Selected", fg_color=LIGHT_GREEN, hover_color=DARK_GREEN)
		else:
			self.trail_selection_button.configure(text="Select", fg_color=PRIMARY_COLOR,
			                                      hover_color=PRIMARY_HOVER_COLOR)

		self.button_list[trail_chosen].configure(fg_color=SECONDARY_COLOR, hover_color=SECONDARY_HOVER_COLOR)
		self.trail_label.grid_forget()

		self.__image_loader("trail_" + str(trail_chosen + 1))
		self.trail_label.grid(row=RID_DESCR, column=CID_RIGHT)

		current_trail = self.__fletch_trail_detail()
		self.__set_title(current_trail["name"])
		self.__set_difficulty(current_trail["difficulty"])
		self.__set_description(current_trail["description"])

	def __image_loader(self, image_name: str):
		"""Loads an image from the given path."""
		image_size = self.trail_image.cget("size")
		self.trail_image = customtkinter.CTkImage(Image.open(self.__get_trail_image_path(image_name + ".jpg")),
		                                          size=image_size)
		self.trail_label.configure(image=self.trail_image)

	def __get_trail_image_path(self, trail_image_name: str):
		"""Return the path of the icon passed in parameter."""
		parent_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
		path = os.path.join(parent_path, 'resources', 'images', trail_image_name)
		if os.path.exists(path):
			return path
		return os.path.join(parent_path, 'resources', 'images', "trail_1.jpg")
	
	def on_size_change(self, width, height):
		super().on_size_change(width, height)

		image_size = min_max_range(uv(75), uv(1000), v(22, width))
		self.trail_image.configure(size=(image_size, image_size))
		self.trail_label.configure(height=iuv(image_size), width=iuv(image_size))

		font_style_default = (FONT, min_max_range(iuv(8), iuv(28), int(v(1.9, width))))
		font_style_title = (FONT, min_max_range(iuv(12), iuv(32), int(v(2.5, width))), "bold")

		self.trail_selection_button.configure(height=v(5, height), width=image_size, font=font_style_default)
		self.detail_description.configure(font=font_style_default)

		for button in self.button_list:
			button.configure(height=v(5, height), width=image_size, font=font_style_default)
		self.trail_list_title.configure(font=font_style_title)

		size_difficulty = min_max_range(uv(15), uv(100), v(2.5, width))
		for i in range(5):
			self.difficulty[i].configure(width=size_difficulty, height=size_difficulty)

	def get_name(self):
		return "Trail selection"
