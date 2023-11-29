import customtkinter
from gui.component.interactive_image import InteractiveImage
from listeners.image_driver import ImageDriver

from gui.abstract.page import Page
from gui.run_page import RunPage


class AddPathPage(Page):
	"""Class of the add path page."""

	def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk = None):
		"""Constructor for the add path page."""

		super().__init__(parent, app)
		self.__config_grid()
		self.__create_widgets()
		self.calibrate_button = customtkinter.CTkButton(self, text="Calibrate", command=lambda : self.app.show_page(AddPathPage))
		self.calibrate_button.grid(row=4, column=0)
		
		self.create_path_button = customtkinter.CTkButton(self, text="Create path", command=lambda : self.create_path())
		self.create_path_button.grid(row=4, column=1)

		#create a list of 12 colors that will be present of the hold list with the rgb code
		self.color_dic={"red":"#FF0000","orange":"#FFA500","yellow":"#FFFF00","green":"#008000","blue":"#0000FF","purple":"#4B0082","rose":"#EE82EE","black":"#000000","grey":"#808080","white":"#FFFFFF","maroon":"#800000","olive":"#808000"}
		for color in self.color_dic:
			self.color_dic[color]=customtkinter.CTkButton(self, text=" eterea ", fg_color=self.color_dic[color], command=lambda : self.app.show_page(AddPathPage))
			self.color_dic[color].grid(row=4, column=color+1)

	def create_path(self):
		"""Create the path."""
		#save the path
		self.app.show_page(RunPage)
		#Check if the path is correctly showed in the run page


	def __config_grid(self):
		self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
		self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)


	def __create_widgets(self):
		"""Creates the widgets for the add path page."""

		self.i_image = InteractiveImage(self, width=500, height=500)
		self.i_image.grid(row=0, column=0, columnspan=5, sticky="nswe")

		self.image_driver = ImageDriver(self.i_image)
		self.app.camera.flux_reader_event.register(self.image_driver)
