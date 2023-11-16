""""Module for tkinter interface of run page."""
import tkinter as tk
from typing import Any
import customtkinter
from gui.abstract.page import page
from PIL import Image
import os.path
from database import route_queries

from gui.utils import FONT, LIGHT_GREEN, DARK_GREEN, PRIMARY_COLOR, PRIMARY_HOVER_COLOR, SECONDARY_COLOR, SECONDARY_HOVER_COLOR, COLOR_DIFFICULTY
from gui.utils import v, UV, IUV, min_max_range

from gui.app_state import AppState

state = AppState()

RID_TITLE = 1
RID_DESCR = 2
RID_DIFFICULTY = 3

CID_LEFT = 1
CID_RIGHT = 2

class run_viewer_page(page):
    """Class of the run viewer page."""

    def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk):
        super().__init__(parent, app)

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=7)
        self.grid_rowconfigure(0, weight=0, minsize=UV(80))
        self.grid_rowconfigure(1, weight=1)

        self.run_list_frame = customtkinter.CTkScrollableFrame(self)
        self.run_list_frame.grid(row=1, column=0, sticky="nswe")
        self.run_list_frame.grid_columnconfigure(0, weight=1)

        self.run_list_title_frame = customtkinter.CTkFrame(self)
        self.run_list_title_frame.grid(row=0, column=0, sticky="nswe")
        self.run_list_title_frame.grid_columnconfigure(0, weight=1)
        self.run_list_title_frame.grid_rowconfigure(0, weight=1)

        self.run_list_title = customtkinter.CTkLabel(self.run_list_title_frame, text="Run list", font=(FONT, IUV(28), "bold"))
        self.run_list_title.grid(row=0, column=0, sticky="nswe")

        self.run_detail_frame = customtkinter.CTkScrollableFrame(self)
        self.run_detail_frame.grid(row=0, column=1, rowspan=2, sticky="nswe")
        self.run_detail_frame.configure(fg_color="transparent")

        self.run_detail_frame.grid_columnconfigure((CID_RIGHT, CID_LEFT), weight=3)
        self.run_detail_frame.grid_columnconfigure((0,3), weight=1)
        self.run_detail_frame.grid_rowconfigure((0,4), weight=0)
        self.run_detail_frame.grid_rowconfigure((RID_TITLE, RID_DIFFICULTY), weight=1)
        self.run_detail_frame.grid_rowconfigure(RID_DESCR, weight=3)


    def create_button(self, display_text, index):
        """Creates a button with the given text."""

        is_first = index == 0

        self.button = customtkinter.CTkButton(
            self.run_list_frame,
            text=display_text,
            fg_color=SECONDARY_COLOR if is_first else "transparent",
            hover_color=SECONDARY_COLOR,
            border_spacing=UV(17), 
            command=lambda : self.show_run_detail(index),
            anchor="w"
        )

        self.button.grid(row=index, column=0, padx=UV(10), sticky="ew")
        return self.button


    def show_run_detail(self, run_choosed):
        """Shows the run detail page."""
        pass


    def __skeleton_loader(self, image_name: str):
        pass


    def __get_run_path(self, run_image_name: str):
        """Return the path of the run passed in parameter."""
        pass


    def onSizeChange(self, width, height):
        super().onSizeChange(width, height)

        image_size = min_max_range(UV(75), UV(1000), v(22, width))
        self.run_image.configure(size=(image_size, image_size))
        self.run_label.configure(height=IUV(image_size), width=IUV(image_size))

        font_style_default = (FONT, min_max_range(IUV(8), IUV(28), int(v(1.9, width))))
        font_style_title = (FONT, min_max_range(IUV(12), IUV(32), int(v(2.5, width))), "bold")

        self.run_selection_button.configure(height=v(5, height), width=image_size, font=font_style_default)
        #self.detail_description.configure(font=font_style_default)

        for button in self.button_list:
            button.configure(height=v(5, height), width=image_size, font=font_style_default)
        self.run_list_title.configure(font=font_style_title)

        size_difficulty = min_max_range(UV(15), UV(100), v(2.5, width))
        for i in range(5):
            self.difficulty[i].configure(width=size_difficulty, height=size_difficulty)
        

    def get_name(self):
        return "Run selection"

