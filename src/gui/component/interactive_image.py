import customtkinter as CTk
from PIL.Image import Image
from tkinter import Event as TkEvent
from typing import Callable

class InteractiveImage(CTk.CTkLabel):
    """Class to create a clickable image."""

    ctkimage: CTk.CTkImage | None = None
    def is_ctkimage(self): return self.ctkimage is not None

    __image_size: tuple[int, int] = (0, 0)

    default_size_width: int = 0
    default_size_height: int = 0

    def __init__(self, parent: CTk.CTkFrame, image: Image| None = None, width: int = None, height: int = None):
        """Constructor."""
        super().__init__(parent, text= "", image= self.ctkimage)

        if(image is not None):
            self.__load_image(image=image)

        if(width is not None and height is not None):
            self.change_size(width, height)


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


    def bind_right_click(self, callback: Callable[[TkEvent], None]):
        """Bind the right click event."""
        self.bind("<Button-3>", callback)
    

    def bind_left_click(self, callback: Callable[[TkEvent], None]):
        """Bind the left click event."""
        self.bind("<Button-1>", callback)