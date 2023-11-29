import customtkinter
from gui.component.interactive_image import InteractiveImage
from listeners.image_driver import ImageDriver

from gui.abstract.page import Page


class AddPathPage(Page):
	"""Class of the add path page."""

	def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk = None):
		"""Constructor for the add path page."""

		super().__init__(parent, app)
		self.__config_grid()
		self.__create_widgets()


	def __config_grid(self):
		self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
		self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)


	def create_widgets(self):
		"""Create the widgets for the page."""
		self.__create_widgets()

	def __create_widgets(self):
		"""Creates the widgets for the add path page."""

		self.i_image = InteractiveImage(self, width=500, height=500)
		self.i_image.grid(row=0, column=0, columnspan=5, sticky="nswe")

		self.image_driver = ImageDriver(self.i_image)
		self.app.camera.flux_reader_event.register(self.image_driver)
