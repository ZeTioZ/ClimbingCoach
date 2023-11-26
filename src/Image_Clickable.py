from asyncio import sleep
import time
from typing import Any
import customtkinter as CTk
from tkinter import Event
from PIL.Image import Image
from os import path

import numpy as np

from enums.image_event_type import ImageEventType
from enums.event_type import EventType
from enums.click_type import ClickType
from interfaces.event import Event
from interfaces.listener import Listener
from models.hold_detector import HoldDetector
from objects.box import Box
from events.flux_reader_event import FluxReaderEvent
from threads.camera_thread import Camera
from enums.flux_reader_event_type import FluxReaderEventType

from utils.click import find_selected_hold
from utils.draw_utils import box_visualizer

# Time mesurer decorator
from functools import wraps
import time
def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        # first item in the args, ie `args[0]` is `self`
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper
# End time mesurer decorator

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
        if ImageEventType.CLICK_EVENT in event_types and isinstance(event, ImageDriver):
            interactive_image = event.get_interactive_image()
            click_type: ClickType = args[0]
            x: int = args[1]
            y: int = args[2]
            if click_type == ClickType.LEFT_CLICK:
                # selected_hold = find_selected_hold(interactive_image.model.get_holds(), x, y)
                # if selected_hold is not None:
                #     self.__add_box_to_path(selected_hold)
                #     interactive_image.refresh_image(self.path)
                print("left click")
            elif click_type == ClickType.RIGHT_CLICK:
                # selected_hold = find_selected_hold(interactive_image.model.get_holds(), x, y)
                # if selected_hold is not None:
                #     self.__remove_box_from_path(selected_hold)
                #     interactive_image.refresh_image(self.path)
                print("right click")
            else:
                print("unknown click type:")

    def __add_box_to_path(self, box: Box):
        """Add a box to the path."""
        if(box not in self.path): self.path.append(box)
    
    def __remove_box_from_path(self, box: Box):
        """Remove a box from the path."""
        if(box in self.path): self.path.remove(box)


class InteractiveImage(CTk.CTkLabel):
    """Class to create a clickable image."""

    ctkimage: CTk.CTkImage | None = None
    def is_ctkimage(self): return self.ctkimage is not None

    __image_size: tuple[int, int] = (0, 0)

    default_size_width: int = 0
    default_size_height: int = 0

    def __init__(self, parent: CTk.CTkFrame, image: Image| None = None, width: int = None, height: int = None):
        """Constructor."""

        if(image is not None):
            self.__load_image(image=image)

        if(width is None or height is None):
            self.change_size(width, height)

        super().__init__(parent, text= "", image= self.ctkimage)
        Event.__init__(self)


    def change_image(self, image: Image):
        """Change the image."""
        if image is None: return
        self.__load_image(image=image)

    
    def __load_image(self, image: Image):
        self.image = image
        self.default_size_width, self.default_size_height = image.size # (width, height)
        self.ctkimage = CTk.CTkImage(image, size=self.__image_size)
        self.configure(image= self.ctkimage)


    def change_size(self, width: int, height: int):
        """Change the size of the image."""
        self.__image_size = (width, height)
        self.configure(width= width, height= height)
        if self.is_ctkimage():
            self.__resize_image(width, height)


    
    def __resize_image(self, width: int, height: int):
        """Resize the image."""
        self.ctkimage.configure(size= (width, height))
        self.configure(image= self.ctkimage)


    def bind_right_click(self, callback: Any):
        """Bind the right click event."""
        self.bind("<Button-3>", callback)
    

    def bind_left_click(self, callback: Any):
        """Bind the left click event."""
        self.bind("<Button-1>", callback)


class ImageDriver(Event, Listener):

    def __init__(self, iimage: InteractiveImage):
        Event.__init__(self)
        Listener.__init__(self, [
            FluxReaderEventType.HOLDS_PROCESSED_EVENT,
            FluxReaderEventType.GET_FRAME_EVENT
        ])

        self.iimage = iimage
        iimage.bind_right_click(self.click_right)
        iimage.bind_left_click(self.click_left)


    def get_interactive_image(self):
        """Return the interactive image."""
        return self.iimage

    # Holds
    holds: list[Box] = []

    def set_holds(self, holds: list[Box]):
        """Set the holds."""
        self.holds = holds


    def is_holds(self): return len(self.holds) > 0


    def draw_holds(self) -> Image:
        """Draw the holds on the image."""
        if self.is_image() and self.is_holds():
            return Image.fromarray(box_visualizer(self.image, self.holds))
    
    # Image
    image: Image | None = None


    def is_image(self): return self.image is not None


    def set_image(self, image: Image):
        """Set the image."""
        self.image = image

    # EVENT

    def click_right(self, event):
        """Called when the image is clicked."""
        self.__click(event, ClickType.RIGHT_CLICK)


    def click_left(self, event):
        """Called when the image is clicked."""
        self.__click(event, ClickType.LEFT_CLICK)


    def __click(self, event, click_type: ClickType):
        """Called when the image is clicked."""
        default_x = int(self.iimage.default_size_width * event.x / self.iimage.winfo_width())
        default_y = int(self.iimage.default_size_height * event.y / self.iimage.winfo_height())
        self.notify([ImageEventType.CLICK_EVENT], click_type, default_x, default_y)

    # LISTENER

    def update(self, event: Event, event_types: [EventType], *args, **kwargs):
        """Called when the event notify the observer."""
        if not isinstance(event, FluxReaderEvent): return
        if FluxReaderEventType.HOLDS_PROCESSED_EVENT in event_types:
            self.__on_hold_recived(args[0])
        
        if FluxReaderEventType.GET_FRAME_EVENT in event_types:
            self.__on_frame_recived(args[0])
            

    def __on_hold_recived(self, holds: list[Box]):
        """Called when the holds are recived."""
        self.set_holds(holds)
        self.change_image()


    def __on_frame_recived(self, frame: Image|np.ndarray):
        """Called when the frame is recived."""
        if isinstance(frame, np.ndarray): 
            frame = Image.fromarray(frame)
        self.set_image(frame)
        self.change_image()

    # UTILS

    def change_image(self):
        """Change the image."""
        self.iimage.change_image(self.draw_holds())

if(__name__ == "__main__"):
    from tkinter import Tk
    from PIL import Image

    root = Tk()
    root.title("test")
    root.geometry("500x500")

    root.bind("<Configure>", lambda e: image_composant.change_size(e.width, e.height))


    image_composant = InteractiveImage(root, width=500, height=500)
    image_composant.pack()

    id = ImageDriver(image_composant)


    printer1 = printer()
    id.register(printer1)

    video_path = path.join(path.dirname(path.dirname(path.abspath(__file__))),"resources","videos","Escalade_Fixe.mp4")
    camera = Camera(video_path)
    camera.flux_reader_event.register(id)
    camera.start()

    root.mainloop()