"""Module tkinter for the test page."""
import os.path
from threading import Thread
from typing import Callable

import customtkinter
import cv2
import numpy as np
import time
from PIL import Image
from threads.camera_thread import Camera

from utils.draw_utils import skeleton_visualizer
from listeners.skeleton_listener import SkeletonRecordSaverListener
from enums.flux_reader_event_type import FluxReaderEventType
from gui.abstract.page import Page
from gui.run_viewer_page import RunViewerPage
from gui.utils import EMPTY_IMAGE, FONT, SECONDARY_COLOR, uv
from listeners.video_widget import VideoWidget


class CreateWall(Page):
	__reading = False
	__thread_actif = False
	__isCameraLoaded = False
	__imageSize = None

	"""test page."""

	def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk):
		"""Constructor. Singleton then init executed only once."""
		super().__init__(parent, app)

		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.grid_columnconfigure((0, 1), weight=2)
		self.grid_columnconfigure(2, weight=1)
		self.grid_rowconfigure(0, weight=3)
		self.grid_rowconfigure(1, weight=1)

		self.image_label = customtkinter.CTkLabel(self, text="", font=("Helvetica", 32))
		self.image_label.grid(row=0, column=0, columnspan=2, sticky="nsew")

		self.screen = customtkinter.CTkButton(self, text="ScreenShot", command=self.__screener,
		                                              font=(FONT, 22))
		self.screen.grid(row=1, column=0, pady=uv(10))

		self.video_widget = VideoWidget([FluxReaderEventType.GET_FRAME_EVENT])


	def set_active(self):
		self.thread_video = Thread(target=self.__start_video)
		self.thread_video.start()
	
	def set_inactive(self):
		self.__stop_video()

	def __get_frame(self):
		"""Get the frame from the camera."""
		frame = self.video_widget.last_image
		if frame is not None:
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			self.__display_image(frame)


	def __read_video(self):	
		if self.is_recording:
			self.__get_frame()
			self.after(10,self.__read_video)
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
		image_to_show = customtkinter.CTkImage(image_array)
		self.image_label.configure(image=image_to_show)

	def on_size_change(self, width, height):
		"""Called when the windows size change."""
		super().on_size_change(width, height)

		hrate = (height * 0.5) / 480
		wrate = (width * 0.5) / 640
		rate = min(hrate, wrate)
		# self.__scale(rate * 100)

	def __save(self, image, name, difficulty, text_box):
		print(name, difficulty, text_box)

	def __screener(self):
		# add logical
		self.__stop_video()
		video_pop_up = customtkinter.CTkToplevel(self)

		scrollable_frame = customtkinter.CTkFrame(video_pop_up)
		scrollable_frame.grid(row=0, column=0, sticky="nsew")

		video_pop_up_lable = customtkinter.CTkLabel(scrollable_frame, text="", font=("Helvetica", 32), image=image)
		video_pop_up_lable.grid(row=0, column=0, columnspan=2, sticky="nsew")

		#set name with entry
		name_label = customtkinter.CTkLabel(scrollable_frame, text="Name of the wall :", font=("Helvetica", 32))
		name_label.grid(row=1, column=0, pady=uv(10), padx=uv(10))

		name = customtkinter.CTkEntry(scrollable_frame)
		name.grid(row=1, column=1, pady=uv(10))

		#set difficulty with combobox
		difficulty_label = customtkinter.CTkLabel(scrollable_frame, text="Difficulty", font=("Helvetica", 32))
		difficulty_label.grid(row=2, column=0, pady=uv(10), padx=uv(10))

		difficulty = customtkinter.CTkComboBox(scrollable_frame, values=["1", "2", "3", "4", "5"])
		difficulty.grid(row=2, column=1, pady=uv(10))

		#set description with textbox
		description_label = customtkinter.CTkLabel(scrollable_frame, text="Description", font=("Helvetica", 32))
		description_label.grid(row=3, column=0, pady=uv(10))

		text_box = customtkinter.CTkTextBox(scrollable_frame)
		text_box.grid(row=4, column=0, pady=uv(10))

		#set button to save
		print(text_box.get("0.0","end"))
		save_button = customtkinter.CTkButton(scrollable_frame, text="Save", command=self.__save("image", name.get(), difficulty.get(), text_box.get("0.0","end")), font=(FONT, 22))
		save_button.grid(row=5, column=0, pady=uv(10))

		self.stop_recording.grid_forget()
		self.start_recording.grid(row=1, column=0, pady=uv(10))
