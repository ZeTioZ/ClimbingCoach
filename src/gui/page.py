from customtkinter import CTkFrame, CTk
from gui.singleton import Singleton

class page(CTkFrame, metaclass=Singleton):

    # __instance = None
    app = None

    def __init__(self, parent: CTkFrame, app: CTk, *args, **kwargs):
        """Constructor. Singleton then init executed only once."""
        super().__init__(parent)
        self.app = app
        
    
    def onSizeChange(self, width, height):
        """Called when the windows size change."""
        pass

    def update(self, *args, **kwargs):
        """Update the page."""
        pass


    def setUnactive(self):
        """Set the page unactive."""
        pass


    def setActive(self):
        """Set the page active."""
        pass


    def get_name(self):
        """Return the name of the page."""
        return self.__class__.__name__
