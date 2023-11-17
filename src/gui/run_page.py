"""Module tkinter for the test page."""
import tkinter as tk
import customtkinter
from PIL import Image, ImageTk 

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

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=1)
        
        #Image with slider over there
        #TODO: Take the current trail image with app_state
        self.slider = customtkinter.CTkSlider(app, from_=0, to=100, command=self.slider_event)
        #get_runs_by_user_and_route

        #Add two button
        #this button will start recording but we'll stay on this page
        self.start_recording = customtkinter.CTkButton(self, text="start recording", command=self.__start_recording)
        self.test_label.grid(row = 0, column = 0)

        self.load_recording = customtkinter.CTkButton(self, text="load recording", command=self.__load_recording)
        self.load_recording.grid(row = 0, column = 1)
        
        self.test_button = customtkinter.CTkButton(self, text="start", command=self.__toggle_camera, state=customtkinter.DISABLED)
        self.test_button.grid(row = 1, column = 0)

        self.camLoader = None
        
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
        self.test_button.configure(state=customtkinter.NORMAL)
        self.app.onWindowsSizeChange()
        self.__toggle_camera()
        

    def __scale(self, scale_percent: int = 100):
        if self.cap is None: return
        rate = scale_percent/100
        self.__imageSize = (self.baseW*rate, self.baseH*rate)


    def __toggle_camera(self):
        if self.__reading or not self.__thread_actif: 
            self.__reading = False
            self.test_button.configure(text="start")
            self.test_label.configure(image=EMPTY_IMAGE)
        else:
            self.__reading = True
            self.test_button.configure(text="stop")
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
        self.test_button.configure(text="start")
        if self.cap is not None:
            self.cap.release()
        
        # Set empty image
        self.test_label.configure(image=EMPTY_IMAGE)
        self.test_button.configure(state=customtkinter.DISABLED, text="start")


    def setActive(self):
        super().setActive()

        # Start the camera
        self.__thread_actif = True
        self.cap = None
        self.__annimation_camera_loading()
        self.camLoader = Thread(target=self.__init_cap, args=(40,))
        self.camLoader.start()


    def get_name(self):
        return "test"

    def __start_recording(self):
        print("start recording")

    def __clear_run_record_frame(self):
        print("clear run record frame")
        for widget in self.run_record_frame.grid_slaves():
            widget.grid_forget()

    def __load_recording(self):
        print("load recording")
        self.show_page(run_viewer_page)
        #self.__clear_run_record_frame()
        
    def __slider_event(self, event):
        print("slider event")
