"""Module for the interface of the application."""
import os.path
import platform
from tkinter import PhotoImage

import customtkinter

from database.database_handler import DatabaseHandler
from gui import LoginPage, RunPage, Page, MenuPage, TrailPage, PathPage, AccountPage, RegisterPage, AddPathPage
from gui import set_height_utils, uv
from threads.camera_thread import Camera


class Application(customtkinter.CTk):
	"""
	Interface of the application.
	"""
	camera: Camera

	significant_change = 50  # Amount of pixel to consider a change as significant and then reload the page

	page_frame: Page | None = None
	menu_frame = None

	latest_width = 0
	latest_height = 0

	def __init__(self):
		"""Constructor."""
		super().__init__()
		#self.camera = Camera("resources/videos/Escalade_Fixe.mp4")
		self.camera = Camera()
		self.camera.start()
		set_height_utils(self.winfo_screenheight())

		self.geometry(f"{uv(700)}x{uv(600)}+600+300")
		self.title("Climbing Coach")

		self.database = DatabaseHandler()
		self.database.create_tables()
		self.minsize(uv(700), uv(600))

		self.current_dir = os.path.dirname(os.path.abspath(__file__))
		self.parent_dir = os.path.dirname(self.current_dir)

		theme_dir = os.path.join(self.parent_dir, 'resources', 'themes', 'cc.json')

		customtkinter.set_default_color_theme(theme_dir)

		# detect windows size change
		self.bind("<Configure>", lambda e: self.on_windows_size_change())
		self.latest_width = self.winfo_width()
		self.latest_height = self.winfo_height()

		self.__os_init()

		self.init_frame()
		self.show_page(LoginPage)
		self.show_menu()

	# OS Init Section
	def __os_init(self):
		"""Os specific initialization for the application"""
		if self.is_windows():
			self.__os_windows_init()
		elif self.is_linux():
			self.__os_linux_init()
		elif self.is_macos():
			self.__os_macos_init()
		else:
			raise Exception("Your os is not supported")

	def is_windows(self) -> bool:
		"""True if the os is Windows"""
		return platform.system() == "Windows"

	def is_linux(self) -> bool:
		"""True if the os is Linux"""
		return platform.system() == "Linux"

	def is_macos(self) -> bool:
		"""True if the os is macOS"""
		return platform.system() == "Darwin"

	def __os_windows_init(self):
		"""Initialisation for windows"""
		icon_path = os.path.join(self.parent_dir, 'resources', 'images', 'climbing_coach.ico')
		self.iconbitmap(icon_path)

	def __os_linux_init(self):
		"""Initialisation for Linux"""
		icon_path = os.path.join(self.parent_dir, 'resources', 'images', 'incroyable_logo_climbing_coach.png')
		img = PhotoImage(file=icon_path)
		self.tk.call('wm', 'iconphoto', self._w, img)

	def __os_macos_init(self):
		"""Initialisation for macOS"""
		icon_path = os.path.join(self.parent_dir, 'resources', 'images', 'incroyable_logo_climbing_coach.png')
		img = PhotoImage(file=icon_path)
		self.tk.call('wm', 'iconphoto', self._w, img)

	# Page utils
	def show_page(self, new_page: type(Page)):
		"""Show the page passed in parameter."""
		if not self.is_page_active(new_page):
			self.empty_container()
			self.set_new_page_frame(new_page)
			self.__hide_show_menu_if_login_or_register()
			self.fill_container()

	def show_login_page(self):
		"""Show the login page."""
		self.show_page(LoginPage)

	def is_page_active(self, page: type(Page)) -> bool:
		"""Return true if the page passed in parameter is active."""
		return isinstance(self.page_frame, type(page))

	def is_a_page_in_container(self) -> bool:
		"""Return true if a page is in the container."""
		return self.page_frame is not None

	def empty_container(self):
		"""Empty the page container."""
		if self.is_a_page_in_container():
			self.page_frame.grid_forget()
			self.page_frame.set_inactive()
			self.page_frame = None

	def fill_container(self):
		"""Fill the page container."""
		self.change_title(self.page_frame.get_name())
		self.page_frame.grid(row=0, column=0, sticky="nsew")

	def set_new_page_frame(self, new_page: type(Page)):
		"""Set the new page frame."""
		self.page_frame: Page = new_page(self.container_frame, self)
		self.page_frame.set_active()
		self.__unguarded_on_windows_size_change()
		self.page_frame.update()

	def show_menu(self):
		"""Show the menu page."""
		if self.menu_frame is not None:
			return
		self.menu_frame = MenuPage(self.menu_container_frame, self)
		self.menu_frame.grid(row=0, column=0, sticky="nsew")
		self.menu_frame.set_command_piste(lambda: self.show_page(TrailPage))
		self.menu_frame.set_command_chemin(lambda: self.show_page(PathPage))
		self.menu_frame.set_command_run(lambda: self.show_page(RunPage))
		self.menu_frame.set_command_compte(lambda: self.show_page(AccountPage))
		self.menu_frame.update()

	def update_page(self, page: type(Page)):
		"""Update the page passed in parameter."""
		page(self).update()
		self.show_page(page)

	def on_windows_size_change(self):
		"""Called when the window size change."""
		if self.__is_significant_change():
			self.__unguarded_on_windows_size_change()

	def __unguarded_on_windows_size_change(self):
		self.latest_width = self.winfo_width()
		self.latest_height = self.winfo_height()
		if self.page_frame is not None:
			self.page_frame.on_size_change(self.winfo_width(), self.winfo_height())
		if self.menu_frame is not None:
			self.menu_frame.on_size_change(self.winfo_width(), self.winfo_height())

	def __is_significant_change(self):
		"""Return true if the change is significant."""
		return abs(self.latest_width - self.winfo_width()) > self.significant_change or abs(
			self.latest_height - self.winfo_height()) > self.significant_change

	# Initialize the application frame
	def init_frame(self):
		"""Initialize the application frame."""

		# configure grid layout (2x1)
		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(0, weight=1)

		self.menu_container_frame = customtkinter.CTkFrame(self, width=uv(170))
		self.menu_container_frame.grid(row=0, column=0, sticky="nswe")

		self.container_frame = customtkinter.CTkFrame(self)
		self.container_frame.grid(row=0, column=1, sticky="nswe")

	# self.main_frame.grid()

	def __collapse_menu(self):
		"""Collapse the menu."""
		self.container_frame.grid_forget()
		self.menu_container_frame.grid_forget()
		self.container_frame.grid(row=0, column=0, columnspan=2, sticky="nswe")

	def __expand_menu(self):
		"""Expand the menu."""
		self.menu_container_frame.grid_forget()
		self.container_frame.grid_forget()
		self.menu_container_frame.grid(row=0, column=0, sticky="nswe")
		self.container_frame.grid(row=0, column=1, sticky="nswe")

	def __hide_show_menu_if_login_or_register(self):
		"""Hide the menu if the user is not logged in."""
		if self.__is_page_login() or self.__is_page_register():
			self.__collapse_menu()
		else:
			self.__expand_menu()

	def toggle_menu(self):
		"""Toggle the menu."""
		if self.menu_frame.winfo_ismapped():
			self.__collapse_menu()
		else:
			self.__expand_menu()

	def __is_page_login(self) -> bool:
		"""Return true if the page is the login page."""
		return isinstance(self.page_frame, LoginPage)

	def __is_page_register(self) -> bool:
		"""Return true if the page is the register page."""
		return isinstance(self.page_frame, RegisterPage)

	def change_title(self, title: str):
		"""Change the title of the application."""
		self.title(f"ClimbingCoach - {title}")

	def update_menu(self):
		"""Update the menu."""
		if self.menu_frame is not None:
			self.menu_frame.update()


if __name__ == "__main__":
	app = Application()
	app.mainloop()
