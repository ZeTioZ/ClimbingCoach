import sys
from os import path
from threading import Thread

import customtkinter as ctk
import cv2
import numpy as np
from PIL import Image

sys.path.append(path.join(path.dirname(path.dirname(path.abspath(__file__))), "src"))

root = ctk.CTk()
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

class ImageDriverCamera:
	def __init__(self, i_image: ctk.CTkLabel, video_path: str):
		self.i_image = i_image
		self.camera = cv2.VideoCapture(video_path)

	def start(self):
		while self.camera.isOpened():
			_, frame = self.camera.read()
			# self.modify_image(frame)
			cv2.imshow("test", frame)
			cv2.waitKey(1)

	def modify_image(self, image: np.ndarray):
		ctk_image = ctk.CTkImage(Image.fromarray(image), size=(500, 500))
		self.i_image.configure(image=ctk_image)


# image_composant = InteractiveImage(root, width=500, height=500)
# image_composant.pack()

label = ctk.CTkLabel(root, text="test", image=None, width=500, height=500, text_color="black")
label.pack()

placeholder = ctk.CTkButton(root, text="test", command=lambda: print("test"))
placeholder.pack()

# root.bind("<Configure>", lambda e: image_composant.change_size(e.width, e.height))

# id = ImageDriver_listener(label)

# video_path = path.join(path.dirname(path.dirname(path.abspath(__file__))),"resources","videos","Escalade_Fixe.mp4")
# camera = Camera(video_path)
# camera.flux_reader_event.register(id)
# camera.start()


video_path = path.join(path.dirname(path.dirname(path.abspath(__file__))), "resources", "videos", "Escalade_Fixe.mp4")
image_driver = ImageDriverCamera(label, video_path)
t = Thread(target=image_driver.start)
t.start()

root.mainloop()
