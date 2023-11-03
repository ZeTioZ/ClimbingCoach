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

    latest_width = 0
    latest_height = 0

    def __init__(self):
        """Constructor."""
        super().__init__()

        self.geometry("600x300+600+300")
        self.title("Climbing Coach")

        # detect windows size change
        self.bind("<Configure>", lambda e: self.onWindowsSizeChange())
        latest_width = self.winfo_width()
        latest_height = self.winfo_height()

        self.init_frame()
        self.show_page(login_page)
    

    # Page utils
    def show_page(self, page: customtkinter.CTkFrame):
        """Show the page passed in parameter."""
        if self.page_frame is not None: self.page_frame.grid_forget()
        self.page_frame = page.get_instance(self.container_frame, self)
        self.page_frame.grid(row=0, column=0, sticky="nsew")
    
    def update_page(self, page: customtkinter.CTkFrame):
        """Update the page passed in parameter."""
        page.get_instance(self).update()
        self.show_page(page)
    
    def onWindowsSizeChange(self):
        """Called when the windows size change."""
        if self.page_frame is not None:
            if self.latest_width != self.winfo_width() or self.latest_height != self.winfo_height():
                self.latest_width = self.winfo_width()
                self.latest_height = self.winfo_height()
                self.page_frame.onSizeChange(self.winfo_width(), self.winfo_height())

    # Initialize the application frame
    def init_frame(self):
        """Initialize the application frame."""

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.menu_frame = customtkinter.CTkFrame(self, fg_color="red", width=150)
        self.menu_frame.grid(row=0, column=0, sticky="nswe")    

        self.container_frame = customtkinter.CTkFrame(self)
        self.container_frame.grid(row=0, column=1, sticky="nswe")

        #self.main_frame.grid()

    def __collapse_menu(self):
        """Collapse the menu."""
        self.menu_frame.grid_forget()
        self.container_frame.grid_forget()
        self.container_frame.grid(row=0, column=0, columnspan = 2 ,sticky="nswe")
    
    def __expand_menu(self):
        """Expand the menu."""
        self.menu_frame.grid_forget()
        self.container_frame.grid_forget()
        self.menu_frame.grid(row=0, column=0, sticky="nswe")
        self.container_frame.grid(row=0, column=1, sticky="nswe")

    def toggle_menu(self):
        """Toggle the menu."""
        if self.menu_frame.winfo_ismapped():
            self.__collapse_menu()
        else:
            self.__expand_menu()


if __name__ == "__main__":
    app = Application()
    app.mainloop()