from typing import Any
import customtkinter as CTk
from tkinter import Event
from PIL.Image import Image
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

    path: list[Box] = []

    def __init__(self):
        """Constructor."""
        super().__init__([ImageEventType.CLICK_EVENT])

    def update(self, event: Event, event_types: [EventType], *args, **kwargs):
        """
        Called when the event notify the observer.
        """
        if ImageEventType.CLICK_EVENT in event_types and isinstance(event, InteractiveImage):
            click_type: ClickType = args[0]
            x: int = args[1]
            y: int = args[2]
            if click_type == ClickType.LEFT_CLICK:
                selected_hold = find_selected_hold(event.model.get_holds(), x, y)
                if selected_hold is not None:
                    self.__add_box_to_path(selected_hold)
                    event.refresh_image(self.path)
            elif click_type == ClickType.RIGHT_CLICK:
                selected_hold = find_selected_hold(event.model.get_holds(), x, y)
                if selected_hold is not None:
                    self.__remove_box_from_path(selected_hold)
                    event.refresh_image(self.path)
            else:
                print("unknown click type:")

    def __add_box_to_path(self, box: Box):
        """Add a box to the path."""
        if(box not in self.path): self.path.append(box)
    
    def __remove_box_from_path(self, box: Box):
        """Remove a box from the path."""
        if(box in self.path): self.path.remove(box)


class ImageDriver(Event):

    def __init__(self):
        super().__init__()


    def register(self, listener: Listener):
        """Register an listener. Override from CTkLabel."""
        Event.register(self, listener)


    def click_right(self, event):
        """Called when the image is clicked."""
        self.__click(event, ClickType.RIGHT_CLICK)


    def click_left(self, event):
        """Called when the image is clicked."""
        self.__click(event, ClickType.LEFT_CLICK)


    def __click(self, event, click_type: ClickType):
        """Called when the image is clicked."""
        default_x = int(self.default_size_width * event.x / self.winfo_width())
        default_y = int(self.default_size_height * event.y / self.winfo_height())
        self.notify([ImageEventType.CLICK_EVENT], click_type, default_x, default_y)


class InteractiveImage(CTk.CTkLabel, Event):
    """Class to create a clickable image."""

    def __init__(self, parent: CTk.CTkFrame, model: HoldDetector, image: Image, width: int = None, height: int = None):
        """Constructor."""

        self.model = model
        self.image = image
        self.default_size_width, self.default_size_height = image.size # (width, height)
        image_processed = self.model.apply_model_on_image(image)

        if(width is None or height is None):
            width, height = self.default_size_width, self.default_size_height

        self.ctkimage = CTk.CTkImage(image_processed, size= (width, height))

        super().__init__(parent, text= "", image= self.ctkimage)
        Event.__init__(self)

        self.bind("<Button-1>", self.__click_left)
        self.bind("<Button-3>", self.__click_right)


    def change_image(self, image: Image):
        del self.ctkimage
        self.__load_image(image=image)

    
    def __load_image(self, image: Image):
        self.image = image
        self.default_size_width, self.default_size_height = image.size # (width, height)
        self.ctkimage = CTk.CTkImage(image, size= (self.winfo_width(), self.winfo_height()))
        self.configure(image= self.ctkimage)

    
    def refresh_image(self, path: list[Box]):
        """Refresh the image."""
        self.change_image(self.model.apply_model_on_image(self.image, path= path))


    def change_size(self, width: int, height: int):
        """Change the size of the image."""
        self.configure(width= width, height= height)
        self.__resize_image(width, height)

    
    def __resize_image(self, width: int, height: int):
        """Resize the image."""
        self.ctkimage.configure(size= (width, height))
        self.configure(image= self.ctkimage)


if(__name__ == "__main__"):
    from tkinter import Tk
    from PIL import Image

    root = Tk()
    root.title("test")
    root.geometry("500x500")

    root.bind("<Configure>", lambda e: image_composant.change_size(e.width, e.height))

    image = Image.open(path.join(path.dirname(path.dirname(path.abspath(__file__))),"resources","images","trail_1.jpg"))

    image_composant = InteractiveImage(root, HoldDetector(), image, width=500, height=500)
    image_composant.pack()


    printer1 = printer()
    image_composant.register(printer1)

    

    root.mainloop()