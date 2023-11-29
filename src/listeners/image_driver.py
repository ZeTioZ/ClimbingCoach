from gui.component.interactive_image import InteractiveImage
from enums.event_type import EventType
from enums.flux_reader_event_type import FluxReaderEventType
from events.flux_reader_event import FluxReaderEvent
from interfaces.event import Event
from interfaces.listener import Listener
from objects.box import Box
from utils.click import find_selected_hold
from utils.draw_utils import box_visualizer, draw_path


import numpy as np
from PIL import Image


from tkinter import Event


class ImageDriver(Listener):

    image: np.ndarray = None

    def __init__(self, i_image: InteractiveImage):
        super().__init__([
            FluxReaderEventType.HOLDS_PROCESSED_EVENT,
            FluxReaderEventType.GET_FRAME_EVENT
        ])

        self.i_image = i_image
        self.i_image.bind_right_click(self.click_right)
        self.i_image.bind_left_click(self.click_left)


    def get_interactive_image(self):
        """Return the interactive image."""
        return self.i_image


    def draw_holds_and_path(self, image: np.ndarray, holds: list[Box]) -> Image:
        """Draw the holds on the image."""
        
        drawed_image = box_visualizer(image, holds)
        drawed_image = box_visualizer(drawed_image, self.path, (0, 0, 255))
        drawed_image = draw_path(drawed_image, self.path)

        return Image.fromarray(drawed_image)


    # PATH MANAGER
    holds: list[Box] = []
    path: list[Box] = []


    def click_right(self, event):
        """Called when the image is clicked."""
        selected_box = self.__click(event)
        if selected_box is not None and selected_box in self.path:
            self.path.remove(selected_box)
            self.i_image.change_image(self.draw_holds_and_path(self.image, self.holds))


    def click_left(self, event):
        """Called when the image is clicked."""
        selected_box = self.__click(event)
        if selected_box is not None:
            self.path.append(selected_box)
            self.i_image.change_image(self.draw_holds_and_path(self.image, self.holds))


    def __click(self, event) -> Box:
        """Called when the image is clicked."""
        if self.image is None: return
        default_x = int(self.i_image.default_size_width * event.x / self.i_image.winfo_width())
        default_y = int(self.i_image.default_size_height * event.y / self.i_image.winfo_height())
        return find_selected_hold(self.holds, default_x, default_y)


    # LISTENER

    def update(self, event: Event, event_types: [EventType], *args, **kwargs):
        """Called when the event notify the observer."""
        if not isinstance(event, FluxReaderEvent): return

        if FluxReaderEventType.HOLDS_PROCESSED_EVENT in event_types:
            self.__on_hold_recived(args[0], args[1])
    
        if FluxReaderEventType.GET_FRAME_EVENT in event_types:
            self.image = args[0]


    def __on_hold_recived(self, holds: list[Box], frame: np.ndarray):
        """Called when the holds are recived."""
        self.holds = holds
        self.image = frame
        self.change_image(holds= holds, image= frame)

    # UTILS

    def change_image(self, holds: list[Box], image: np.ndarray):
        """Change the image."""
        self.i_image.change_image(self.draw_holds_and_path(image, holds))