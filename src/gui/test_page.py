"""Module tkinter for the test page."""
import tkinter as tk
import customtkinter
from PIL import Image, ImageTk 

import cv2
import platform

from threading import Thread
from typing import Callable
import numpy as np

from gui.abstract.page import Page
from gui.utils import EMPTY_IMAGE

class run_page(Page):

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
            app.title("test Page")

        parent.grid_rowconfigure(0, weight=1) 
        parent.grid_columnconfigure(0, weight=1)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=1)

        self.test_label = customtkinter.CTkLabel(self, text="", font=("Helvetica", 32))
        self.test_label.grid(row = 0, column = 0)

        self.test_button = customtkinter.CTkButton(self, text="start", command=self.__toggle_camera, state=customtkinter.DISABLED)
        self.test_button.grid(row = 1, column = 0)

        self.camLoader = None


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


