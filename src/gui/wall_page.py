"""Module for tkinter interface of wall page."""
import os.path
import pickle
import numpy as np
import tkinter as tk
import customtkinter

from PIL import Image

from gui.create_wall import CreateWall
from gui.abstract.page import Page
from gui.app_state import AppState
from gui.utils import FONT, LIGHT_GREEN, DARK_GREEN, PRIMARY_COLOR, PRIMARY_HOVER_COLOR, SECONDARY_COLOR, \
	SECONDARY_HOVER_COLOR, COLOR_DIFFICULTY
from gui.utils import v, uv, iuv, min_max_range, get_ressources_path, normalize_title
from database.queries import wall_queries

state = AppState()

RID_TITLE = 1
RID_DESCR = 2
RID_DIFFICULTY = 3

CID_LEFT = 1
CID_RIGHT = 2


class WallPage(Page):
	"""Class of the wall page."""

	def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk):
		super().__init__(parent, app)

		self.choose_index = 0

		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=7)
		self.grid_rowconfigure(0, weight=0, minsize=uv(80))
		self.grid_rowconfigure(1, weight=1)

		self.image_max_size = (uv(200), uv(200))  # (width, height)

		self.wall_list_frame = customtkinter.CTkScrollableFrame(self, width=uv(150))
		self.wall_list_frame.grid(row=1, column=0, sticky="nswe")
		self.wall_list_frame.grid_columnconfigure(0, weight=1)

		self.wall_list_title = customtkinter.CTkLabel(self, text="Walls list", font=(FONT, iuv(28), "bold"))
		self.wall_list_title.grid(row=0, column=0, sticky="nswe")

		self.wall_detail_frame = customtkinter.CTkFrame(self)
		self.wall_detail_frame.grid(row=0, column=1, rowspan=2, sticky="nswe")
		self.wall_detail_frame.configure(fg_color="transparent")

		self.wall_detail_frame.grid_columnconfigure((CID_RIGHT, CID_LEFT), weight=3)
		self.wall_detail_frame.grid_columnconfigure((0, 3), weight=1)
		self.wall_detail_frame.grid_rowconfigure((0, 4), weight=0)
		self.wall_detail_frame.grid_rowconfigure((RID_TITLE, RID_DIFFICULTY), weight=1)
		self.wall_detail_frame.grid_rowconfigure(RID_DESCR, weight=3)

	def set_active(self):
		"""Set the page active."""
		self.all_walls = wall_queries.get_all_walls()

		if len(self.all_walls) > 0:
			for widget in self.wall_detail_frame.winfo_children():
				widget.grid_forget()
			for widget in self.wall_list_frame.winfo_children():
				widget.grid_forget()

			self.current_wall = self.__fetch_wall_detail()
			# Convert the image from bytes to numpy array
			# image: np.array = pickle.loads(self.current_trail["image"])
			# image_fromarray = Image.fromarray(image)

			# self.trail_image = customtkinter.CTkImage(image_fromarray, size=(uv(200), uv(200)))
			# self.trail_label = customtkinter.CTkLabel(self.trail_detail_frame, text="", image=self.trail_image)
			self.wall_label = customtkinter.CTkLabel(self.wall_detail_frame, text="")
			self.wall_label.grid(row=RID_DESCR, rowspan=1, column=CID_RIGHT, padx=(uv(0), uv(50)))
			self.__image_loader()

			self.wall_selection_button = customtkinter.CTkButton(self.wall_detail_frame, text="Select",
			                                                     command=lambda: self.selection_wall())
			self.wall_selection_button.grid(row=RID_DIFFICULTY, column=CID_RIGHT, sticky="n", padx=(uv(0), uv(50)))

			self.detail_title_name = customtkinter.CTkLabel(self.wall_detail_frame, text=normalize_title(self.current_wall["name"]),
			                                                font=(FONT, iuv(32), "bold"), fg_color=SECONDARY_COLOR,
			                                                corner_radius=20, width=uv(350))
			self.detail_title_name.grid(row=RID_TITLE, column=CID_LEFT, columnspan=2, sticky="", ipady=uv(10))

			self.detail_description = customtkinter.CTkTextbox(self.wall_detail_frame, font=(FONT, iuv(16)),
			                                                   wrap=tk.WORD,
			                                                   fg_color="transparent")
			self.detail_description.insert(tk.END, self.current_wall["description"])
			self.detail_description.configure(state=tk.DISABLED)
			self.detail_description.grid(row=RID_DESCR, column=CID_LEFT, sticky="nswe", pady=(uv(50), uv(0)), padx=(uv(50), uv(0)))

			self.detail_difficulty = customtkinter.CTkFrame(self.wall_detail_frame, fg_color="transparent")
			self.detail_difficulty.grid_columnconfigure((1, 2, 3, 4, 5), weight=1)
			self.detail_difficulty.grid_columnconfigure((0, 6), weight=2)
			self.detail_difficulty.grid(row=RID_DIFFICULTY, column=CID_LEFT, sticky="nwe")

			self.difficulty: list[customtkinter.CTkFrame] = []

			for i in range(5):
				self.difficulty.append(
					customtkinter.CTkFrame(self.detail_difficulty, fg_color="green", corner_radius=uv(1000),
					                       width=uv(25),
					                       height=uv(25), border_color="white"))
				self.difficulty[i].grid(row=0, column=i + 1)

			self.__set_difficulty(self.current_wall["difficulty"])

		self.button_list: list[customtkinter.CTkButton] = []
		for wall in self.all_walls:
			self.wall_button = self.create_button(wall.name, self.all_walls.index(wall))
			self.button_list.append(self.wall_button)

		self.user = state.get_user()
		# TODO: faire un reload des pistes
		if self.user.role == "admin":
			get_image_button = customtkinter.CTkImage(
				Image.open(os.path.join(get_ressources_path(), "images", "add_button.png")), size=(uv(40), uv(40)))
			self.add_wall_button = customtkinter.CTkButton(self.wall_list_frame, image=get_image_button, text="",
			                                               command=lambda: self.app.show_page(CreateWall),
			                                               corner_radius=uv(10000000), width=uv(40), height=uv(40),
			                                               fg_color="transparent")
			self.add_wall_button.grid(row=0, column=0, pady=uv(10))

		if state.get_wall() is not None:
			self.selection_wall()

	def __set_description(self, description: str):
		"""Set the description of the wall."""
		self.detail_description.configure(state=tk.NORMAL)
		self.detail_description.delete("1.0", tk.END)
		self.detail_description.insert(tk.END, description)
		self.detail_description.configure(state=tk.DISABLED)

	def __set_difficulty(self, difficulty: int):
		"""Set the difficulty of the wall."""

		if difficulty < 1 or difficulty > 5:
			raise ValueError("difficulty must be in [1..5]")

		for i in range(5):
			if i <= difficulty - 1:
				self.difficulty[i].configure(fg_color=COLOR_DIFFICULTY[i], border_width=0)
			else:
				self.difficulty[i].configure(fg_color="transparent", border_width=uv(2))

	def __set_title(self, title: str):
		"""Set the title of the page."""
		title_normalized = normalize_title(title)
		self.detail_title_name.configure(text=title_normalized)

	def __fetch_wall_detail(self):
		"""Fetch the wall detail from the database."""
		return {"name": self.all_walls[self.choose_index].name,
		        "difficulty": self.all_walls[self.choose_index].difficulty,
		        "image": self.all_walls[self.choose_index].image,
		        "description": self.all_walls[self.choose_index].description
		        }

	def create_button(self, display_text, index):
		"""Creates a button with the given text."""

		self.button = customtkinter.CTkButton(
			self.wall_list_frame,
			text=normalize_title(display_text),
			fg_color=SECONDARY_COLOR if self.choose_index == index else "transparent",
			hover_color=SECONDARY_COLOR,
			border_spacing=uv(17),
			command=lambda: self.show_wall_detail(index),
			anchor="w"
		)

		self.button.grid(row=index + 1, column=0, padx=uv(10), sticky="ew")
		return self.button

	def selection_wall(self):
		"""Select the wall."""
		button_text = self.wall_selection_button.cget("text")
		if button_text == "Select":
			self.wall_selection_button.configure(text="Selected", fg_color=LIGHT_GREEN, hover_color=DARK_GREEN)
			state.set_wall(wall_queries.get_wall_by_name(self.all_walls[self.choose_index].name))
		else:
			self.wall_selection_button.configure(text="Select", fg_color=PRIMARY_COLOR,
			                                     hover_color=PRIMARY_HOVER_COLOR)
			state.set_wall(None)
		self.app.update_menu()

	# TODO: faire le back-end pour enregistrer le choix de l'utilisateur

	def show_wall_detail(self, wall_chosen):
		"""Shows the wall detail page."""
		if not self.button_list or wall_chosen == self.choose_index:
			return

		for button in self.button_list:
			button.configure(fg_color="transparent")

		self.choose_index = wall_chosen
		if wall_chosen == state.get_wall():
			self.wall_selection_button.configure(text="Selected", fg_color=LIGHT_GREEN, hover_color=DARK_GREEN)
		else:
			self.wall_selection_button.configure(text="Select", fg_color=PRIMARY_COLOR,
			                                     hover_color=PRIMARY_HOVER_COLOR)

		self.button_list[wall_chosen].configure(fg_color=SECONDARY_COLOR, hover_color=SECONDARY_HOVER_COLOR)

		self.current_wall = self.__fetch_wall_detail()

		self.wall_label.grid_forget()
		self.__image_loader()
		self.wall_label.grid(row=RID_DESCR, column=CID_RIGHT)

		self.__set_title(self.current_wall["name"])
		self.__set_difficulty(self.current_wall["difficulty"])
		self.__set_description(self.current_wall["description"])

	def __image_loader(self):
		"""Loads an image from the given path."""

		image: np.array = pickle.loads(self.current_wall["image"])
		image_fromarray = Image.fromarray(image)

		image_size = self.__get_image_ration_safe(image_fromarray)

		self.wall_image = customtkinter.CTkImage(image_fromarray,
		                                         size=image_size)
		self.wall_label.configure(image=self.wall_image)

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

	def on_size_change(self, width, height):
		super().on_size_change(width, height)

		if len(self.all_walls) > 0:

			max_dim_size = min_max_range(uv(75), uv(1000), v(22, width))
			self.image_max_size = (max_dim_size, max_dim_size)

			if hasattr(self, "wall_image"):
				image_size = self.__get_image_ration_safe_by_size(self.wall_image.cget("size"))
				self.wall_image.configure(size=image_size)
				self.wall_label.configure(height=iuv(image_size[1]), width=iuv(image_size[0]))

			# self.trail_image.configure(size=(image_size, image_size))
			# self.trail_label.configure(height=iuv(image_size), width=iuv(image_size))

			font_style_default = (FONT, min_max_range(iuv(8), iuv(28), int(v(1.9, width))))
			font_style_title = (FONT, min_max_range(iuv(12), iuv(32), int(v(2.5, width))), "bold")

			self.wall_selection_button.configure(height=v(5, height), width=max_dim_size, font=font_style_default)
			self.detail_description.configure(font=font_style_default)

			for button in self.button_list:
				button.configure(height=v(5, height), width=max_dim_size, font=font_style_default)
			self.wall_list_title.configure(font=font_style_title)

			size_difficulty = min_max_range(uv(15), uv(100), v(2.5, width))
			for i in range(5):
				self.difficulty[i].configure(width=size_difficulty, height=size_difficulty)

			self.wall_list_frame.configure(width=max(uv(250), v(10, width)))

	def get_name(self):
		return "Wall selection"