import sys
from os import path
from threading import Thread
import time
from tkinter import Tk
import customtkinter as CTk
from PIL import Image
import cv2
import numpy as np
sys.path.append(path.join(path.dirname(path.dirname(path.abspath(__file__))), "src"))
from enums.flux_reader_event_type import FluxReaderEventType
from enums.event_type import EventType
from threads.camera_thread import Camera
from interfaces.event import Event
from interfaces.listener import Listener


root = CTk.CTk()
root.title("test")
root.geometry("500x700")

# class ImageDriver_listener(Listener):

#     def __init__(self, iimage: CTk.CTkLabel):

#         Listener.__init__(self, [
#             FluxReaderEventType.GET_FRAME_EVENT
#         ])
#         self.iimage = iimage

#     def update(self, observable: Event, event_types: [EventType], frame, *args, **kwargs):
#         ctkimage = CTk.CTkImage(Image.fromarray(frame))
#         self.iimage.configure(image=ctkimage)

class ImageDriver_camera():

    def __init__(self, iimage: CTk.CTkLabel, video_path: str):

        self.iimage = iimage
        self.camera = cv2.VideoCapture(video_path)
    
    def start(self):
        while self.camera.isOpened():
            _, frame = self.camera.read()
            # self.modify_image(frame)    
            cv2.imshow("test", frame)
            cv2.waitKey(1)

    def modify_image(self, image: np.ndarray):
        
        ctkimage = CTk.CTkImage(Image.fromarray(image), size=(500, 500))
        self.iimage.configure(image=ctkimage)


# image_composant = InteractiveImage(root, width=500, height=500)
# image_composant.pack()

label = CTk.CTkLabel(root, text= "test", image= None, width=500, height=500, text_color="black")
label.pack()

placeholder = CTk.CTkButton(root, text="test", command=lambda: print("test"))
placeholder.pack()

# root.bind("<Configure>", lambda e: image_composant.change_size(e.width, e.height))

# id = ImageDriver_listener(label)

# video_path = path.join(path.dirname(path.dirname(path.abspath(__file__))),"resources","videos","Escalade_Fixe.mp4")
# camera = Camera(video_path)
# camera.flux_reader_event.register(id)
# camera.start()


video_path = path.join(path.dirname(path.dirname(path.abspath(__file__))),"resources","videos","Escalade_Fixe.mp4")
id = ImageDriver_camera(label, video_path)
t = Thread(target = id.start)
t.start()


root.mainloop()