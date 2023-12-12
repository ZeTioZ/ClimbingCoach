"""Module tkinter for the test page."""
import pickle
from threading import Thread

import customtkinter
import cv2
from PIL import Image

from database.queries import wall_queries
from enums.flux_reader_event_type import FluxReaderEventType
from gui.abstract.page import Page
from gui.utils import FONT, uv, v
from listeners.video_widget import VideoWidget


class CreateWall(Page):
	__imageSize = (1, 1)

	def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk):
		"""Constructor."""
		super().__init__(parent, app)

		self.cap = self.app.camera.flux_reader_event.video
		self.baseW = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
		self.baseH = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

		self.__imageSize = (self.baseW, self.baseH)

		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.grid_columnconfigure((0, 1), weight=2)
		self.grid_columnconfigure(2, weight=1)
		self.grid_rowconfigure(0, weight=3)
		self.grid_rowconfigure(1, weight=1)

		self.image_label = customtkinter.CTkLabel(self, text="", font=("Helvetica", 32))
		self.image_label.grid(row=0, column=0, columnspan=2, sticky="nsew")

		self.screen = customtkinter.CTkButton(self, text="Screenshot", command=self.__screener,
		                                      font=(FONT, 22))
		self.screen.grid(row=1, column=0, pady=uv(10), columnspan=2)

		self.video_widget = VideoWidget([FluxReaderEventType.GET_FRAME_EVENT])

	def set_active(self):
		self.thread_video = Thread(target=self.__start_video)
		self.thread_video.start()

	def set_inactive(self):
		self.__stop_video()

	def __get_frame(self):
		"""Get the frame from the camera."""
		frame = self.video_widget.last_image
		return frame

	def __read_video(self):
		if self.is_recording:
			frame = self.__get_frame()
			if frame is not None:
				self.__display_image(frame)
			self.after(10, self.__read_video)
		else:
			return

	def __start_video(self):
		self.is_recording = True
		self.app.camera.flux_reader_event.register(self.video_widget)
		self.__read_video()

	def __stop_video(self):
		self.is_recording = False
		self.app.camera.flux_reader_event.unregister(self.video_widget)

	def get_name(self):
		return "AddWall"

	def __display_image(self, image: Image):
		"""Display the image passed in parameter."""
		image_array = Image.fromarray(image)
		image_to_show = customtkinter.CTkImage(image_array, size=self.__imageSize)
		self.image_label.configure(image=image_to_show)

	def __change_image_size(self, size: (int, int)):
		"""Change the size of the image."""
		self.__imageSize = size

	def __resize_image(self, width: int, height: int):
		"""Resize the image."""
		actual_ratio = self.baseW/self.baseH

		target_height = v(50,height)
		target_width = target_height * actual_ratio

		if target_width > width:
			target_width = width
			target_height = target_width / actual_ratio

		self.__change_image_size((target_width, target_height))

	def on_size_change(self, width, height):
		"""Called when the windows size change."""
		super().on_size_change(width, height)

		self.__resize_image(width, height)

	def __save(self, image, name, difficulty, text_box):
		wall_queries.create_wall(name=name, difficulty=difficulty, description=text_box, image=pickle.dumps(image))

	# TODO: ajouter difficulty dans l'appel quand se sera set up

	def __screener(self):
		# add logical
		video_pop_up = customtkinter.CTkToplevel(self)
		video_pop_up.geometry("600x600")

		video_pop_up.grid_rowconfigure(0, weight=1)
		video_pop_up.grid_columnconfigure(0, weight=1)

		scrollable_frame = customtkinter.CTkScrollableFrame(video_pop_up)
		scrollable_frame.grid(row=0, column=0, sticky="nsew")

		scrollable_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
		scrollable_frame.grid_columnconfigure((0, 1), weight=1)

		image = Image.fromarray(self.__get_frame())
		image_to_show = customtkinter.CTkImage(image, size=self.__imageSize)
		video_pop_up_label = customtkinter.CTkLabel(scrollable_frame, text="", font=(FONT, 32), image=image_to_show)
		video_pop_up_label.grid(row=0, column=0, columnspan=2, sticky="nsew")

		# set name with entry
		name_label = customtkinter.CTkLabel(scrollable_frame, text="Name of the wall :", font=(FONT, 32))
		name_label.grid(row=1, column=0, pady=uv(10), padx=uv(10), sticky="e")

		name = customtkinter.CTkEntry(scrollable_frame, width=uv(150))
		name.grid(row=1, column=1, pady=uv(10), sticky="w")

		# set difficulty with combobox
		difficulty_label = customtkinter.CTkLabel(scrollable_frame, text="Difficulty :", font=(FONT, 32))
		difficulty_label.grid(row=2, column=0, pady=uv(10), padx=uv(10), sticky="e")

		difficulty = customtkinter.CTkComboBox(scrollable_frame, values=["1", "2", "3", "4", "5"], state="readonly",
		                                       width=uv(150))
		difficulty.grid(row=2, column=1, pady=uv(10), sticky="w")

		# set description with textbox
		description_label = customtkinter.CTkLabel(scrollable_frame, text="Description", font=(FONT, 32))
		description_label.grid(row=3, column=0, columnspan=2, pady=uv(10))

		text_box = customtkinter.CTkTextbox(scrollable_frame, width=uv(400))
		text_box.grid(row=4, column=0, pady=uv(10), columnspan=2)

		# set button to save
		save_button = customtkinter.CTkButton(scrollable_frame, text="Save",
		                                      command=lambda: [
			                                      self.__save(self.__get_frame(), name.get(), int(difficulty.get()),
			                                                  text_box.get("0.0", "end")), video_pop_up.destroy()],
		                                      font=(FONT, 22))
		save_button.grid(row=5, column=0, columnspan=2, pady=uv(10))
