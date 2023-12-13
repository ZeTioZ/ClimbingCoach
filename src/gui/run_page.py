"""Module tkinter for the test page."""
import os.path
from threading import Thread

import customtkinter
import cv2
from PIL import Image

from database.queries import run_queries
from enums.flux_reader_event_type import FluxReaderEventType
from gui.abstract.page import Page
from gui.app_state import AppState
from gui.run_viewer_page import RunViewerPage
from gui.utils import EMPTY_IMAGE, FONT, uv, v, get_font_style_default, get_font_style_title
from listeners.skeleton_listener import SkeletonRecordSaverListener
from listeners.video_widget import VideoWidget

state = AppState()

class RunPage(Page):
	__reading = False
	__isCameraLoaded = False
	__imageSize = None
	__pop_up = None

	def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk):
		"""Constructor."""
		super().__init__(parent, app)

		app_width = app.winfo_width()
		app_height = app.winfo_height()

		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.grid_columnconfigure((0, 1), weight=2)
		self.grid_columnconfigure(2, weight=1)
		self.grid_rowconfigure(0, weight=4)
		self.grid_rowconfigure(1, weight=1)

		self.video_widget = VideoWidget([FluxReaderEventType.FRAME_PROCESSED_EVENT])
		self.skeleton_record_saver_listener: SkeletonRecordSaverListener = SkeletonRecordSaverListener()

		v_width, v_height = self.__get_image_size_from_app_size()

		default_font = get_font_style_default(app_width, app_height)
		title_font = get_font_style_title(app_width, app_height)

		self.test_label = customtkinter.CTkLabel(self, text="", font=title_font, width=v_width,
		                                         height=v_height)
		self.test_label.grid(row=0, column=0, columnspan=2, sticky="nsew")

		b_width, b_height = self.__get_button_size(app_width, app_height)
		self.start_recording = customtkinter.CTkButton(self, text="Start recording", command=self.__start_recording,
		                                               font=default_font, width=b_width, height=b_height)
		self.start_recording.grid(row=1, column=0, pady=uv(10))

		self.load_recording = customtkinter.CTkButton(self, text="Load recording", command=self.__load_recording,
		                                              font=default_font, width=b_width, height=b_height)
		self.load_recording.grid(row=1, column=1, pady=uv(10))

		self.stop_recording = customtkinter.CTkButton(self, text="Stop recording", command=self.__stop_recording,
		                                              font=default_font, fg_color="#dc3835", hover_color="#ae1e1d",
													  width=b_width, height=b_height)

		vb_width, vb_height = self.__get_visibility_button_size(self.app.winfo_width(), self.app.winfo_height())

		self.show_cam = customtkinter.CTkImage(dark_image=Image.open(self.__get_icon_path("show_cam.png")),
		                                       size=(vb_width - 25, vb_height - 25))
		self.hide_cam = customtkinter.CTkImage(dark_image=Image.open(self.__get_icon_path("hide_cam.png")),
		                                       size=(vb_width - 25, vb_height - 25))
		
		
		self.visibility_button = customtkinter.CTkButton(self, text="", command=self.__toggle_camera,
		                                                 state=customtkinter.NORMAL, image=self.hide_cam,
		                                                 width=vb_width, height=vb_height)
		self.visibility_button.grid(row=0, column=2, padx=uv(10))

		self.camLoader = None

	def __get_icon_path(self, icon_name: str):
		"""Return the path of the icon passed in parameter."""
		return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'resources',
		                    'images', icon_name)

	def __start_loading_animation(self):
		"""Start the loading animation."""
		self.__isCameraLoaded = False
		self.__animation_camera_loading()

	def __animation_camera_loading(self):
		if self.__isCameraLoaded:
			self.test_label.configure(text="")
			return
		inner_text = self.test_label.cget("text")
		if len(inner_text) > 3:
			inner_text = ""
		inner_text += "."
		self.test_label.configure(text=inner_text)
		
		self.after(1000, self.__animation_camera_loading)

	def __get_ratio(self) -> float:
		"""
		return the ratio of the camera (width / height)
		"""
		cap = self.app.camera.flux_reader_event.video
		width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
		height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

		return width / height

	def __get_image_size(self, width: int, height: int) -> tuple[int, int]:
		"""
		return the size of the image to display
		"""
		ratio = self.__get_ratio()
		target_height = v(50, height)
		target_width = target_height * ratio
		return int(target_width), int(target_height)
	
	def __get_image_size_from_app_size(self) -> tuple[int, int]:
		return self.__get_image_size(self.app.winfo_width(), self.app.winfo_height())

	def __get_button_size(self, width: int, height: int) -> tuple[int, int]:
		"""
		return the size of the image to display
		"""
		target_height = v(7, height)
		target_width = v(15, width)
		return int(target_width), int(target_height)

	def __toggle_camera(self):
		if self.__reading:
			self.__stop_reading()
		else:
			self.__start_reading()

	def __start_reading(self):
		self.__reading = True
		self.visibility_button.configure(image=self.hide_cam)
		thread = Thread(target=self.__read_camera)
		thread.start()
		self.__start_loading_animation()

	def __stop_reading(self):
		self.__reading = False
		self.visibility_button.configure(image=self.show_cam)
		self.test_label.configure(image=EMPTY_IMAGE)

	def __read_camera(self):
		if not self.__reading:
			return

		frame = self.video_widget.last_image
		if frame is not None:
			self.__display_image(frame)

		self.test_label.after(10, self.__read_camera)

	def __display_image(self, image: Image):
		"""Display the image passed in parameter."""
		self.__isCameraLoaded = True
		image_array = Image.fromarray(image)
		image_to_show = customtkinter.CTkImage(image_array, size=self.__get_image_size_from_app_size())
		self.test_label.configure(image=image_to_show, text="")

	def set_inactive(self):
		super().set_inactive()
		self.app.camera.flux_reader_event.unregister(self.video_widget)

		self.__stop_reading()

		# Set empty image
		self.test_label.configure(image=EMPTY_IMAGE)
		# self.visibility_button.configure(state=customtkinter.DISABLED, image=self.show_cam)

	def set_active(self):
		super().set_active()
		self.app.camera.flux_reader_event.register(self.video_widget)

		self.__start_reading()
		# self.visibility_button.configure(state=customtkinter.NORMAL, image=self.show_cam)

	def get_name(self):
		return "Run"

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
		self.skeleton_record_saver_listener.save_skeletons_record()

		self.stop_recording.grid_forget()
		self.start_recording.grid(row=1, column=0, pady=uv(10))
		self.load_recording.grid(row=1, column=1, pady=uv(10))
		self.visibility_button.grid(row=0, column=2, padx=uv(10))

	def __load_recording(self):
		self.run_list = run_queries.get_runs_by_user_and_route(state.get_user().username, state.get_route().name)
		if len(self.run_list) == 0:
			if self.__pop_up is None:	
				self.__pop_up = customtkinter.CTkToplevel(self)
				self.__pop_up.title("Warning")
				self.__pop_up.geometry("300x100")
				self.__pop_up.resizable(False, False)
				self.__pop_up.grid_columnconfigure(0, weight=1)
				self.__pop_up.grid_rowconfigure((0,1), weight=1)
				__pop_up_label = customtkinter.CTkLabel(self.__pop_up, text="You have no run for this route", font=(FONT, 18))
				__pop_up_label.grid(row=0, column=0, sticky="nswe")
				__pop_up_button = customtkinter.CTkButton(self.__pop_up,
											  			text="Ok",
														command=self.__close_pop_up,
														font=(FONT, 16))
				__pop_up_button.grid(row=1, column=0)
		else:
			self.app.show_page(RunViewerPage)

	def __close_pop_up(self):
		self.__pop_up.destroy()
		self.__pop_up = None

	def __get_visibility_button_size(self, width: int, height: int) -> tuple[int, int]:
		"""
		return the size of the image to display
		"""
		target_height = v(7, height)
		target_width = target_height
		return int(target_width), int(target_height)

	def on_size_change(self, width, height):
		"""Called when the windows size change."""
		super().on_size_change(width, height)

		default_font = get_font_style_default(width, height)
		title_font = get_font_style_title(width, height)

		b_width, b_height = self.__get_button_size(width, height)

		self.start_recording.configure(font=title_font, width=b_width, height=b_height)
		self.load_recording.configure(font=title_font, width=b_width, height=b_height)
		self.stop_recording.configure(font=title_font, width=b_width, height=b_height)

		v_width, v_height = self.__get_image_size_from_app_size()
		self.test_label.configure(width=v_width, height=v_height, font=title_font)
		image: customtkinter.CTkImage = self.test_label.cget("image")
		if image is not None:
			image.configure(size=(v_width, v_height))

		vb_width, vb_height = self.__get_visibility_button_size(width, height)
		self.visibility_button.configure(width=vb_width, height=vb_height)

		self.show_cam.configure(size=(vb_width - 25, vb_height - 25))
		self.hide_cam.configure(size=(vb_width - 25, vb_height - 25))

		