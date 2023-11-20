from enum import Enum
from typing import Any
import customtkinter as CTk
from tkinter import Event
from PIL import Image
from os import path

from enums.image_event_type import ImageEventType
from enums.event_type import EventType
from enums.click_type import ClickType
from interfaces.event import Event
from interfaces.listener import Listener
from models.hold_detector import HoldDetector
from objects.box import Box

from utils.click import find_selected_hold


class printer(Listener):
    """Class to print the event."""

    def __init__(self):
        """Constructor."""
        super().__init__()

    def update(self, event: Event, event_types: [EventType], *args, **kwargs):
        """
        Called when the event notify the observer.
        """
        if ImageEventType.CLICK_EVENT in event_types:
            click_type: ClickType = event.click_type
            if click_type == ClickType.LEFT_CLICK:
                if (type(event) == image_clickable):  
                    selected_hold = find_selected_hold(event.model.get_holds() ,*args)
                    if selected_hold is not None:
                        event.add_box_path(selected_hold)
                        event.refresh_image()
                else:
                    print("not the right event")
            elif click_type == ClickType.RIGHT_CLICK:
                print(f"right click: {args}")
            else:
                print(f"unknown click type: {click_type}")


class image_clickable(CTk.CTkLabel, Event):
    """Class to create a clickable image."""

    path: list[Box] = []

    def __init__(self, parent: CTk.CTkFrame, model: HoldDetector,  image: Image, width: int, height: int):
        """Constructor."""
        self.model = model

        self.image = image
        self.default_size = image.size # (width, height)
        image_processed = self.model.apply_model_on_image(image)

        self.ctkimage = CTk.CTkImage(image_processed, size= (width, height))

        super().__init__(parent, text= "", image= self.ctkimage)
        Event.__init__(self)

        self.bind("<Button-1>", self.__click_left)
        self.bind("<Button-3>", self.__click_right)


    def change_image(self, image: Image.Image):
        del self.ctkimage
        self.ctkimage = CTk.CTkImage(image, size= (self.winfo_width(), self.winfo_height()))
        self.configure(image= self.ctkimage)

    
    def refresh_image(self):
        """Refresh the image."""
        self.change_image(self.model.apply_model_on_image(self.image, path= self.path))


    def register(self, listener: Listener):
        """Register an listener. Override from CTkLabel."""
        Event.register(self, listener)


    def add_box_path(self, box: Box):
        """Add a box to the path."""
        self.path.append(box)

    
    def change_size(self, width: int, height: int):
        """Change the size of the image."""
        self.configure(width= width, height= height)
        self.__resize_image(width, height)

    
    def __resize_image(self, width: int, height: int):
        """Resize the image."""
        self.ctkimage.configure(size= (width, height))
        self.configure(image= self.ctkimage)


    def __click_left(self, event: Event):
        """Called when the image is clicked."""
        default_X = int(self.default_size[0] * event.x / self.winfo_width())
        default_Y = int(self.default_size[1] * event.y / self.winfo_height())
        self.notify(ClickType.LEFT_CLICK, default_X, default_Y)

    
    def __click_right(self, event: Event):
        """Called when the image is clicked."""
        self.notify(ClickType.RIGHT_CLICK, event.x, event.y, self.winfo_width(), self.winfo_height())


if(__name__ == "__main__"):
    from tkinter import Tk
    from PIL import Image

    root = Tk()
    root.title("test")
    root.geometry("500x500")

    image = Image.open(path.join(path.dirname(path.dirname(path.abspath(__file__))),"resources","images","trail_1.jpg"))

    image_composant = image_clickable(root, HoldDetector(), image, width=500, height=500)
    image_composant.pack()


    printer1 = printer()
    image_composant.register(printer1)

    root.mainloop()