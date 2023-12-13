"""Module for tkinter interface of menu page."""
import os.path

import customtkinter
from PIL import Image

from gui.abstract.page import Page
from gui.app_state import AppState
from gui.utils import v, min_max_range, iuv, uv, PRIMARY_COLOR, SECONDARY_COLOR, EMPTY_IMAGE

state = AppState()

DEFAULT_RADIUS = 12
COLOR = PRIMARY_COLOR  # "#0b7687"

DEFAULT_RADIUS_ACTIVE = 4
COLOR_ACTIVE = SECONDARY_COLOR  # "#2ab9d4"


class MenuPage(Page):
	"""Class of the menu page"""

	__active_elem = None

	def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk):
		super().__init__(parent, app)

		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure((1, 2, 3, 4), weight=1)
		self.grid_rowconfigure((0, 5), weight=6)

		# initialize logo

		self.piste = customtkinter.CTkImage(dark_image=Image.open(self.__get_icon_path("piste_light.png")),
		                                    size=(80, 80))
		self.wall_label = customtkinter.CTkLabel(self, text="", font=("Helvetica", 20, "bold"), image=self.piste,
		                                          height=100, width=100, fg_color=COLOR, corner_radius=DEFAULT_RADIUS)
		self.wall_label.grid(row=1, column=0, pady=(10, 10), padx=(10, 10))
		self.__set_hover_effect(self.wall_label, self.piste, "Wall")

		self.route = customtkinter.CTkImage(dark_image=Image.open(self.__get_icon_path("chemin_light.png")),
		                                     size=(80, 80))
		self.route_label = customtkinter.CTkLabel(self, text="", font=("Helvetica", 20, "bold"), image=self.route,
		                                           height=100, width=100, fg_color=COLOR, corner_radius=DEFAULT_RADIUS)
		self.route_label.grid(row=2, column=0, padx=(10, 10))
		self.__set_hover_effect(self.route_label, self.route, "Route")

		self.run = customtkinter.CTkImage(dark_image=Image.open(self.__get_icon_path("run_light.png")), size=(80, 80))
		self.run_label = customtkinter.CTkLabel(self, text="", font=("Helvetica", 20, "bold"), image=self.run,
		                                        height=100, width=100, fg_color=COLOR, corner_radius=DEFAULT_RADIUS)
		self.run_label.grid(row=3, column=0, pady=(10, 10), padx=(10, 10))
		self.__set_hover_effect(self.run_label, self.run, "Run")

		self.account = customtkinter.CTkImage(dark_image=Image.open(self.__get_icon_path("compte_light.png")),
		                                     size=(80, 80))
		self.account_label = customtkinter.CTkLabel(self, text="", font=("Helvetica", 20, "bold"), image=self.account,
		                                           height=100, width=100, fg_color=COLOR, corner_radius=DEFAULT_RADIUS)
		self.account_label.grid(row=4, column=0, pady=(0, 10), padx=(10, 10))
		self.__set_hover_effect(self.account_label, self.account, "My\nspace")

		entry = self.wall_label

		self.__change_active(entry)

	# Hide/Show methods
	def hide_wall(self):
		self.wall_label.grid_forget()

	def show_wall(self):
		self.wall_label.grid(row=1, column=0, pady=(10, 10), padx=(10, 10))

	def hide_route(self):
		self.route_label.grid_forget()

	def show_route(self):
		self.route_label.grid(row=2, column=0, padx=(10, 10))

	def hide_run(self):
		self.run_label.grid_forget()

	def show_run(self):
		self.run_label.grid(row=3, column=0, pady=(10, 10), padx=(10, 10))

	# Set Command methods
	def set_command_route(self, command):
		self.__set_on_click(self.route_label, lambda e: command())

	def set_command_run(self, command):
		self.__set_on_click(self.run_label, lambda e: command())

	def set_command_account(self, command):
		self.__set_on_click(self.account_label, lambda e: command())

	def set_command_wall(self, command):
		self.__set_on_click(self.wall_label, lambda e: command())

	# Utils
	def __change_active(self, elem: customtkinter.CTkLabel):
		"""Change the active element."""
		if self.__active_elem is not None:
			self.__active_elem.configure(fg_color=COLOR, corner_radius=DEFAULT_RADIUS)
		elem.configure(fg_color=COLOR_ACTIVE, corner_radius=DEFAULT_RADIUS_ACTIVE)
		self.__active_elem = elem

	def __get_icon_path(self, icon_name: str):
		"""Return the path of the icon passed in parameter."""
		return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'resources',
		                    'images', icon_name)

	def __set_hover_effect(self, elem: customtkinter.CTkLabel, image: customtkinter.CTkImage, hover_text: str):
		"""Set the hover effect on the label passed in parameter."""
		elem.bind("<Enter>", lambda e: elem.configure(text=hover_text, image=EMPTY_IMAGE))
		elem.bind("<Leave>", lambda e: elem.configure(image=image, text=""))

	def __set_on_click(self, elem: customtkinter.CTkLabel,
	                   on_click=lambda e: print("Please implement the on click function")):
		"""Set the on click function on the label passed in parameter."""

		def extended_on_click(e):
			self.__change_active(elem)
			on_click(e)

		elem.bind("<Button-1>", extended_on_click)

	# Methods for the page
	def update(self, *args, **kwargs):
		"""Update the page."""
		self.__update_route()
		self.__update_run()

	def __update_route(self):
		if state.is_wall_selected():
			self.show_route()
		else:
			self.hide_route()

	def __update_run(self):
		if state.is_route_selected():
			self.show_run()
		else:
			self.hide_run()

	def set_active(self):
		"""Set the page active."""
		super().set_active()
		self.__change_active(self.wall_label)

	def on_size_change(self, width, height):
		"""Called when the windows size change."""

		size_icon = min_max_range(uv(60), uv(80), v(5.5, width))
		size_label_icon = 115 / 80 * size_icon
		default_font = ("Helvetica", min_max_range(iuv(22), iuv(30), int(v(1.7, width))), "bold")

		def set_size(label: customtkinter.CTkLabel, image: customtkinter.CTkImage):
			label.configure(height=size_label_icon, width=size_label_icon, font=default_font)
			image.configure(size=(size_icon, size_icon))

		set_size(self.wall_label, self.piste)
		set_size(self.route_label, self.route)
		set_size(self.run_label, self.run)
		set_size(self.account_label, self.account)
