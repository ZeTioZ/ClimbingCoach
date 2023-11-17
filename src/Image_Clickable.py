from collections.abc import Callable, Sequence
from enum import Enum
from typing import Any
import customtkinter as CTk
from tkinter import Event
from PIL import Image
from os import path

from interfaces.observable import Observable
from interfaces.observer import Observer
from models.hold_detector import apply_model_on_image

class image_clickable_enum(Enum):

    LEFT_CLICK = 1 # arg: x_coord, y_coord, width, height
    RIGHT_CLICK = 2 # arg: x_coord, y_coord, width, height


class printer(Observer):
    """Class to print the event."""

    def __init__(self):
        """Constructor."""
        super().__init__()

    def update(self, observable: Observable, event_type, *args, **kwargs):
        """Called when the observable notify the observer."""
        if event_type == image_clickable_enum.LEFT_CLICK:
            print(f"left click: {args}")
        elif event_type == image_clickable_enum.RIGHT_CLICK:
            print(f"right click: {args}")
        else:
            print(f"unknown event: {event_type}")


class image_clickable(CTk.CTkLabel, Observable):
    """Class to create a clickable image."""

    def __init__(self, parent: CTk.CTkFrame, model: Callable[[Image.Image], Image.Image],  image: Image, width: int, height: int):
        """Constructor."""

        image_processed = model(image)

        self.image = CTk.CTkImage(image_processed, size= (width, height))

        super().__init__(parent, text= "", image= self.image)
        Observable.__init__(self)

        self.bind("<Button-1>", self.__click_left)
        self.bind("<Button-3>", self.__click_right)


    def change_image(self, image: Image.Image):
        del self.image
        self.image = CTk.CTkImage(image, size= (self.winfo_width(), self.winfo_height()))
        self.configure(image= self.image)



    def register(self, observer: Observer):
        """Register an observer. Override from CTkLabel."""
        Observable.register(self, observer)


    def __click_left(self, event: Event):
        """Called when the image is clicked."""
        self.notify(image_clickable_enum.LEFT_CLICK, event.x, event.y, self.winfo_width(), self.winfo_height())

    
    def __click_right(self, event: Event):
        """Called when the image is clicked."""
        self.notify(image_clickable_enum.RIGHT_CLICK, event.x, event.y, self.winfo_width(), self.winfo_height())


if(__name__ == "__main__"):
    from tkinter import Tk
    from PIL import Image

    root = Tk()
    root.title("test")
    root.geometry("500x500")

    image = Image.open(path.join(path.dirname(path.dirname(path.abspath(__file__))),"resources","images","image0.jpg"))

    image_composant = image_clickable(root, apply_model_on_image,image , width=300, height=300)
    image_composant.pack()


    printer1 = printer()
    Observable.register(image_composant, printer1)

    root.mainloop()