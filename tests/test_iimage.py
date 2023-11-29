import sys
from os import path
import threading
from tkinter import Tk
import customtkinter as CTk
# from src.threads.camera_thread import Camera
# from src.gui.component.interactive_image import InteractiveImage
# from src.listeners.image_driver import ImageDriver
# from src.database.database_handler import DatabaseHandler
sys.path.append(path.join(path.dirname(path.dirname(path.abspath(__file__))), "src"))
from threads.camera_thread import Camera
from gui.component.interactive_image import InteractiveImage
from listeners.image_driver import ImageDriver
from database.database_handler import DatabaseHandler

def save(id: ImageDriver, name: str):
	id.route_set_name(name)
	id.save_route()

root = Tk()
root.title("test")
root.geometry("500x700")

database = DatabaseHandler()
database.create_tables()

image_composant = InteractiveImage(root, width=500, height=500)
image_composant.pack()

load_btn = CTk.CTkButton(root, text="Load")
load_btn.pack()

save_btn = CTk.CTkButton(root, text="Save")
save_btn.pack()

# root.bind("<Configure>", lambda e: image_composant.change_size(e.width, e.height))
id = ImageDriver(image_composant)

load_btn.configure(command=lambda: id.load_route("test"))
save_btn.configure(command=lambda: save(id, "test"))

video_path = path.join(path.dirname(path.dirname(path.abspath(__file__))), "resources", "videos", "Escalade_Fixe.mp4")
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
