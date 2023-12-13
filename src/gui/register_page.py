"""Module for tkinter interface of register page."""
import customtkinter

from database import user_queries
from gui.abstract.page import Page
from gui.utils import SECONDARY_COLOR, SECONDARY_HOVER_COLOR, FONT


class RegisterPage(Page):
	"""Class of the register page."""

	def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk = None):
		super().__init__(parent, app)

		self.show_page = app.show_page
		self.popup = None

		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.grid_columnconfigure((0, 1, 2, 3), weight=1)
		self.grid_rowconfigure((0, 2, 3, 4, 5, 7), weight=1)
		self.grid_rowconfigure((1, 6), weight=4)

		self.register_label = customtkinter.CTkLabel(self, text="Register", font=("Arial", 30))
		self.register_label.grid(row=0, column=0, columnspan=2, pady=(10, 0))

		self.pseudo_label = customtkinter.CTkLabel(self, text="Username")
		self.pseudo_label.grid(row=2, column=1, sticky="sw", columnspan=2)
		self.pseudo_entry = customtkinter.CTkEntry(self, width=200)
		self.pseudo_entry.grid(row=3, column=1, sticky="nw", columnspan=2)
		self.pseudo_entry.bind("<Return>", lambda event: self.register())

		self.password_label = customtkinter.CTkLabel(self, text="Password")
		self.password_label.grid(row=4, column=1, sticky="sw", columnspan=2)
		self.password_entry = customtkinter.CTkEntry(self, show="*", width=200)
		self.password_entry.grid(row=5, column=1, sticky="nw", columnspan=2)
		self.password_entry.bind("<Return>", lambda event: self.register())

		self.register_button = customtkinter.CTkButton(self, text="Register", fg_color=SECONDARY_COLOR,
		                                               hover_color=SECONDARY_HOVER_COLOR, command=self.register)
		self.register_button.grid(row=7, column=0, columnspan=2)

		self.back_button = customtkinter.CTkButton(self, text="Back", fg_color=SECONDARY_COLOR,
		                                           hover_color=SECONDARY_HOVER_COLOR, command=self.cancel)
		self.back_button.grid(row=7, column=2, columnspan=2)

	def register(self):
		"""Register the user."""
		pseudo = self.pseudo_entry.get()
		password = self.password_entry.get()

		if pseudo not in self.__get_all_usernames():
			user_queries.create_user(pseudo, password)
			self.app.show_login_page()
			if self.popup is not None and self.popup.winfo_exists():
				self.popup.destroy()
		else:
			if self.popup is None or not self.popup.winfo_exists():
				self.popup = customtkinter.CTkToplevel(self)
				self.popup.grid_columnconfigure(0, weight=1)
				self.popup.grid_rowconfigure((0,1), weight=1)
				self.popup.geometry("300x100")
				self.popup.resizable(False, False)
				self.popup.title("Warning")
				popup_button = customtkinter.CTkButton(self.popup,
														text="Ok",
														command=self.popup.destroy,
														font=(FONT, 16))
				popup_button.grid(row=1, column=0)
			
			self.after(200, self.popup.lift)
			popup_label = customtkinter.CTkLabel(self.popup, text=f"Username \"{pseudo}\" is already taken!", font=(FONT, 18))
			popup_label.grid(row=0, column=0, sticky="nswe")
		

	def cancel(self):
		"""Cancel the registration."""
		from gui.login_page import LoginPage

		if self.app is not None:
			self.app.show_page(LoginPage)

	def __get_all_usernames(self):
		username_list = []
		for user in user_queries.get_all_users():
			username_list.append(user.username)
		return username_list
