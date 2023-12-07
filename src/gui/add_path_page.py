import customtkinter
import time
import os

from gui.component.interactive_image import InteractiveImage
from listeners.image_driver import ImageDriver

from PIL import Image

from gui.abstract.page import Page
from gui.component.interactive_image import InteractiveImage
from gui.utils import v, uv, iuv, FONT, get_ressources_path

from utils.color_holds import rgb_to_hex, generate_gradient_colors


class AddPathPage(Page):
	"""Class of the add path page."""

	def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk = None):
		"""Constructor for the add path page."""

		super().__init__(parent, app)
		self.__config_grid()
		#self.__config_pop_up()
		self.__create_widgets()

		self.calibrate_button = customtkinter.CTkButton(self, text="Refresh", command=self.__refresh_image)
		self.calibrate_button.grid(row=3, column=1, pady=iuv(10))
		self.create_path_button = customtkinter.CTkButton(self, text="Validate", command=lambda : self.create_path())
		self.create_path_button.grid(row=3, column=2, pady=iuv(10))

		self.hold_frame = customtkinter.CTkScrollableFrame(self, width=uv(175))

		self.hold_label_size = [uv(6), uv(3), uv(1.5)]
		self.trash_label_size = [uv(1), uv(3), uv(1.5)]

		self.label_list = []

		if self.label_list != []:
			self.modify_frame()

	def create_hold_label(self, hold, index: int, color: tuple[int,int,int]):
		"""Creates a button with the given text."""

		hold_label = customtkinter.CTkLabel(
			self.hold_frame,
			text=f"hold {index+1}",
			fg_color= rgb_to_hex(color),
			anchor="center",
			corner_radius=uv(100),
			width=self.hold_label_size[0],
			height=self.hold_label_size[1],
			font=(FONT, self.hold_label_size[2])
		)
		
		bin_img = customtkinter.CTkImage(Image.open(os.path.join(get_ressources_path(), "images", "bin.png")))
		hold_trash_button = customtkinter.CTkLabel(
			self.hold_frame, 
			text="",
			image=bin_img, 
			width=self.trash_label_size[0], 
			height=self.trash_label_size[1], 
			fg_color=rgb_to_hex(color), 
			corner_radius=uv(100)
		)
		

		hold_label.bind("<Enter>", lambda event: self.image_driver.set_hold_to_highlight(self.image_driver.get_hold_by_index(index)))
		hold_label.bind("<Leave>", lambda event: self.image_driver.remove_hold_to_highlight())


		def remove_hold():
			"""Remove the hold."""
			self.image_driver.route_remove_box_by_index(index)
			self.__refresh_hold_menu()
			self.image_driver.display_holds(self.image_driver.holds)

		hold_trash_button.bind("<Button-1>", lambda event: remove_hold())
		hold_trash_button.grid(row=index, column=1, sticky="e")
		# hold_label.bind("<Button-1>", lambda event: self.image_driver.route_remove_box_by_index(index))

		hold_label.grid(row=index, column=0, padx=uv(10), sticky="ew", pady=uv(10))
		return hold_label, hold_trash_button


	def get_path(self):
		"""Return the path of the holds."""
		return self.image_driver.route.get_route()


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

		route_name_pop_up_button = customtkinter.CTkButton(route_name_pop_up, text="Save", command=lambda : [self.save_function(entry_route_name.get()), route_name_pop_up.destroy()])
		route_name_pop_up_button.grid(row=2, column=0, pady=iuv(10))
		
		#get all the holds
		self.label_list : list[customtkinter.CTkLabel] = []
		hold_list = self.get_path()
		colors = generate_gradient_colors(len(hold_list))

		for hold_num in range(len(hold_list)):
			hold_label, trash_label = self.create_hold_label(hold_list[hold_num], hold_num, colors[hold_num])
			self.label_list.append((hold_label, trash_label))

		#Check if the path is correctly showed in the run page


	def __refresh_hold_menu(self):
		self.__empty_label_list()
		hold_list = self.get_path()
		colors = generate_gradient_colors(len(hold_list))
		for hold_num in range (len(hold_list)):
			hold_label, trash_label = self.create_hold_label(hold_list[hold_num], hold_num, colors[hold_num])
			self.label_list.append((hold_label, trash_label))

		if len(hold_list) > 0:
			self.__show_hold_menu()
		else:
			self.__hide_hold_menu()


	def __empty_label_list(self):
		if len(self.label_list) > 0:
			for label_tuple in self.label_list:
				label_tuple[0].destroy()
				label_tuple[1].destroy()
			self.label_list = []


	def __show_hold_menu(self):
		"""Save the path."""
		#grid the frame with the holds
		self.hold_frame.grid(row=0, column=0, rowspan=5, sticky="nswe")
		self.calibrate_button.grid_forget()
		self.create_path_button.grid_forget()

		self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

		self.calibrate_button.grid(row=3, column=2, pady=iuv(10))
		self.create_path_button.grid(row=3, column=3, pady=iuv(10))

		self.i_image.grid(row=0, column=2, columnspan=2)

	
	def __hide_hold_menu(self):
		"""Save the path."""
		#grid the frame with the holds
		self.hold_frame.grid_forget()
		self.calibrate_button.grid_forget()
		self.create_path_button.grid_forget()

		self.grid_columnconfigure((0, 1, 2, 3), weight=1)

		self.calibrate_button.grid(row=3, column=1, pady=iuv(10))
		self.create_path_button.grid(row=3, column=2, pady=iuv(10))

		self.i_image.grid(row=0, column=1, columnspan=2)

		
	def save_function(self, name : str):
		print(name)
		self.image_driver.route_set_name(name)
		self.image_driver.save_route()


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


	def __refresh_image(self):
		"""Refresh the image."""
		self.image_driver.route_clear()
		self.__refresh_hold_menu()
		self.app.camera.flux_reader_event.refresh_holds()


	def __create_widgets(self):
		"""Creates the widgets for the add path page."""

		self.i_image = InteractiveImage(self, width=iuv(500), height=iuv(500))
		self.i_image.grid(row=0, column=1, columnspan=2) # Don't use sticky here, it will break the image

		self.image_driver = ImageDriver(self.i_image)
		# self.app.camera.flux_reader_event.register(self.image_driver)
		self.image_driver.bind_click(self.__refresh_hold_menu)


	def __resize_hold_label(self, width: int, height: int):
		"""Resize the hold label."""

		self.hold_label_size = [v(6, width), v(3, height), v(1.5, height)]
		self.trash_label_size = [v(1, width), v(3, height), v(1.5, height)]

		for hold_label in self.label_list:
			hold_label[0].configure(width=v(6, width), height=v(3, height), font=(FONT, v(1.5, height)))
			hold_label[1].configure(width=v(1, width), height=v(3, height), font=(FONT, v(1.5, height)))

	# Page methods

	def on_size_change(self, width, height):
		"""Called when the size of the window change."""
		self.i_image.change_size(v(50, height), v(50, height))

		self.__resize_hold_label(width, height)

		self.calibrate_button.configure(width=v(7, width), height=v(5, height), font=(FONT, v(2.5, height)))
		self.create_path_button.configure(width=v(7, width), height=v(5, height), font=(FONT, v(2.5, height)))

	
	def set_active(self):
		super().set_active()
		self.app.camera.flux_reader_event.register(self.image_driver)
		self.app.camera.flux_reader_event.refresh_holds()


	def set_inactive(self):
		super().set_inactive()
		self.app.camera.flux_reader_event.unregister(self.image_driver)