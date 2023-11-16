""""Module for tkinter interface of account page."""
import tkinter as tk
import customtkinter
from gui.page import page

from gui.utils import SECONDARY_COLOR, SECONDARY_HOVER_COLOR

class account_page(page):
    """Class of the account page."""

    def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk = None):
        super().__init__(parent)

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.grid_columnconfigure((0,1,2,3,4), weight=1)
        self.grid_rowconfigure((0,1,2,3,4), weight=1)

        self.account_label = customtkinter.CTkLabel(self, text="Account", font=("Arial", 30))
        self.account_label.grid(row=0, column=0, columnspan=2)

        self.desconnect_button = customtkinter.CTkButton(self, text="Log out", fg_color=SECONDARY_COLOR, hover_color=SECONDARY_HOVER_COLOR, command=self.desconnect)
        self.desconnect_button.grid(row=4, column=4)


    def desconnect(self):
        """Desconnect the user."""
        #TODO: desconnect the user
        pass