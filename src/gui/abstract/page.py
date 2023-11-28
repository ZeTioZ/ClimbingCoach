from abc import abstractmethod

from customtkinter import CTkFrame, CTk
from gui.abstract.singleton import Singleton

class Page(CTkFrame, metaclass=Singleton):

    # __instance = None
    app = None

    def __init__(self, parent: CTkFrame, app: CTk, *args, **kwargs):
        """Constructor. Singleton then init executed only once."""
        super().__init__(parent)
        self.app = app
        
    @abstractmethod
    def onSizeChange(self, width, height):
        """Called when the windows size change."""
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        """Update the page."""
        pass

    @abstractmethod
    def setUnactive(self):
        """Set the page unactive."""
        pass

    @abstractmethod
    def setActive(self):
        """Set the page active."""
        pass

    def get_name(self):
        """Return the name of the page."""
        return self.__class__.__name__
