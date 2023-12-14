"""Module for tkinter interface of account page."""
import customtkinter

from gui.abstract.page import Page
from gui.app_state import AppState
from gui.login_page import LoginPage
from gui.utils import SECONDARY_COLOR, SECONDARY_HOVER_COLOR, FONT
from utils.camera_discover_utils import get_available_cameras_names
from database.queries import user_queries

state = AppState()


class AccountPage(Page):
	"""Class of the account page."""

	def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk = None):
		super().__init__(parent, app)

		self.popup = None

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

		self.choose_cam_button = customtkinter.CTkButton(self, text="Validate", fg_color=SECONDARY_COLOR,
		                                                 hover_color=SECONDARY_HOVER_COLOR, command=self.validate)
		self.choose_cam_button.grid(row=2, column=1, columnspan=2)

		self.delete_acc_button = customtkinter.CTkButton(self, text="Delete account", fg_color=SECONDARY_COLOR,
		                                                 hover_color=SECONDARY_HOVER_COLOR, command=self.ask_confirmation)
		self.delete_acc_button.grid(row=4, column=3)

		self.desconnect_button = customtkinter.CTkButton(self, text="Log out", fg_color=SECONDARY_COLOR,
		                                                 hover_color=SECONDARY_HOVER_COLOR, command=self.desconnect)
		self.desconnect_button.grid(row=4, column=4, padx=10)

	def validate(self):
		"""Validate the settings."""
		self.choose_cam()

	def choose_cam(self):
		"""Choose the camera."""
		state.set_camera_name(self.choose_cam_combobox.get())
		print("Camera set to", self.choose_cam_combobox.get())
		pass

	def desconnect(self):
		"""Desconnect the user."""
		self.app.show_page(LoginPage)
		state.set_wall(None)
		state.set_route(None)
		state.set_user(None)
		self.app.update_menu()
		self.app.menu_frame.set_active()

	def ask_confirmation(self):
		"""Delete the account."""
		if state.get_user().role in ["admin", "guest"]:
			return
		elif self.popup is None or not self.popup.winfo_exists():
			self.popup = customtkinter.CTkToplevel(self)
			self.popup.grid_columnconfigure((0,1), weight=1)
			self.popup.grid_rowconfigure((0,1), weight=1)
			self.popup.geometry("300x100")
			self.popup.resizable(False, False)
			self.popup.title("Warning")
			popup_button_yes = customtkinter.CTkButton(self.popup,
													text="Yes",
													command=lambda:[self.popup.destroy(), self.delete_account()],
													font=(FONT, 16))
			popup_button_yes.grid(row=1, column=0)

			popup_button_no = customtkinter.CTkButton(self.popup,
													text="No",
													command=self.popup.destroy,
													font=(FONT, 16))
			popup_button_no.grid(row=1, column=1)
		
			self.after(200, self.popup.lift)
			popup_label = customtkinter.CTkLabel(self.popup, text=f"Are you sure you want to\n delete your account?", font=(FONT, 18))
			popup_label.grid(row=0, column=0, sticky="nswe", columnspan=2)
	
	def delete_account(self):
		user_queries.delete_user_by_name(state.get_user().username)
		self.app.show_page(LoginPage)
