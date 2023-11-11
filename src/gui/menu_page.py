""""Module for tkinter interface of menu page."""
import tkinter as tk
import customtkinter
from gui.page import page
from PIL import Image

from gui.utils import v, min_max_range, IUV, UV, PRIMARY_COLOR, SECONDARY_COLOR, SECONDARY_HOVER_COLOR, EMPTY_IMAGE

from gui.db import db as dbclass

import os.path

db = dbclass()

DEFAULT_RADIUS = 12
COLOR = PRIMARY_COLOR #"#0b7687"

DEFAULT_RADIUS_ACTIVE = 4
COLOR_ACTIVE = SECONDARY_COLOR #"#2ab9d4"


class menu_page(page):
    """Class of the menu page"""

    __active_elem = None

    def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk):
        super().__init__(parent, app)

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((1,2,3,4), weight=1)
        self.grid_rowconfigure((0,5), weight=6)

        #initialize logo

        self.piste = customtkinter.CTkImage(dark_image=Image.open(self.__get_icon_path("piste_light.png")), size=(80,80))
        self.piste_label = customtkinter.CTkLabel(self, text="", font=("Helvetica", 20, "bold"), image=self.piste, height=100, width=100, fg_color=COLOR, corner_radius=DEFAULT_RADIUS)
        self.piste_label.grid(row=1, column=0, pady=(10, 10), padx=(10, 10))
        self.__set_hover_effect(self.piste_label, self.piste, "Trail")

        self.chemin = customtkinter.CTkImage(dark_image=Image.open(self.__get_icon_path("chemin_light.png")), size=(80,80))
        self.chemin_label = customtkinter.CTkLabel(self, text="", font=("Helvetica", 20, "bold"), image=self.chemin, height=100, width=100, fg_color=COLOR, corner_radius=DEFAULT_RADIUS)
        self.chemin_label.grid(row=2, column=0, padx=(10, 10))
        self.__set_hover_effect(self.chemin_label, self.chemin, "Route")

        self.run = customtkinter.CTkImage(dark_image=Image.open(self.__get_icon_path("run_light.png")), size=(80,80))
        self.run_label = customtkinter.CTkLabel(self, text="", font=("Helvetica", 20, "bold"), image=self.run, height=100, width=100, fg_color=COLOR, corner_radius=DEFAULT_RADIUS)
        self.run_label.grid(row=3, column=0, pady=(10, 10), padx=(10, 10))
        self.__set_hover_effect(self.run_label, self.run, "Run")

        self.compte = customtkinter.CTkImage(dark_image=Image.open(self.__get_icon_path("compte_light.png")), size=(80,80))
        self.compte_label = customtkinter.CTkLabel(self, text="", font=("Helvetica", 20, "bold"), image=self.compte, height=100, width=100, fg_color=COLOR, corner_radius=DEFAULT_RADIUS)
        self.compte_label.grid(row=4, column=0, pady=(0, 10), padx=(10, 10))
        self.__set_hover_effect(self.compte_label, self.compte, "My\nspace")

        entry = self.piste_label

        self.__change_active(entry)

        self.refresh_hide_show()
    

    def refresh_hide_show(self):
        """Refresh hide and show."""
        if db.get_trail() is None:
            self.hide_chemin()
        else:
            self.show_chemin()


    def set_command_piste(self, command):
        self.__set_on_click(self.piste_label, lambda e: command())


    def hide_piste(self):
        self.piste_label.grid_forget()


    def show_piste(self):
        self.piste_label.grid(row=1, column=0, pady=(10, 10), padx=(10, 10))


    def set_command_chemin(self, command):
        self.__set_on_click(self.chemin_label, lambda e: command())


    def hide_chemin(self):
        self.chemin_label.grid_forget()
    

    def show_chemin(self):
        self.chemin_label.grid(row=2, column=0, padx=(10, 10))


    def set_command_run(self, command):
        self.__set_on_click(self.run_label, lambda e: command())


    def set_command_compte(self, command):
        self.__set_on_click(self.compte_label, lambda e: command())


    def __change_active(self, elem: customtkinter.CTkLabel):
            """Change the active element."""
            if self.__active_elem is not None:
                self.__active_elem.configure(fg_color = COLOR, corner_radius= DEFAULT_RADIUS)
            elem.configure(fg_color = COLOR_ACTIVE, corner_radius= DEFAULT_RADIUS_ACTIVE)
            self.__active_elem = elem


    def __get_icon_path(self, icon_name: str):
        """Return the path of the icon passed in parameter."""
        return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'resources\\images', icon_name)


    def __set_hover_effect(self, elem: customtkinter.CTkLabel, image: customtkinter.CTkImage, hover_text: str):
        """Set the hover effect on the label passed in parameter."""
        elem.bind("<Enter>", lambda e: elem.configure(text=hover_text, image=EMPTY_IMAGE))
        elem.bind("<Leave>", lambda e: elem.configure(image=image, text=""))


    def __set_on_click(self, elem: customtkinter.CTkLabel, on_click = lambda e: print("Please implement the on click function")):
        """Set the on click function on the label passed in parameter."""
        def extended_on_click(e):
            self.__change_active(elem)
            on_click(e)
        elem.bind("<Button-1>", extended_on_click)


    def update(self, *args, **kwargs):
        """Update the page."""
        if db.get_trail() is not None:
            self.show_chemin()
        else:
            self.hide_chemin()


    def onSizeChange(self, width, height):
        """Called when the windows size change."""

        size_icon = min_max_range(UV(60), UV(80), v(5.5, width))
        size_label_icon = 115/80 * size_icon
        #min(int(v(1.7, width)), 32)
        default_font = ("Helvetica", min_max_range(IUV(22), IUV(30), int(v(1.7, width))), "bold")

        def set_size(label: customtkinter.CTkLabel, image: customtkinter.CTkImage):
            label.configure(height = size_label_icon, width = size_label_icon, font= default_font)
            image.configure(size = (size_icon,size_icon))
        set_size(self.piste_label, self.piste)
        set_size(self.chemin_label, self.chemin)
        set_size(self.run_label, self.run)
        set_size(self.compte_label, self.compte)