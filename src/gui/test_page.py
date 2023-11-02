"""Module tkinter for the test page."""
import tkinter as tk
import customtkinter
from gui.singleton_metaclass import singleton_page
from gui.login_page import login_page

class test_page(customtkinter.CTkFrame, singleton_page):
    """test page."""
    def __init__(self, parent):
        """Constructor. Singleton then init executed only once."""
        super().__init__(parent)

        parent.title("test Page")

        self.test_label = customtkinter.CTkLabel(self, text="test:")
        self.test_label.grid(row = 0, column = 0)

        self.btn = customtkinter.CTkButton(self, text="test", command=lambda: parent.show_page(login_page))
        self.btn.grid(row = 1, column = 0)
    
    def update(self) -> None:
        return self