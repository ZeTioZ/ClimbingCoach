import customtkinter
from gui.abstract.page import page
from gui.component.interactive_image import InteractiveImage
from listeners.image_driver import ImageDriver

class add_path_page(page):
    """Class of the add path page."""
    
    def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk = None):
        """Constructor for the add path page."""

        super().__init__(parent, app)
        self.__config_grid()
        self.__create_widgets()



    def __config_grid(self):
        self.grid_columnconfigure((0,1,2,3,4), weight=1)
        self.grid_rowconfigure((0,1,2,3,4), weight=1)

    
    def __create_widgets(self):
        """Creates the widgets for the add path page."""

        self.iimage = InteractiveImage(self, width=500, height=500)
        self.iimage.grid(row=0, column=0, columnspan=5, sticky="nswe")

        self.image_driver = ImageDriver(self.iimage)
        self.app.camera.flux_reader_event.register(self.image_driver)


