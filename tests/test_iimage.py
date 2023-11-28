import sys
from os import path
import threading
import time
from tkinter import Tk
from PIL import Image
sys.path.append(path.join(path.dirname(path.dirname(path.abspath(__file__))), "src"))
from threads.camera_thread import Camera
from gui.component.interactive_image import InteractiveImage
from listeners.image_driver import ImageDriver


root = Tk()
root.title("test")
root.geometry("500x500")


image_composant = InteractiveImage(root, width=500, height=500)
image_composant.pack()

root.bind("<Configure>", lambda e: image_composant.change_size(e.width, e.height))

id = ImageDriver(image_composant)

video_path = 0# path.join(path.dirname(path.dirname(path.abspath(__file__))),"resources","videos","Escalade_Fixe.mp4")
camera = Camera(video_path)
camera.flux_reader_event.register(id)
camera.start()


def change_image():
    if id.image is not None:
        id.change_image(id.holds, id.image)
    id.i_image.after(10, change_image)

thread = threading.Thread(target=change_image)
thread.start()
root.mainloop()

