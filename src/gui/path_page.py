"""Module for tkinter interface of path page."""
import os.path

import customtkinter
from PIL import Image

from gui.abstract.page import Page
from gui.app_state import AppState
from gui.add_path_page import AddPathPage
from gui.utils import FONT, LIGHT_GREEN, DARK_GREEN, PRIMARY_COLOR, PRIMARY_HOVER_COLOR, SECONDARY_COLOR, \
	SECONDARY_HOVER_COLOR
from gui.utils import v, uv, iuv, min_max_range

state = AppState()


class PathPage(Page):
	"""Class of the path page."""
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

		self.path_list_frame = customtkinter.CTkScrollableFrame(self, width=uv(150))
		self.path_list_frame.grid(row=1, column=0, sticky="nswe")
		self.path_list_frame.grid_columnconfigure(0, weight=1)

		self.path_creation_frame = customtkinter.CTkFrame(self)
		self.path_creation_frame.grid(row=2, column=0, sticky="nswe")

		self.path_list_tiltle = customtkinter.CTkLabel(self, text="Path list", font=(FONT, iuv(28), "bold"))
		self.path_list_tiltle.grid(row=0, column=0, sticky="nswe")
		
		self.create_path_button = customtkinter.CTkButton(self.path_creation_frame, text="Create path", fg_color=PRIMARY_COLOR, hover_color=PRIMARY_HOVER_COLOR, command=lambda : self.app.show_page(AddPathPage))
		self.create_path_button.grid(row=0, column=0)

		self.path_detail_frame = customtkinter.CTkFrame(self)
		self.path_detail_frame.grid(row=0, column=1, rowspan=2, sticky="nswe")
		self.path_detail_frame.configure(fg_color="transparent")

		self.path_detail_frame.grid_columnconfigure(0, weight=2)
		self.path_detail_frame.grid_columnconfigure((1, 2, 3), weight=1)
		self.path_detail_frame.grid_rowconfigure((0, 1), weight=1)
		self.path_detail_frame.grid_rowconfigure((2, 3), weight=1)

		self.path_image = customtkinter.CTkImage(Image.open(self.__get_image_path("trail_1.jpg")),
												 size=(uv(200), uv(200)))
		self.path_label = customtkinter.CTkLabel(self.path_detail_frame, text="", image=self.path_image)
		self.path_label.grid(row=1, column=1)

		self.path_selection_button = customtkinter.CTkButton(self.path_detail_frame, text="Select",
															 command=lambda: self.selection_path())
		self.path_selection_button.grid(row=2, column=1)

		self.difficulty_image_1 = customtkinter.CTkImage(Image.open(self.__get_image_path("diff_1.png")),
														 size=(uv(35), uv(35)))
		self.path_difficulty_label = customtkinter.CTkLabel(self.path_detail_frame, text="",
															image=self.difficulty_image_1)
		self.path_difficulty_label.grid(row=2, column=2, sticky="w", padx=uv(30))

		test_list = self.__fetch_path_list()

		self.button_list: list[customtkinter.CTkButton] = []
		for path in test_list:
			self.path_button = self.create_button(path, test_list.index(path))
			self.button_list.append(self.path_button)

	def __fetch_path_list(self):
		"""Fetch the path list from the database."""
		return [f"Path {i}" for i in range(1, 7)]

	def create_button(self, display_text, index):
		"""Creates a button with the given text."""

		is_first = index == 0

		self.button = customtkinter.CTkButton(
			self.path_list_frame,
			text=display_text,
			fg_color=SECONDARY_COLOR if is_first else "transparent",
			hover_color=SECONDARY_COLOR,
			border_spacing=uv(17),
			command=lambda: self.show_path_detail(index),
			anchor="w"
		)

		self.button.grid(row=index, column=0, padx=uv(10), sticky="ew")
		return self.button

	def selection_path(self):
		"""Select the path."""
		button_text = self.path_selection_button.cget("text")
		if button_text == "Select":
			self.path_selection_button.configure(text="Selected", fg_color=LIGHT_GREEN, hover_color=DARK_GREEN)
			state.set_run(self.choose_index)
		else:
			self.path_selection_button.configure(text="Select", fg_color=PRIMARY_COLOR, hover_color=PRIMARY_HOVER_COLOR)
			state.set_run(None)
		self.app.update_menu()

	def show_path_detail(self, path_chosen):
		"""Shows the path detail page."""
		if not self.button_list or self.__is_already_in_tab(path_chosen):
			return

		for button in self.button_list:
			button.configure(fg_color="transparent")

		self.choose_index = path_chosen
		self.__change_select_btn()

		self.button_list[path_chosen].configure(fg_color=SECONDARY_COLOR, hover_color=SECONDARY_HOVER_COLOR)

		# afficher a droite
		self.path_label.grid_forget()
		# self.trail_label.configure(image=self.__image_loader("trail_" + str(trail_chosen+1)),size=(300, 300))
		self.__image_loader("path_" + str(path_chosen + 1))
		self.path_label.grid(row=1, column=1)

	def __change_select_btn(self):
		if self.__is_already_selected():
			self.__set_select_btn_active()
		else:
			self.__set_select_btn_inactive()

	def __set_select_btn_active(self):
		self.path_selection_button.configure(text="Selected", fg_color=LIGHT_GREEN, hover_color=DARK_GREEN)

	def __set_select_btn_inactive(self):
		self.path_selection_button.configure(text="Select", fg_color=PRIMARY_COLOR, hover_color=PRIMARY_HOVER_COLOR)

	def __is_already_in_tab(self, tab: int) -> bool:
		"""Return true if the page is already in the tab."""
		return tab == self.choose_index

	def __is_already_selected(self) -> bool:
		"""Return true if the page is already selected."""
		return self.choose_index == state.get_run()

	def __image_loader(self, image_name: str):
		"""Loads an image from the given path."""
		image_size = self.path_image.cget("size")
		self.path_image = customtkinter.CTkImage(Image.open(self.__get_image_path(image_name + ".jpg")),
												 size=image_size)
		self.path_label.configure(image=self.path_image)

	def __get_image_path(self, image_name: str):
		"""Return the path of the icon passed in parameter."""
		parent_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
		path = os.path.join(parent_path, 'resources', 'images', image_name)
		if os.path.exists(path):
			return path
		return os.path.join(parent_path, 'resources', 'images', 'trail_1.jpg')

	def on_size_change(self, width, height):
		super().on_size_change(width, height)

		image_size = min_max_range(uv(75), uv(1000), v(25, width))
		self.path_image.configure(size=(image_size, image_size))
		self.path_label.configure(height=iuv(image_size), width=iuv(image_size))

		# TODO: change diff image size
		size_difficulty = min_max_range(uv(35), uv(100), v(2.5, width))
		self.difficulty_image_1.configure(width=size_difficulty, height=size_difficulty)

		font_style_default = (FONT, min_max_range(iuv(8), iuv(28), int(v(1.9, width))))
		self.path_selection_button.configure(height=v(5, height), width=image_size, font=font_style_default)
		for button in self.button_list:
			button.configure(height=v(5, height), width=image_size, font=font_style_default)

	def get_name(self):
		return "Path selection"

	# Overwriting section
	def set_active(self):
		super().set_active()

		self.__change_select_btn()
