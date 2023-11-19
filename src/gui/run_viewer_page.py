""""Module for tkinter interface of run page."""
import tkinter as tk
from typing import Any
import customtkinter
from gui.abstract.page import page
from PIL import Image
import os.path
from database import route_queries


from gui.utils import FONT, SECONDARY_COLOR
from gui.utils import v, UV, IUV, min_max_range

from gui.app_state import AppState

state = AppState()

class run_viewer_page(page):
    """Class of the run viewer page."""

    def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk = None):
        super().__init__(parent, app)

        self.app = app

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=7)
        self.grid_rowconfigure((0,2), weight=0, minsize=UV(80))
        self.grid_rowconfigure(1, weight=1)

        self.run_list_frame = customtkinter.CTkScrollableFrame(self, width=UV(170))
        self.run_list_frame.grid(row=1, column=0, sticky="nswe")
        self.run_list_frame.grid_columnconfigure((0,1), weight=1)

        self.run_list_title = customtkinter.CTkLabel(self, text="Run list", font=(FONT, IUV(28), "bold"))
        self.run_list_title.grid(row=0, column=0, sticky="nswe")

        self.run_back_button = customtkinter.CTkButton(self, text="Back", width=UV(100)
                                                       , command= self.__show_run_page
                                                       )
        self.run_back_button.grid(row=2, column=0, sticky="w")

        self.run_add_button = customtkinter.CTkButton(self, text="Add", width=UV(100)
                                                      #, command=lambda : self.app.change_page("AddRun")
                                                      )
        self.run_add_button.grid(row=2, column=0, sticky="e")

        self.run_detail_frame = customtkinter.CTkScrollableFrame(self, width=UV(170), bg_color="transparent")
        self.run_detail_frame.grid(row=0, column=1, rowspan=2, sticky="nswe")
        self.run_detail_frame.configure(fg_color="transparent")

        self.run_detail_frame.grid_columnconfigure((0,1,2,3), weight=1)
        self.run_detail_frame.grid_rowconfigure(0, weight=4)
        self.run_detail_frame.grid_rowconfigure((1,2,3,4), weight=1)

        self.run_detail_title = customtkinter.CTkLabel(self.run_detail_frame, text="Run 1", font=(FONT, IUV(28), "bold"))
        self.run_detail_title.grid(row=0, column=0, columnspan=4)

        self.video_player_img = customtkinter.CTkImage(Image.open(os.path.join("resources", "images", "video_player.png")), size=(200,200))
        self.video_player = customtkinter.CTkLabel(self.run_detail_frame, image=self.video_player_img, bg_color="transparent", text="")
        self.video_player.grid(row=2, column=0, columnspan=4)

        self.video_commands_frame = customtkinter.CTkFrame(self.run_detail_frame, bg_color="transparent")
        self.video_commands_frame.grid(row=3, column=0, columnspan=4, pady=UV(10))
        self.video_commands_frame.grid_columnconfigure((0,1), weight=1)

        self.video_play_button_img = customtkinter.CTkImage(Image.open(os.path.join("resources", "images", "play_button.png")), size=(30,30))
        self.video_pause_button_img = customtkinter.CTkImage(Image.open(os.path.join("resources", "images", "pause_button.png")), size=(30,30))
        self.video_play_button = customtkinter.CTkButton(self.video_commands_frame, text="", width=UV(40), image=self.video_play_button_img, bg_color="transparent", command=self.__change_video_state)
        self.video_play_button.grid(row=0, column=0, sticky="w")
        self.video_progressbar = customtkinter.CTkSlider(self.video_commands_frame, from_=0, to=100)
        self.video_progressbar.grid(row=0, column=1, pady=UV(10))

        self.run_detail_description = customtkinter.CTkLabel(self.run_detail_frame, text="Run informations", font=(FONT, IUV(32)))
        self.run_detail_description.grid(row=4, column=0, columnspan=4)

        self.run_information_frame = customtkinter.CTkFrame(self.run_detail_frame, bg_color="transparent")
        self.run_information_frame.grid(row=5, column=0, columnspan=4, sticky="nswe",padx=UV(20), pady=UV(20))
        self.run_information_frame.grid_columnconfigure((0,1), weight=1)

        self.user_record_label = customtkinter.CTkLabel(self.run_information_frame, text="User record", font=(FONT, IUV(26)))
        self.user_record_label.grid(row=0, column=0)

        self.all_time_record_label = customtkinter.CTkLabel(self.run_information_frame, text="All time record", font=(FONT, IUV(26)))
        self.all_time_record_label.grid(row=0, column=1)

        #get all the run in the db
        run_list= self.__fetch_run_list()
        user_record_list = self.__get_user_record()
        all_time_record_list = self.__get_all_time_record()

        self.button_list: list[customtkinter.CTkButton] = []
        for run in run_list:
            self.run_button = self.create_button(run, run_list.index(run))
            self.button_list.append(self.run_button)

        self.user_record_button_list: list[customtkinter.CTkButton] = []
        for user_record in user_record_list:
            self.record_button = self.create_label(user_record, (user_record_list.index(user_record))+1,0)
            self.user_record_button_list.append(self.record_button)

        self.all_time_record_button_list: list[customtkinter.CTkButton] = []
        for all_time_record in all_time_record_list:
            self.all_time_record_button = self.create_label(all_time_record, (all_time_record_list.index(all_time_record))+1,1)
            self.all_time_record_button_list.append(self.all_time_record_button)

    def __get_user_record(self):
        """Return the user record of the run."""
        return [f"User record {i}" for i in range(1, 3)]
    

    def __get_all_time_record(self):
        """Return the all time record of the run."""
        return [f"All time record {i}" for i in range(1, 3)]
        

    def __change_video_state(self):
        """Change the state of the video."""
        if self.video_play_button.cget("image") == self.video_play_button_img:
            self.video_play_button.configure(image=self.video_pause_button_img)
        else:
            self.video_play_button.configure(image=self.video_play_button_img)


    def __show_run_page(self):
        """Show the page passed in parameter."""
        from gui.run_page import run_page

        if self.app is not None:
            self.app.show_page(run_page)


    def create_label(self, display_text, index, column):
        """Creates a label with the given text."""

        self.label = customtkinter.CTkLabel(
            self.run_information_frame,
            text=display_text,
        )

        self.label.grid(row=index, column=column, padx=UV(10), sticky="ew")
        return self.label

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


    def __fetch_run_list(self):
        """Fetch the run list from the database."""
        return [f"Run {i}" for i in range(1, 13)]
        #return [f"Run {run}" for run in route_queries.get_all_routes()]


    def __skeleton_loader(self, image_name: str):
        pass


    def __get_run_path(self, run_image_name: str):
        """Return the path of the run passed in parameter."""
        pass


    def onSizeChange(self, width, height):
        super().onSizeChange(width, height)

        image_size = min_max_range(UV(75), UV(1000), v(22, width))
        #self.run_image.configure(size=(image_size, image_size))
        #self.run_label.configure(height=IUV(image_size), width=IUV(image_size))

        font_style_default = (FONT, min_max_range(IUV(8), IUV(28), int(v(1.9, width))))
        font_style_title = (FONT, min_max_range(IUV(12), IUV(32), int(v(2.5, width))), "bold")

        #self.run_selection_button.configure(height=v(5, height), width=image_size, font=font_style_default)
        #self.detail_description.configure(font=font_style_default)

        #for button in self.button_list:
        #    button.configure(height=v(5, height), width=image_size, font=font_style_default)
        self.run_list_title.configure(font=font_style_title)

        size_difficulty = min_max_range(UV(15), UV(100), v(2.5, width))
        

    def get_name(self):
        return "Run selection"

