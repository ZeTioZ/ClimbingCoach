"""Module for the interface of the application."""
import tkinter as tk
import customtkinter
from tkinter import messagebox
from gui import login_page, test_page, page, menu_page, trail_page, path_page
from gui import set_height_utils, UV
import os.path

class Application(customtkinter.CTk):
    """
    Interface of the application.
    """

    significant_change = 50 # Amount of pixel to consider a change as significant and then reload the page

    page_frame: page | None = None
    menu_frame = None

    latest_width = 0
    latest_height = 0

    def __init__(self):
        """Constructor."""
        super().__init__()
        set_height_utils(self.winfo_screenheight())

        self.geometry(f"{UV(700)}x{UV(600)}+600+300")
        self.title("Climbing Coach")

        self.minsize(UV(700), UV(600))


        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        icon_path = os.path.join(parent_dir, 'resources\\images', 'climbing_coach.ico')
        themeDir = os.path.join(parent_dir, 'resources\\themes', 'cc.json')

        self.iconbitmap(icon_path)

        customtkinter.set_default_color_theme(themeDir)

        # detect windows size change
        self.bind("<Configure>", lambda e: self.onWindowsSizeChange())
        self.latest_width = self.winfo_width()
        self.latest_height = self.winfo_height()

        self.init_frame()
        #self.show_page(login_page)
        self.show_page(trail_page)
        self.show_menu()
    
    # Page utils
    def show_page(self, new_page: page):
        """Show the page passed in parameter."""
        if(not self.is_page_active(new_page)): 
            
            self.empty_container()
            self.set_new_page_frame(new_page)
            self.fill_container()


    def is_page_active(self, page: page) -> bool:
        """Return true if the page passed in parameter is active."""
        return isinstance(self.page_frame, page)


    def is_a_page_in_container(self) -> bool:
        """Return true if a page is in the container."""
        return self.page_frame is not None


    def empty_container(self):
        """Empty the page container."""
        if self.is_a_page_in_container(): 
            self.page_frame.grid_forget()
            self.page_frame.setUnactive()
            self.page_frame = None


    def fill_container(self):
        """Fill the page container."""
        self.change_title(self.page_frame.get_name())
        self.page_frame.grid(row=0, column=0, sticky="nsew")


    def set_new_page_frame(self, new_page: page):
        """Set the new page frame."""
        self.page_frame: page = new_page(self.container_frame, self)
        self.page_frame.setActive()
        self.__ungarded_onWindowsSizeChange()
        self.page_frame.update()


    def show_menu(self):
        """Show the menu page."""
        if self.menu_frame is not None: return
        self.menu_frame = menu_page(self.menu_container_frame, self)
        self.menu_frame.grid(row=0, column=0, sticky="nsew")
        self.menu_frame.set_command_piste(lambda: self.show_page(trail_page))
        self.menu_frame.set_command_chemin(lambda: self.show_page(path_page))
        self.menu_frame.set_command_run(lambda: self.show_page(test_page))
        self.menu_frame.set_command_compte(lambda: self.show_page(login_page))
        self.menu_frame.update()
        
    
    def update_page(self, page: page):
        """Update the page passed in parameter."""
        page(self).update()
        self.show_page(page)
    

    def onWindowsSizeChange(self):
        """Called when the windows size change."""
        if self.__is_significant_change():
            self.__ungarded_onWindowsSizeChange()


    def __ungarded_onWindowsSizeChange(self):
        self.latest_width = self.winfo_width()
        self.latest_height = self.winfo_height()
        if self.page_frame is not None:
            self.page_frame.onSizeChange(self.winfo_width(), self.winfo_height())
        if self.menu_frame is not None:
            self.menu_frame.onSizeChange(self.winfo_width(), self.winfo_height())
            
    
    def __is_significant_change(self):
        """Return true if the change is significant."""
        return abs(self.latest_width - self.winfo_width()) > self.significant_change or abs(self.latest_height - self.winfo_height()) > self.significant_change

    # Initialize the application frame
    def init_frame(self):
        """Initialize the application frame."""

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.menu_container_frame = customtkinter.CTkFrame(self, width=UV(170))
        self.menu_container_frame.grid(row=0, column=0, sticky="nswe")    

        self.container_frame = customtkinter.CTkFrame(self)
        self.container_frame.grid(row=0, column=1, sticky="nswe")

        #self.main_frame.grid()


    def __collapse_menu(self):
        """Collapse the menu."""
        self.container_frame.grid_forget()
        self.menu_container_frame.grid_forget()
        self.container_frame.grid(row=0, column=0, columnspan = 2 ,sticky="nswe")


    def __expand_menu(self):
        """Expand the menu."""
        self.menu_container_frame.grid_forget()
        self.container_frame.grid_forget()
        self.menu_container_frame.grid(row=0, column=0, sticky="nswe")
        self.container_frame.grid(row=0, column=1, sticky="nswe")


    def toggle_menu(self):
        """Toggle the menu."""
        if self.menu_frame.winfo_ismapped():
            self.__collapse_menu()
        else:
            self.__expand_menu()
    

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