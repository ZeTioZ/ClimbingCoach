"""Module for tkinter interface of account page."""
import customtkinter

from gui.abstract.page import Page
from gui.app_state import AppState
from gui.login_page import LoginPage
from gui.utils import SECONDARY_COLOR, SECONDARY_HOVER_COLOR
from utils.camera_discover_utils import get_available_cameras_names

state = AppState()


class AccountPage(Page):
	"""Class of the account page."""

	def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk = None):
		super().__init__(parent, app)

		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
		self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

		self.account_label = customtkinter.CTkLabel(self, text="Account", font=("Arial", 30))
		self.account_label.grid(row=0, column=0)

		self.choose_cam_label = customtkinter.CTkLabel(self, text="Choose camera", font=("Arial", 20))
		self.choose_cam_label.grid(row=1, column=1, sticky="e")

		cam_list = get_available_cameras_names()
		self.choose_cam_combobox = customtkinter.CTkComboBox(self, values=cam_list, state="readonly")
		self.choose_cam_combobox.grid(row=1, column=2, padx=10, sticky="w")

		self.frame_rate_label = customtkinter.CTkLabel(self, text="Frame rate", font=("Arial", 20))
		self.frame_rate_label.grid(row=2, column=1, sticky="e")

		self.frame_rate_combobox = customtkinter.CTkComboBox(self, values=["30", "60"], state="readonly")
		self.frame_rate_combobox.grid(row=2, column=2, padx=10, sticky="w")

		self.choose_cam_button = customtkinter.CTkButton(self, text="Validate", fg_color=SECONDARY_COLOR,
		                                                 hover_color=SECONDARY_HOVER_COLOR, command=self.validate)
		self.choose_cam_button.grid(row=3, column=1, columnspan=2)

		self.desconnect_button = customtkinter.CTkButton(self, text="Log out", fg_color=SECONDARY_COLOR,
		                                                 hover_color=SECONDARY_HOVER_COLOR, command=self.desconnect)
		self.desconnect_button.grid(row=4, column=4, padx=10)

	def validate(self):
		"""Validate the settings."""
		self.choose_cam()
		self.choose_frame_rate()

	def choose_cam(self):
		"""Choose the camera."""
		state.set_camera_name(self.choose_cam_combobox.get())
		print("Camera set to", self.choose_cam_combobox.get())
		pass

	def choose_frame_rate(self):
		"""Choose the frame rate."""
		# state.set_framerate(self.frame_rate_combobox.get())
		print("Frame rate set to", self.frame_rate_combobox.get())
		pass

	def desconnect(self):
		"""Desconnect the user."""
		# TODO: desconnect the user
		self.app.show_page(LoginPage)
