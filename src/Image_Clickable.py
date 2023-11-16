import customtkinter as CTk
from PIL import Image

from interfaces.observable import Observable

class image_clickable(CTk.CTkLabel, Observable):
    """Class to create a clickable image."""

    __callback = None

    def __init__(self, parent: CTk.CTkFrame, image: Image, callback, *args, **kwargs):
        """Constructor."""

        super().__init__(parent, text= "", image= image, *args, **kwargs)
        Observable.__init__(self)

        self.__callback = callback
        self.bind("<Button-1>", self.__click)
        self.bind("<Enter>", self.__enter)
        self.bind("<Leave>", self.__leave)


    def __click(self, event):
        """Called when the image is clicked."""
        self.__callback()


    def __enter(self, event):
        """Called when the mouse enter the image."""
        self.configure(image=self.dark_image)


    def __leave(self, event):
        """Called when the mouse leave the image."""
        self.configure(image=self.light_image)

if(__name__ == "__main__"):
    from tkinter import Tk
    from PIL import Image

    root = Tk()
    root.title("test")
    root.geometry("500x500")

    image = Image.open("../resources/images/chemin_light.png")
    image = image.resize((100, 100))
    image = image.convert("RGBA")

    def callback():
        print("clicked")

    image = image_clickable(root, image, callback)
    image.pack()

    root.mainloop()