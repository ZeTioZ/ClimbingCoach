from collections.abc import Callable, Sequence
from enum import Enum
from typing import Any
import customtkinter as CTk
from tkinter import Event
from PIL import Image
from os import path

from interfaces.observable import Observable
from interfaces.observer import Observer
from models.hold_detector import HoldDetector
from objects.box import Box

from utils.click import find_selected_hold

class image_clickable_enum(Enum):

    LEFT_CLICK = 1 # arg: x_coord, y_coord
    RIGHT_CLICK = 2 # arg: x_coord, y_coord


class printer(Observer):
    """Class to print the event."""

    path: list[Box] = []

    def __init__(self):
        """Constructor."""
        super().__init__()

    def update(self, observable: Observable, event_type, *args, **kwargs):
        """Called when the observable notify the observer."""
        if (not type(observable) == image_clickable):
            print("not the right observable")
            return
        if event_type == image_clickable_enum.LEFT_CLICK:
            selected_hold = find_selected_hold(observable.model.get_holds() ,*args)
            if selected_hold is not None:
                self.__add_box_to_path(selected_hold)
                observable.refresh_image(self.path)
        
        elif event_type == image_clickable_enum.RIGHT_CLICK:
            selected_hold = find_selected_hold(observable.model.get_holds() ,*args)
            if selected_hold is not None:
                self.__remove_box_from_path(selected_hold)
                observable.refresh_image(self.path)
        else:
            print(f"unknown event: {event_type}")

    def __add_box_to_path(self, box: Box):
        """Add a box to the path."""
        if(not box in self.path): self.path.append(box)
    
    def __remove_box_from_path(self, box: Box):
        """Remove a box from the path."""
        if(box in self.path): self.path.remove(box)


class image_clickable(CTk.CTkLabel, Observable):
    """Class to create a clickable image."""

    def __init__(self, parent: CTk.CTkFrame, model: HoldDetector,  image: Image, width: int, height: int):
        """Constructor."""
        self.model = model

        self.image = image
        self.default_size = image.size # (width, height)
        image_processed = self.model.apply_model_on_image(image)

        self.ctkimage = CTk.CTkImage(image_processed, size= (width, height))

        super().__init__(parent, text= "", image= self.ctkimage)
        Observable.__init__(self)

        self.bind("<Button-1>", self.__click_left)
        self.bind("<Button-3>", self.__click_right)


    def change_image(self, image: Image.Image):
        del self.ctkimage
        self.ctkimage = CTk.CTkImage(image, size= (self.winfo_width(), self.winfo_height()))
        self.configure(image= self.ctkimage)

    
    def refresh_image(self, path: list[Box]):
        """Refresh the image."""
        self.change_image(self.model.apply_model_on_image(self.image, path= path))


    def register(self, observer: Observer):
        """Register an observer. Override from CTkLabel."""
        Observable.register(self, observer)

    
    def change_size(self, width: int, height: int):
        """Change the size of the image."""
        self.configure(width= width, height= height)
        self.__resize_image(width, height)

    
    def __resize_image(self, width: int, height: int):
        """Resize the image."""
        self.ctkimage.configure(size= (width, height))
        self.configure(image= self.ctkimage)


    def __click_right(self, event: Event):
        """Called when the image is clicked."""
        self.__click(event, image_clickable_enum.RIGHT_CLICK)


    def __click_left(self, event: Event):
        """Called when the image is clicked."""
        self.__click(event, image_clickable_enum.LEFT_CLICK)


    def __click(self, event: Event, event_type: image_clickable_enum):
        """Called when the image is clicked."""
        default_X = int(self.default_size[0] * event.x / self.winfo_width())
        default_Y = int(self.default_size[1] * event.y / self.winfo_height())
        self.notify(event_type, default_X, default_Y)

if(__name__ == "__main__"):
    from tkinter import Tk
    from PIL import Image

    root = Tk()
    root.title("test")
    root.geometry("500x500")

    root.bind("<Configure>", lambda e: image_composant.change_size(e.width, e.height))

    image = Image.open(path.join(path.dirname(path.dirname(path.abspath(__file__))),"resources","images","trail_1.jpg"))

    image_composant = image_clickable(root, HoldDetector(), image, width=500, height=500)
    image_composant.pack()


    printer1 = printer()
    image_composant.register(printer1)

    

    root.mainloop()