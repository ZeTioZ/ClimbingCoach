"""Module for tkinter interface of the login page."""
import os.path
import tkinter as tk

import customtkinter
from PIL import Image

from database import user_queries
from gui.abstract.page import Page
from gui.app_state import AppState
from gui.trail_page import TrailPage
from gui.utils import v, uv, iuv, get_parent_path, FONT
from gui.register_page import RegisterPage

state = AppState()
DEFAULT_FONT = (FONT, iuv(16))
TITLE_FONT = (FONT, iuv(24))
DF = DEFAULT_FONT
TF = TITLE_FONT

DEFAULT_FONT_BIG = (FONT, iuv(32))
DFB = DEFAULT_FONT_BIG


class LoginPage(Page):
	"""Class for the login page."""

	RI_TITLE = 1
	RI_USERNAME_LABEL = 2
	RI_USERNAME = 3
	RI_PASSWORD_LABEL = 4
	RI_PASSWORD = 5
	RI_LOGIN = 6

	CI_LEFT = 1
	CI_RIGHT = 2

	__sizeState = None

	def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk):
		"""Constructor. Singleton then init executed only once."""
		super().__init__(parent, app)  # Call the __init__ method of the parent class
		app_path = get_parent_path(__file__, 3)

		# Frame configure
		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)  # Use to align the frame in the center of the window

		self.grid_rowconfigure((self.RI_TITLE, self.RI_LOGIN), weight=2, minsize=100)
		self.grid_rowconfigure((self.RI_USERNAME, self.RI_PASSWORD), weight=1)
		self.grid_rowconfigure((self.RI_USERNAME_LABEL, self.RI_PASSWORD_LABEL), weight=0)
		self.grid_rowconfigure((0, 7), weight=6)

		self.grid_columnconfigure((self.CI_LEFT, self.CI_RIGHT), weight=1)
		self.grid_columnconfigure((0, 3), weight=4)

		# Title
		self.app_image = customtkinter.CTkImage(
			Image.open(os.path.join(app_path, "resources", "images", "incroyable_logo_climbing_coach.png")),
			size=(100, 100))
		self.title = customtkinter.CTkLabel(self, text="", font=TF, image=self.app_image)
		self.title.bind("<Enter>", lambda e: self.title.configure(text="Logo", image=customtkinter.CTkImage(
			Image.frombytes("RGBA", (1, 1), b"\x00\x00\x00\x00"))))
		self.title.bind("<Leave>", lambda e: self.title.configure(text="", image=self.app_image))
		self.title.grid(row=self.RI_TITLE, column=self.CI_LEFT, columnspan=2)

		# Username
		self.username_label = customtkinter.CTkLabel(self, text="Username", font=DF)
		self.username_combobox = customtkinter.CTkComboBox(self, values=self.__get_all_usernames(), font=DF,
		                                                   dropdown_font=DF)  # Faire appel à la fonction qui permet de choper tous les users
		self.username_combobox.set("")
		self.username_label.grid(row=self.RI_USERNAME_LABEL, column=self.CI_LEFT, sticky="sw", columnspan=2)
		self.username_combobox.grid(row=self.RI_USERNAME, column=self.CI_LEFT, sticky="nwe", columnspan=2)
		self.username_combobox.bind("<Return>", lambda event: self.login())

		# Password
		self.password_label = customtkinter.CTkLabel(self, text="Password", font=DF)
		self.password_entry = customtkinter.CTkEntry(self, show="*")
		self.password_label.grid(row=self.RI_PASSWORD_LABEL, column=self.CI_LEFT, sticky="sw", columnspan=2)
		self.password_entry.grid(row=self.RI_PASSWORD, column=self.CI_LEFT, sticky="nwe", columnspan=2)
		self.password_entry.bind("<Return>", lambda event: self.login())

		# Login button
		self.login_button = customtkinter.CTkButton(self, text="Login", command=self.login, font=DF)
		self.login_button.grid(row=self.RI_LOGIN, column=self.CI_LEFT, columnspan=2)

		self.guest_button = customtkinter.CTkButton(self, text="Guest", font=DF, fg_color="#027148",
		                                            hover_color="#013220")
		self.guest_button.grid(row=self.RI_LOGIN, column=self.CI_LEFT, columnspan=2)

		self.register_button = customtkinter.CTkButton(self, text="Register",
		                                               command=lambda: self.app.show_page(RegisterPage), font=DF)
		self.register_button.grid(row=self.RI_LOGIN, column=self.CI_RIGHT, columnspan=2)

	def login(self):
		username = self.username_combobox.get()
		password = self.password_entry.get()
		self.__get_usernames(username)
		success, user = user_queries.user_can_connect(username, password)
		print(user_queries.user_can_connect(username, password))
		if success:
			# self.toggle_menu()
			self.app.show_page(TrailPage)
			state.set_username(user)
			print(f"You're now logged in as {user.username}")
			print(state.get_username())

	def __get_usernames(self, username: str):
		self.user = user_queries.get_user_by_name(username)
		return self.user

	def __get_all_usernames(self):
		username_list = []
		for user in user_queries.get_all_users():
			username_list.append(user.username)
		return username_list

	def __setup_small_screen(self):
		"""Set up the container for small screen."""
		self.grid_rowconfigure((0, 7), weight=6)

		self.login_button.grid(row=self.RI_LOGIN, column=self.CI_LEFT, columnspan=1, sticky="nw", pady=(10, 4))
		self.register_button.grid(row=self.RI_LOGIN, column=self.CI_RIGHT, columnspan=1, sticky="ne", pady=(10, 4))
		self.guest_button.grid(row=self.RI_LOGIN, column=self.CI_LEFT, columnspan=2, sticky="swe")

	def __setup_big_screen(self):
		"""Set up the container for big screen."""
		self.grid_rowconfigure(0, weight=1)
		self.grid_rowconfigure(7, weight=1)

		self.login_button.grid(row=self.RI_LOGIN, column=self.CI_LEFT, columnspan=1, sticky="nw", pady=0)
		self.guest_button.grid(row=self.RI_LOGIN, column=self.CI_RIGHT, columnspan=1, sticky="ne")
		self.register_button.grid(row=self.RI_LOGIN, column=self.CI_LEFT, columnspan=1, sticky="w", pady=0)

	def on_size_change(self, width, height):
		"""Called when the windows size change."""

		# Change grid structure
		if width > 800 and height > 600 and self.__sizeState != "big":
			self.__sizeState = "big"
			self.__setup_big_screen()
		elif width and height <= 600 and self.__sizeState != "small":
			self.__sizeState = "small"
			self.__setup_small_screen()

		default_font = (FONT, min(int(v(4, height)), iuv(24)))
		title_font = (FONT, min(int(v(6, height)), iuv(32)))

		app_icon_size = min(int(v(15, width)), uv(250))
		self.app_image.configure(size=(app_icon_size, app_icon_size))
		self.title.configure(width=app_icon_size, height=app_icon_size)

		self.username_label.configure(font=default_font)
		self.password_label.configure(font=default_font)
		self.login_button.configure(
			font=default_font,
			width=v(20, width)
		)
		self.register_button.configure(
			font=default_font,
			width=v(20, width)
		)
		self.guest_button.configure(
			font=default_font,
			width=v(20, width)
		)

		self.title.configure(font=title_font)

		self.password_entry.configure(font=default_font)
		self.username_combobox.configure(font=default_font, dropdown_font=default_font)

	def set_inactive(self):
		super().set_active()
		self.username_combobox.set("")
		self.password_entry.delete(0, tk.END)

	def get_name(self):
		return "Login"
