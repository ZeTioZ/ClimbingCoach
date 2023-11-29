import customtkinter

from gui.component.interactive_image import InteractiveImage
from listeners.image_driver import ImageDriver
import time


from gui.abstract.page import Page
from gui.component.interactive_image import InteractiveImage
from listeners.image_driver import ImageDriver
from gui.utils import v, uv, iuv, get_parent_path, FONT

from gui.utils import FONT


class AddPathPage(Page):
	"""Class of the add path page."""

	def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk = None):
		"""Constructor for the add path page."""

		super().__init__(parent, app)
		self.__config_grid()
		#self.__config_pop_up()
		self.__create_widgets()

		self.calibrate_button = customtkinter.CTkButton(self, text="Take a picture", command=self.__config_pop_up)
		self.calibrate_button.grid(row=4, column=1, pady=iuv(10))
		self.create_path_button = customtkinter.CTkButton(self, text="Validate", command=lambda : self.create_path())
		self.create_path_button.grid(row=4, column=2, pady=iuv(10))

		self.hold_frame = customtkinter.CTkScrollableFrame(self, width=uv(150))

		#create a list of 12 colors that will be present of the hold list with the rgb code
		colors = ["red", "orange", "yellow", "green", "blue", "purple", "rose", "black", "grey", "white", "maroon", "olive"]
		self.color_dic={"red":"#FF0000","orange":"#FFA500","yellow":"#FFFF00","green":"#008000","blue":"#0000FF","purple":"#4B0082","rose":"#EE82EE","black":"#000000","grey":"#808080","white":"#FFFFFF","maroon":"#800000","olive":"#808000"}
		#self.color_dic={"red":(255, 0, 0),"orange":(255, 165, 0),"yellow":(255, 255, 0),"green":(0, 128, 0),"blue":(0, 0, 255),"purple":(75, 0, 130),"rose":(238, 130, 238),"black":(0, 0, 0),"grey":(128, 128, 128),"white":(255, 255, 255),"maroon":(128, 0, 0),"olive":(128, 128, 0)}
		#for i, color in enumerate(colors):
		#	button = customtkinter.CTkButton(self, text=" eterea ", fg_color=self.color_dic[color], command=lambda color=color: self.app.show_page(AddPathPage))
		#	button.grid(row=4, column=i+2)


	def create_button(self, display_text, index):
		"""Creates a button with the given text."""

		is_first = index == 0

		self.button = customtkinter.CTkButton(
			self.path_list_frame,
			text=display_text,
			#fg_color= ,
			#hover_color=, TODO : get the color of the hold
			border_spacing=uv(17),
			command=lambda: self.show_path_detail(index),
			anchor="w"
		)

		self.button.grid(row=index, column=0, padx=uv(10), sticky="ew")
		return self.button


	def get_path(self):
		"""Return the path of the holds."""
		return self.image_driver.path
	

	def refresh_color(self):
		"""Refresh the color of the holds when a hold is deleted."""
		#Check if the color is correctly changed in the run page
		pass

	def create_path(self):
		"""Create the path."""
		#self.image_driver.save_root
		route_name_pop_up = customtkinter.CTkToplevel(self)
		self.after(200, route_name_pop_up.lift)
		route_name_pop_up.title("Route name")
		route_name_pop_up.geometry("300x100")
		route_name_pop_up.resizable(False, False)
		route_name_pop_up.grid_columnconfigure(0, weight=1)
		route_name_pop_up.grid_rowconfigure((0, 1), weight=1)

		route_name_pop_up_label = customtkinter.CTkLabel(route_name_pop_up, text="Name your route !", font=(FONT, 15))
		route_name_pop_up_label.grid(row=0, column=0)
		
		entry_route_name = customtkinter.CTkEntry(route_name_pop_up)
		entry_route_name.grid(row=1, column=0)

		#TODO : faire appel a la fonction qui save la route
		route_name_pop_up_button = customtkinter.CTkButton(route_name_pop_up, text="Save", command=lambda : [route_name_pop_up.destroy(), self.save_function()])
		route_name_pop_up_button.grid(row=2, column=0, pady=iuv(10))
		
		#get all the holds
		self.button_list : list[customtkinter.CTkButton] = []
		hold_list = self.get_path()
		for hold in hold_list:
			self.hold_button = self.create_button(hold, hold_list.index(hold))
			self.button_list.append(self.hold_button)

		#Check if the path is correctly showed in the run page


	def save_function(self):
		"""Save the path."""
		#grid the frame with the holds
		self.hold_frame.grid(row=0, column=0, rowspan=5, sticky="nswe")
		self.calibrate_button.grid_forget()
		self.create_path_button.grid_forget()
		self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

		self.calibrate_button.grid(row=4, column=2, pady=iuv(10))
		self.create_path_button.grid(row=4, column=3, pady=iuv(10))
		#TODO : faire appel a la fonction qui save la route


	def __config_grid(self):
		self.grid_columnconfigure((0, 1, 2, 3), weight=1)
		self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

	
	def __config_pop_up(self):
		"""Configure the pop up."""
		pop_up = customtkinter.CTkToplevel(self)
		self.after(200, pop_up.lift)
		pop_up.title("Countdown information")
		pop_up.geometry("300x100")
		pop_up.resizable(False, False)
		pop_up.grid_columnconfigure(0, weight=1)
		pop_up.grid_rowconfigure((0, 1), weight=1)

		pop_up_message = customtkinter.CTkLabel(pop_up, text="An image will be taken in 3 seconds\n after clicking on OK", font=(FONT, 15))
		pop_up_message.grid(row=0, column=0)
		pop_up_button = customtkinter.CTkButton(pop_up, text="OK", command=lambda : [pop_up.destroy(), self.__take_a_picture()])
		pop_up_button.grid(row=1, column=0)

	
	def __take_a_picture(self):
		"""Take a picture."""
		#self.after(3000, self.image_driver.refresh())
		pass


	def __create_widgets(self):
		"""Creates the widgets for the add path page."""

		self.i_image = InteractiveImage(self, width=iuv(500), height=iuv(500))
		self.i_image.grid(row=0, column=1, columnspan=5, sticky="nswe")

		self.image_driver = ImageDriver(self.i_image)
		self.app.camera.flux_reader_event.register(self.image_driver)
