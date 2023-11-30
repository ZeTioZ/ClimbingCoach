"""Module tkinter for the test page."""
import os.path
from threading import Thread
from typing import Callable

import customtkinter
import cv2
import numpy as np
import time
from PIL import Image

from utils.draw_utils import skeleton_visualizer
from listeners.skeleton_listener import SkeletonRecordSaverListener
from enums.flux_reader_event_type import FluxReaderEventType
from gui.abstract.page import Page
from gui.run_viewer_page import RunViewerPage
from gui.utils import EMPTY_IMAGE, FONT, SECONDARY_COLOR, uv
from listeners.video_widget import VideoWidget


class RunPage(Page):
	__reading = False
	__thread_actif = False
	__isCameraLoaded = False
	__imageSize = None

	"""test page."""

	def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk):
		"""Constructor. Singleton then init executed only once."""
		super().__init__(parent, app)

		if app is not None:
			app.title("Run Page")

		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.grid_columnconfigure((0, 1), weight=2)
		self.grid_columnconfigure(2, weight=1)
		self.grid_rowconfigure(0, weight=3)
		self.grid_rowconfigure(1, weight=1)

		self.video_widget = VideoWidget([FluxReaderEventType.FRAME_PROCESSED_EVENT])
		self.skeleton_record_saver_listener: SkeletonRecordSaverListener = SkeletonRecordSaverListener()

		self.test_label = customtkinter.CTkLabel(self, text="", font=("Helvetica", 32))
		self.test_label.grid(row=0, column=0, columnspan=2, sticky="nsew")

		# Add two button
		# this button will start recording, but we'll stay on this page
		self.start_recording = customtkinter.CTkButton(self, text="Start recording", command=self.__start_recording,
		                                               font=(FONT, 22))
		self.start_recording.grid(row=1, column=0, pady=uv(10))

		self.load_recording = customtkinter.CTkButton(self, text="Load recording", command=self.__load_recording,
		                                              font=(FONT, 22))
		self.load_recording.grid(row=1, column=1, pady=uv(10))

		self.stop_recording = customtkinter.CTkButton(self, text="Stop recording", command=self.__stop_recording,
		                                              font=(FONT, 22), fg_color="red")

		self.show_cam = customtkinter.CTkImage(dark_image=Image.open(self.__get_icon_path("show_cam.png")),
		                                       size=(25, 25))
		self.hide_cam = customtkinter.CTkImage(dark_image=Image.open(self.__get_icon_path("hide_cam.png")),
		                                       size=(25, 25))
		self.visibility_button = customtkinter.CTkButton(self, text="", command=self.__toggle_camera,
		                                                 state=customtkinter.DISABLED, image=self.hide_cam,
		                                                 width=uv(50), height=uv(50))
		self.visibility_button.grid(row=0, column=2, padx=uv(10))

		self.camLoader = None

	def __get_icon_path(self, icon_name: str):
		"""Return the path of the icon passed in parameter."""
		return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'resources',
		                    'images', icon_name)

	def __fetch_run_list(self):
		"""Fetch the run list from the database."""
		return [f"Run {i}" for i in range(1, 7)]

	def create_button(self, display_text, index):
		"""Creates a button with the given text."""

		is_first = index == 0

		self.button = customtkinter.CTkButton(
			self.run_list_frame,
			text=display_text,
			fg_color=SECONDARY_COLOR if is_first else "transparent",
			hover_color=SECONDARY_COLOR,
			border_spacing=uv(17),
			# command=,
			anchor="w"
		)

		self.button.grid(row=index, column=0, padx=uv(10), sticky="ew")
		return self.button

	def set_model(self, model: Callable[[np.ndarray], np.ndarray]):
		self.__model = model

	def __animation_camera_loading(self):
		if not self.__thread_actif:
			return
		inner_text = self.test_label.cget("text")
		if len(inner_text) > 3:
			inner_text = ""
		inner_text += "."
		self.test_label.configure(text=inner_text)
		if self.__isCameraLoaded:
			self.test_label.configure(text="")
			return
		self.after(1000, self.__animation_camera_loading)

	def __init_cap(self, scale_percent: int = 100):
		self.cap = self.app.camera.flux_reader_event.video
		self.baseW = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
		self.baseH = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

		self.__imageSize = (self.baseW, self.baseH)

		if scale_percent != 100:
			self.__scale(scale_percent)
		self.visibility_button.configure(state=customtkinter.NORMAL)
		self.app.on_windows_size_change()
		self.__toggle_camera()

	def __scale(self, scale_percent: int = 100):
		if self.cap is None:
			return
		rate = scale_percent / 100
		self.__imageSize = (self.baseW * rate, self.baseH * rate)

	def __toggle_camera(self):
		if self.__reading:
			self.__reading = False
			self.visibility_button.configure(image=self.show_cam)
			self.test_label.configure(image=EMPTY_IMAGE)
		else:
			self.__reading = True
			self.visibility_button.configure(image=self.hide_cam)
			thread = Thread(target=self.__read_camera)
			thread.start()

	def __read_camera(self):
		if not self.__reading:
			return

		frame = self.video_widget.last_image
		if frame is not None:
			self.__display_image(frame)

		self.test_label.after(10, self.__read_camera)

	def __display_image(self, image: Image):
		"""Display the image passed in parameter."""
		image_array = Image.fromarray(image)
		image_to_show = customtkinter.CTkImage(image_array, size=self.__imageSize)
		self.test_label.configure(image=image_to_show)

	def on_size_change(self, width, height):
		"""Called when the windows size change."""
		super().on_size_change(width, height)

		hrate = (height * 0.5) / 480
		wrate = (width * 0.5) / 640
		rate = min(hrate, wrate)
		self.__scale(rate * 100)

	def set_inactive(self):
		super().set_inactive()
		self.app.camera.flux_reader_event.unregister(self.video_widget)

		# Set empty image
		self.test_label.configure(image=EMPTY_IMAGE)
		self.visibility_button.configure(state=customtkinter.DISABLED, image=self.show_cam)

	def set_active(self):
		super().set_active()
		self.app.camera.flux_reader_event.register(self.video_widget)
		self.__init_cap()

	def get_name(self):
		return "Run"

	def __clear_run_record_frame(self):
		print("clear run record frame")
		for widget in self.run_record_frame.grid_slaves():
			widget.grid_forget()

	def __start_recording(self):
		self.skeleton_record_saver_listener.start_timer()
		self.app.camera.flux_reader_event.register(self.skeleton_record_saver_listener)
		
		if self.visibility_button.cget("image") == self.hide_cam:
			self.start_recording.grid_forget()
			self.load_recording.grid_forget()
			self.visibility_button.grid_forget()
			self.stop_recording.grid(row=1, column=0, columnspan=2, pady=uv(10))

	def __stop_recording(self):
		# add logical
		self.app.camera.flux_reader_event.unregister(self.skeleton_record_saver_listener)
		skeleton_record = self.skeleton_record_saver_listener.save_skeletons_record()[0]
		print(skeleton_record.frame_rate)
		image = self.video_widget.last_image

		video_pop_up = customtkinter.CTkToplevel(self)
		video_pop_up_lable = customtkinter.CTkLabel(video_pop_up, text="", font=("Helvetica", 32), image=EMPTY_IMAGE)
		video_pop_up_lable.grid(row=0, column=0, columnspan=2, sticky="nsew")


		def run_playback():
			skeleton_index = 0
			while skeleton_index < len(skeleton_record.skeletons):
				if skeleton_index >= len(skeleton_record.skeletons):
					return
				skeletonned_image = image.copy()
				for skeleton in skeleton_record.skeletons[skeleton_index]:
					skeletonned_image = skeleton_visualizer(skeletonned_image, skeleton)
				image_array = Image.fromarray(skeletonned_image)
				image_to_show = customtkinter.CTkImage(image_array, size=self.__imageSize)
				video_pop_up_lable.configure(image=image_to_show)
				skeleton_index += 1
				time.sleep(1/skeleton_record.frame_rate)

		Thread(target=run_playback).start()

		self.stop_recording.grid_forget()
		self.start_recording.grid(row=1, column=0, pady=uv(10))
		self.load_recording.grid(row=1, column=1, pady=uv(10))
		self.visibility_button.grid(row=0, column=2, padx=uv(10))

	def __load_recording(self):
		print("load recording")
		self.app.show_page(RunViewerPage)

	def __slider_event(self, event):
		print("slider event")
