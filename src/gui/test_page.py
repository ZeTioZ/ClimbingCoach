"""Module tkinter for the test page."""
import tkinter as tk
import customtkinter
from gui.page import page
import cv2
from PIL import Image, ImageTk 

import platform
from threading import Thread
from typing import Callable
import numpy as np

class test_page(page):

    __reading = False
    __isCameraLoaded = False
    __imageSize = None
    __model: Callable[[np.ndarray], np.ndarray] = lambda self, x: x

    """test page."""
    def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk, *args, **kwargs):
        """Constructor. Singleton then init executed only once."""
        super().__init__(parent)

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

        self.cap = None
        self.__annimation_camera_loading()
        camLoader = Thread(target=self.__init_cap, args=(40,app))
        camLoader.start()

    def set_model(self, model: Callable[[np.ndarray], np.ndarray]):
        self.__model = model

    def __annimation_camera_loading(self):
        
        innerText = self.test_label.cget("text")
        if len(innerText) > 3: innerText = ""
        innerText += "."
        self.test_label.configure(text=innerText)
        if self.__isCameraLoaded: 
            self.test_label.configure(text="")
            return
        self.after(1000, self.__annimation_camera_loading)
     
    def __init_cap(self, scale_percent: int = 100, app: customtkinter.CTk = None):
        #check the os of the user
        if platform.system() == "Darwin": #Means Mac
            video_cap = 1
        else:
            #Check if it works on linux
            video_cap = 0

        self.cap = cv2.VideoCapture(video_cap)
        self.baseW = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.baseH = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.__imageSize = (self.baseW, self.baseH)

        if(scale_percent != 100): self.__scale(scale_percent)
        
        self.__isCameraLoaded = True
        self.test_button.configure(state=customtkinter.NORMAL)
        self.__toggle_camera()
        if app is not None: self.onSizeChange(app.winfo_width(), app.winfo_height())

    def __scale(self, scale_percent: int = 100):
        if self.cap is None: return
        rate = scale_percent/100
        self.__imageSize = (self.baseW*rate, self.baseH*rate)

    def __toggle_camera(self): 
        if self.__reading: 
            self.__reading = False
            self.test_button.configure(text="start")
            self.test_label.configure(image=customtkinter.CTkImage(Image.frombytes("RGBA", (1,1), b"\x00\x00\x00\x00")))
        else:
            self.__reading = True
            self.test_button.configure(text="stop")
            self.__read_camera()

    def __read_camera(self):

        if not self.__reading or self.cap is None: return
    
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
        hrate = (height*0.5)/480
        wrate = (width*0.5)/640
        rate = min(hrate, wrate)
        self.__scale(rate*100) 

    def setUnactive(self):
        super().setUnactive()

        # Stop the camera
        self.__reading = False
        self.test_button.configure(text="start")


