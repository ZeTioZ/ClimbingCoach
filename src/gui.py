"""Module for the interface of the application."""
import tkinter as tk
import customtkinter
from tkinter import messagebox
from gui import login_page, test_page, singleton_page

class Application(customtkinter.CTk):
    """
    Interface of the application.
    """

    page_frame = None

    def __init__(self):
        """Constructor."""
        super().__init__()

        self.geometry("600x300+600+300")
        self.title("Climbing Coach")

        self.init_frame()
    

    # Page utils
    def show_page(self, page: customtkinter.CTkFrame):
        """Show the page passed in parameter."""
        if self.page_frame is not None: self.page_frame.grid_forget()
        self.page_frame = page.get_instance(self.container_frame)
        self.page_frame.grid(row=0, column=0, sticky="nsew")
    
    def update_page(self, page: customtkinter.CTkFrame):
        """Update the page passed in parameter."""
        page.get_instance(self).update()
        self.show_page(page)

    # Initialize the application frame
    def init_frame(self):
        """Initialize the application frame."""
        self.main_frame = customtkinter.CTkFrame(self)

        self.main_frame.grid_rowconfigure(0,weight=1)
        self.main_frame.grid_columnconfigure((0), weight=1)
        self.main_frame.grid_columnconfigure((1), weight=5)

        self.menu_frame = customtkinter.CTkButton(self.main_frame, bg_color="white", fg_color="red")
        self.menu_frame.grid(row=0, column=0, padx=5)

        self.container_frame = customtkinter.CTkButton(self.main_frame, bg_color="white", fg_color="blue")
        self.container_frame.grid(row=0, column=1)

        self.main_frame.grid()


if __name__ == "__main__":
    app = Application()
    app.mainloop()