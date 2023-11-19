"""Module tkinter for the test page."""
import tkinter as tk
import customtkinter
from PIL import Image, ImageTk 
import os.path

import cv2
import platform

from threading import Thread
from typing import Callable
import numpy as np

from gui.abstract.page import page
from gui.utils import EMPTY_IMAGE, FONT, LIGHT_GREEN, DARK_GREEN, PRIMARY_COLOR, PRIMARY_HOVER_COLOR, SECONDARY_COLOR, SECONDARY_HOVER_COLOR
from gui.utils import v, UV, IUV, min_max_range
from gui.run_viewer_page import run_viewer_page

class run_page(page):

    __reading = False
    __thread_actif = False
    __isCameraLoaded = False
    __imageSize = None
    __model: Callable[[np.ndarray], np.ndarray] = lambda self, x: x

    """test page."""
    def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk):
        """Constructor. Singleton then init executed only once."""
        super().__init__(parent, app)

        if app is not None:
            app.title("Run Page")
            
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.grid_columnconfigure((0,1), weight=2)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=1)
        
        #Image with slider over there
        #TODO: Take the current trail image with app_state
        #self.slider = customtkinter.CTkSlider(app, from_=0, to=100, command=self.slider_event)
        #get_runs_by_user_and_route

        self.test_label = customtkinter.CTkLabel(self, text="", font=("Helvetica", 32))
        self.test_label.grid(row = 0, column = 0, columnspan = 2, sticky = "nsew")

        #Add two button
        #this button will start recording but we'll stay on this page
        self.start_recording = customtkinter.CTkButton(self, text="Start recording", command=self.__start_recording, font=(FONT, 22))
        self.start_recording.grid(row = 1, column = 0, pady = UV(10))

        self.load_recording = customtkinter.CTkButton(self, text="Load recording", command=self.__load_recording, font=(FONT, 22))
        self.load_recording.grid(row = 1, column = 1, pady = UV(10))

        self.stop_recording = customtkinter.CTkButton(self, text="Stop recording", command=self.__stop_recording, font=(FONT, 22), fg_color="red")
        
        self.show_cam = customtkinter.CTkImage(dark_image=Image.open(self.__get_icon_path("show_cam.png")), size=(25,25))
        self.hide_cam = customtkinter.CTkImage(dark_image=Image.open(self.__get_icon_path("hide_cam.png")), size=(25,25))
        self.visibility_button = customtkinter.CTkButton(self, text="", command=self.__toggle_camera, state=customtkinter.DISABLED, image=self.hide_cam, width=UV(50), height=UV(50))
        self.visibility_button.grid(row = 0, column = 2,padx = UV(10))

        self.camLoader = None

    def __get_icon_path(self, icon_name: str):
        """Return the path of the icon passed in parameter."""
        return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'resources', 'images', icon_name)
        
    def __fetch_run_list(self):
        """Fetch the run list from the database."""
        return [f"Run {i}" for i in range(1, 7)]


    def create_button(self, display_text, index):
        """Creates a button with the given text."""

        is_first = index == 0

        self.button = customtkinter.CTkButton(
            self.run_list_frame,
            text=display_text,
            fg_color= SECONDARY_COLOR if is_first else "transparent",
            hover_color=SECONDARY_COLOR,
            border_spacing=UV(17), 
            #command=,
            anchor="w"
        )

        self.button.grid(row=index, column=0, padx=UV(10), sticky="ew")
        return self.button


    def set_model(self, model: Callable[[np.ndarray], np.ndarray]):
        self.__model = model


    def __annimation_camera_loading(self):
        if not self.__thread_actif: return
        innerText = self.test_label.cget("text")
        if len(innerText) > 3: innerText = ""
        innerText += "."
        self.test_label.configure(text=innerText)
        if self.__isCameraLoaded: 
            self.test_label.configure(text="")
            return
        self.after(1000, self.__annimation_camera_loading)


    def __init_cap(self, scale_percent: int = 100):

        if not self.__thread_actif: return

        #check the os of the user
        if self.app.is_windows() or self.app.is_linux():
            video_cap = 0
        elif self.app.is_macos():
            video_cap = 1
        else:
            raise Exception("Your os is not supported")

        self.cap = cv2.VideoCapture(video_cap)
        self.baseW = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.baseH = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.__imageSize = (self.baseW, self.baseH)

        if(scale_percent != 100): self.__scale(scale_percent)

        self.__isCameraLoaded = True

        if not self.__thread_actif: return
        self.visibility_button.configure(state=customtkinter.NORMAL)
        self.app.onWindowsSizeChange()
        self.__toggle_camera()
        

    def __scale(self, scale_percent: int = 100):
        if self.cap is None: return
        rate = scale_percent/100
        self.__imageSize = (self.baseW*rate, self.baseH*rate)


    def __toggle_camera(self):
        if self.__reading or not self.__thread_actif: 
            self.__reading = False
            self.visibility_button.configure(image=self.show_cam)
            self.test_label.configure(image=EMPTY_IMAGE)
        else:
            self.__reading = True
            self.visibility_button.configure(image=self.hide_cam)
            self.__read_camera()


    def __read_camera(self):

        if not self.__reading or self.cap is None or not self.__thread_actif: return
    
        _, frame = self.cap.read() 
    
        # Convert image from one color space to other 
        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 

        model_image = self.__model(opencv_image)

        image_array = Image.fromarray(model_image)
        image_to_show = customtkinter.CTkImage(image_array, size=self.__imageSize) 
        self.test_label.configure(image=image_to_show) 
    
        self.test_label.after(10, self.__read_camera) 


    def __display_image(self, image: Image):
        """Display the image passed in parameter."""
        image_array = Image.fromarray(image)
        image_to_show = customtkinter.CTkImage(image_array, size=self.__imageSize) 
        self.test_label.configure(image=image_to_show)


    def onSizeChange(self, width, height):
        """Called when the windows size change."""
        super().onSizeChange(width, height)

        hrate = (height*0.5)/480
        wrate = (width*0.5)/640
        rate = min(hrate, wrate)
        self.__scale(rate*100) 


    def setUnactive(self):
        super().setUnactive()

        # Stop the camera
        self.__thread_actif = False
        self.__reading = False
        self.__isCameraLoaded = False
        self.visibility_button.configure(image=self.show_cam)
        if self.cap is not None:
            self.cap.release()
        
        # Set empty image
        self.test_label.configure(image=EMPTY_IMAGE)
        self.visibility_button.configure(state=customtkinter.DISABLED, image=self.show_cam)


    def setActive(self):
        super().setActive()

        # Start the camera
        self.__thread_actif = True
        self.cap = None
        self.__annimation_camera_loading()
        self.camLoader = Thread(target=self.__init_cap, args=(40,))
        self.camLoader.start()


    def get_name(self):
        return "Run"

    def __clear_run_record_frame(self):
        print("clear run record frame")
        for widget in self.run_record_frame.grid_slaves():
            widget.grid_forget()

    def __start_recording(self):
        #add logical
        if self.visibility_button.cget("image") == self.hide_cam:   
            self.start_recording.grid_forget()
            self.load_recording.grid_forget()
            self.visibility_button.grid_forget()
            self.stop_recording.grid(row = 1, column = 0, columnspan = 2, pady = UV(10))

    def __stop_recording(self):
        #add logical
        self.stop_recording.grid_forget()
        self.start_recording.grid(row = 1, column = 0, pady = UV(10))
        self.load_recording.grid(row = 1, column = 1, pady = UV(10))
        self.visibility_button.grid(row = 0, column = 2,padx = UV(10))

    def __load_recording(self):
        print("load recording")
        self.app.show_page(run_viewer_page)
        
    def __slider_event(self, event):
        print("slider event")

