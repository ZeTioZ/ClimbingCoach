from customtkinter import CTkFrame, CTk

class page(CTkFrame):

    __instance = None

    def __init__(self, parent: CTkFrame, app: CTk = None, *args, **kwargs):
        """Constructor. Singleton then init executed only once."""
        super().__init__(parent)
    
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

    @classmethod
    def get_instance(cls, parent, app=None):
        """Return the instance of the login page."""
        if cls.__instance is None:
            cls.__instance = cls(parent, app)
        return cls.__instance