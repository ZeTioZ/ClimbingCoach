"""Module for tkinter interface of run page."""
import os.path
import pickle

import customtkinter
from PIL import Image

from database.queries import run_queries
from gui.abstract.page import Page
from gui.app_state import AppState
from gui.utils import FONT, SECONDARY_COLOR, SECONDARY_HOVER_COLOR
from gui.utils import get_parent_path
from gui.utils import v, uv, iuv, min_max_range
from threads import playback_thread
from utils.serializer_utils import deserialize_skeletons_record

state = AppState()


class RunViewerPage(Page):
	"""Class of the run viewer page."""
	choose_index = 0  # Index of the page we are on

	def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk = None):
		super().__init__(parent, app)

		self.app = app
		self.popup = None

		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=7)
		self.grid_rowconfigure((0, 2), weight=0, minsize=uv(80))
		self.grid_rowconfigure(1, weight=1)

		self.run_list_frame = customtkinter.CTkScrollableFrame(self, width=uv(150))
		self.run_list_frame.grid(row=1, column=0, sticky="nswe")
		self.run_list_frame.grid_columnconfigure((0, 1), weight=1)

		self.run_list_title = customtkinter.CTkLabel(self, text="Run list", font=(FONT, iuv(28), "bold"))
		self.run_list_title.grid(row=0, column=0, sticky="nswe")

		self.run_back_button = customtkinter.CTkButton(self, text="Back", width=uv(10)
		                                               , command=self.__show_run_page
		                                               )
		self.run_back_button.grid(row=2, column=0)

		# TITLE
		self.run_detail_title = customtkinter.CTkLabel(self, text="Run 1", font=(FONT, iuv(32)))
		self.run_detail_title.grid(row=0, column=1, columnspan=4, pady=uv(25))

		# RIGHT FRAME
		self.run_detail_frame = customtkinter.CTkScrollableFrame(self, width=uv(170), bg_color="transparent")
		self.run_detail_frame.grid(row=1, column=1, rowspan=2, sticky="nswe")
		self.run_detail_frame.configure(fg_color="transparent")

		self.run_detail_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
		self.run_detail_frame.grid_rowconfigure(0, weight=4)
		self.run_detail_frame.grid_rowconfigure((1, 2, 3, 4), weight=1)

		# STREAM
		self.load_img = pickle.loads(state.get_route().image)
		self.ratio_img = self.load_img.shape[1] / self.load_img.shape[0]
		print(self.ratio_img)
		self.video_player_img = customtkinter.CTkImage(Image.fromarray(self.load_img), size=(iuv(500), iuv(500/self.ratio_img)))
		self.video_player = customtkinter.CTkLabel(self.run_detail_frame, image=self.video_player_img,
		                                           bg_color="transparent", text="")	
		self.video_player.grid(row=0, column=0, columnspan=4)


		# VIDEO COMMANDS
		self.video_commands_frame = customtkinter.CTkFrame(self.run_detail_frame, bg_color="transparent")
		self.video_commands_frame.grid(row=3, column=0, columnspan=4, pady=uv(10))
		self.video_commands_frame.grid_columnconfigure((0, 1, 2), weight=1)

		self.video_play_button_img = customtkinter.CTkImage(Image.open(self.__get_image_path("play_button.png")),
		                                                    size=(31, 31))
		self.video_pause_button_img = customtkinter.CTkImage(Image.open(self.__get_image_path("pause_button.png")),
		                                                     size=(30, 30))
		self.video_play_button = customtkinter.CTkButton(self.video_commands_frame, text="", width=uv(10),
		                                                 image=self.video_play_button_img, fg_color="transparent",
		                                                 command=self.__change_video_state)
		self.video_play_button.grid(row=0, column=0)
		self.video_progressbar = customtkinter.CTkSlider(self.video_commands_frame, from_=0, to=100)
		self.video_progressbar.set(0)
		self.video_progressbar.grid(row=0, column=1, pady=uv(9))
		self.video_pop_up_button_img = customtkinter.CTkImage(Image.open(self.__get_image_path("pop_up.png")),
		                                                      size=(30, 30))
		self.video_pop_up_button = customtkinter.CTkButton(self.video_commands_frame, text="", width=uv(10),
		                                                   command=self.__popup_window,
		                                                   image=self.video_pop_up_button_img, fg_color="transparent")
		self.video_pop_up_button.grid(row=0, column=2)

		# RUN INFORMATIONS
		self.run_detail_description = customtkinter.CTkLabel(self.run_detail_frame, text="Run informations",
		                                                     font=(FONT, iuv(30)))
		self.run_detail_description.grid(row=4, column=0, columnspan=4, pady=uv(20))

		self.run_information_frame = customtkinter.CTkFrame(self.run_detail_frame, bg_color="transparent")
		self.run_information_frame.grid(row=5, column=0, columnspan=4, sticky="nswe", padx=uv(20), pady=uv(20))
		self.run_information_frame.grid_columnconfigure((0, 1), weight=1)

		self.user_record_label = customtkinter.CTkLabel(self.run_information_frame, text="User record",
		                                                font=(FONT, iuv(26)))
		self.user_record_label.grid(row=0, column=0, pady=uv(5))

		self.all_time_record_label = customtkinter.CTkLabel(self.run_information_frame, text="All time record",
		                                                    font=(FONT, iuv(26)))
		self.all_time_record_label.grid(row=0, column=1, pady=uv(5))

		# OTHER RUNS
		self.other_runs_frame = customtkinter.CTkFrame(self.run_detail_frame, bg_color="transparent",
		                                               fg_color="transparent")
		self.other_runs_frame.grid(row=6, column=0, columnspan=4, sticky="nswe", padx=uv(20), pady=uv(20))
		self.other_runs_frame.grid_columnconfigure((0, 1), weight=1)

		self.user_runs_label = customtkinter.CTkLabel(self.other_runs_frame, text="Your runs", font=(FONT, iuv(26)))
		self.user_runs_label.grid(row=0, column=0, pady=uv(5))

		self.other_runs_label = customtkinter.CTkLabel(self.other_runs_frame, text="All runs", font=(FONT, iuv(26)))
		self.other_runs_label.grid(row=0, column=1, pady=uv(5))

		# get all the run in the db
		self.run_list = run_queries.get_runs_by_user(state.get_user().username)

		if len(self.run_list) > 0:
			#TODO: faire appel aux stats des autres ici 
			user_record_list = self.__get_user_record()
			all_time_record_list = self.__get_all_time_record()

			self.button_list: list[customtkinter.CTkButton] = []
			for run in self.run_list:
				self.run_button = self.create_button(run.id, self.run_list.index(run))
				self.button_list.append(self.run_button)

			self.user_record_button_list: list[customtkinter.CTkButton] = []
			for user_record in user_record_list:
				self.record_button = self.create_label(user_record, (user_record_list.index(user_record)) + 1, 0)
				self.user_record_button_list.append(self.record_button)

			self.all_time_record_button_list: list[customtkinter.CTkButton] = []
			for all_time_record in all_time_record_list:
				self.all_time_record_button = self.create_label(all_time_record,
																(all_time_record_list.index(all_time_record)) + 1, 1)
				self.all_time_record_button_list.append(self.all_time_record_button)

		self.playback_thread = None

	def set_active(self):
		"""Called when the page is set as active page."""
		# get all the run in the db
		self.run_list = run_queries.get_runs_by_user(state.get_user().username)
		if len(self.run_list) > 0:
			#TODO: faire appel aux stats des autres ici 
			user_record_list = self.__get_user_record()
			all_time_record_list = self.__get_all_time_record()

			self.button_list: list[customtkinter.CTkButton] = []
			for run in self.run_list:
				self.run_button = self.create_button(run.id, self.run_list.index(run))
				self.button_list.append(self.run_button)

			self.user_record_button_list: list[customtkinter.CTkButton] = []
			for user_record in user_record_list:
				self.record_button = self.create_label(user_record, (user_record_list.index(user_record)) + 1, 0)
				self.user_record_button_list.append(self.record_button)

			self.all_time_record_button_list: list[customtkinter.CTkButton] = []
			for all_time_record in all_time_record_list:
				self.all_time_record_button = self.create_label(all_time_record,
																(all_time_record_list.index(all_time_record)) + 1, 1)
				self.all_time_record_button_list.append(self.all_time_record_button)


	def __change_video_state(self):
		"""Change the state of the video."""
		if self.video_play_button.cget("image") == self.video_play_button_img:
			if not (self.popup is not None and self.popup.winfo_exists()):
				self.video_play_button.configure(image=self.video_pause_button_img)
				self.video_progressbar.configure(state='disabled')
				
				choosen_run = self.run_list[self.choose_index]
				deserialized_skeletons_record = deserialize_skeletons_record(choosen_run.skeletons_record)
				if self.playback_thread is None or \
					(self.playback_thread.skeletons_list != deserialized_skeletons_record.skeletons):
					self.playback_thread = playback_thread.Playback(pickle.loads(state.get_route().image), deserialized_skeletons_record.frame_rate, deserialized_skeletons_record.skeletons, self, choosen_run.runtime)
					self.playback_thread.start()
				self.playback_thread.play()
		else:
			self.video_play_button.configure(image=self.video_play_button_img)
			self.video_progressbar.configure(state='normal')
			if self.playback_thread is not None:
				self.playback_thread.pause()

	def __show_run_page(self):
		"""Show the page passed in parameter."""
		from gui.run_page import RunPage

		if self.app is not None:
			self.app.show_page(RunPage)


	def create_label(self, display_text, index, column):
		"""Creates a label with the given text."""

		self.label = customtkinter.CTkLabel(
			self.run_information_frame,
			text=display_text,
		)

		self.label.grid(row=index, column=column, padx=uv(10), sticky="ew", pady=uv(10))
		return self.label

	def create_button(self, display_text, index):
		"""Creates a button with the given text."""

		is_first = index == 0

		self.button = customtkinter.CTkButton(
			self.run_list_frame,
			text=display_text,
			fg_color=SECONDARY_COLOR if is_first else "transparent",
			hover_color=SECONDARY_COLOR,
			border_spacing=uv(17),
			command=lambda: self.show_run_detail(index),
			anchor="w"
		)

		self.button.grid(row=index, column=0, padx=uv(10), sticky="ew")
		return self.button

	def __set_title(self, title: str):
		"""Set the title of the page."""
		self.run_detail_title.configure(text=title)

	def __fetch_run_list(self):
		"""Fetch the run list from the database."""
		return [f"Run {i}" for i in range(1, 13)]
		# return [f"Run {run}" for run in route_queries.get_all_routes()]

	def __fetch_run_detail(self):
		"""Fetch the run detail from the database."""
		return {"title": f"Run {self.choose_index + 1}"}

	def __get_user_record(self):
		"""Return the user record of the run."""
		return [f"User record {i}" for i in range(1, 3)]

	def __get_all_time_record(self):
		"""Return the all-time record of the run."""
		return [f"All time record {i}" for i in range(1, 3)]

	def show_run_detail(self, run_chosen):
		"""Shows the run detail page."""
		if not self.button_list or run_chosen == self.choose_index:
			return

		for button in self.button_list:
			button.configure(fg_color="transparent")

		self.video_progressbar.set(0)
		
		self.choose_index = run_chosen
		self.button_list[run_chosen].configure(fg_color=SECONDARY_COLOR, hover_color=SECONDARY_HOVER_COLOR)

		current_run = self.__fetch_run_detail()
		self.__set_title(current_run["title"])

	def __skeleton_loader(self, image_name: str):
		pass

	def __get_run_path(self, run_image_name: str):
		"""Return the path of the run passed in parameter."""
		pass

	def __get_image_path(self, image_name: str):
		"""Return the path of the icon passed in parameter."""
		parent_path = get_parent_path(__file__, 3)
		path = os.path.join(parent_path, 'resources', 'images', image_name)
		if os.path.exists(path):
			return path
		else:
			return None

	def on_size_change(self, width, height):
		super().on_size_change(width, height)

		self.run_back_button.configure(height=v(4, height), width=uv(100),
		                               font=(FONT, min_max_range(iuv(8), iuv(28), int(v(1.9, width)))))

		image_size = min_max_range(uv(75), uv(1000), v(22, width))
		self.video_player_img.configure(size=(image_size, image_size/self.ratio_img))
		self.video_player.configure(height=iuv(image_size), width=iuv(image_size))
		self.video_commands_frame.configure(width=iuv(image_size))
		self.video_progressbar.configure(width=iuv(image_size))

		font_style_default = (FONT, min_max_range(iuv(8), iuv(28), int(v(1.9, width))))
		font_style_title = (FONT, min_max_range(iuv(12), iuv(32), int(v(2.5, width))), "bold")

		if len(self.run_list) > 0:
			for button in self.button_list:
				button.configure(height=v(5, height), width=image_size, font=font_style_default)
		self.run_list_title.configure(font=font_style_title)
		self.run_detail_title.configure(font=font_style_title)
		self.run_detail_description.configure(font=font_style_title)

		self.user_record_label.configure(font=font_style_title)
		self.all_time_record_label.configure(font=font_style_title)
		self.user_runs_label.configure(font=font_style_title)
		self.other_runs_label.configure(font=font_style_title)

	def get_name(self):
		return "Run selection"

	def __popup_window(self):
		"""Create the pop-up window."""
		self.video_play_button.configure(state='disabled', image=self.video_play_button_img)
		self.video_progressbar.configure(state='disabled')
		# pause video
		popup = PopUp(self, self.app)
		popup.show_popup()
		popup.mainloop()


class PopUp(Page):
	"""Class of the pop-up page."""

	def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk = None):
		super().__init__(parent, app)
		self.app = app
		self.popup = None
		self.parent = parent

	def show_popup(self):
		"""Show a popup if there isn't one already."""
		if self.popup is None or not self.popup.winfo_exists():
			self.popup = self.__create_pop_up()
		self.after(200, self.popup.lift)

	def on_close(self):
		"""Called when the popup window is closed."""
		self.parent.video_play_button.configure(state='normal')
		self.parent.video_progressbar.configure(state='normal')
		self.parent.video_progressbar.set(self.video_progressbar.get())
		self.popup.destroy()

	def __create_pop_up(self):
		"""Create the pop-up window."""
		popup = customtkinter.CTkToplevel(self)
		popup.grid_columnconfigure(0, weight=1)
		popup.grid_rowconfigure((0, 1), weight=1)

		popup.title("Run viewer")
		popup.resizable(False, False)
		popup.protocol("WM_DELETE_WINDOW", self.on_close)

		# Create a frame for the popup to hold all other widgets
		self.popup_frame = customtkinter.CTkFrame(popup)
		self.popup_frame.grid(row=0, column=0, sticky="nswe")

		# Stream
		self.load_img = pickle.loads(state.get_route().image)
		self.video_player_img = customtkinter.CTkImage(Image.fromarray(self.load_img), size=(iuv(680), iuv(680)))
		self.video_player = customtkinter.CTkLabel(self.popup_frame, image=self.video_player_img,
		                                           bg_color="transparent", text="")
		self.video_player.grid(row=0, column=0, columnspan=4)

		# Video commands
		self.video_commands_frame = customtkinter.CTkFrame(self.popup_frame, bg_color="transparent")
		self.video_commands_frame.grid(row=1, column=0, sticky="nsew")
		self.video_commands_frame.grid_columnconfigure((0, 1), weight=1)

		self.video_play_button_img = customtkinter.CTkImage(
			Image.open(os.path.join("resources", "images", "play_button.png")), size=(51, 51))
		self.video_pause_button_img = customtkinter.CTkImage(
			Image.open(os.path.join("resources", "images", "pause_button.png")), size=(50, 50))
		self.video_play_button = customtkinter.CTkButton(self.video_commands_frame, text="", width=uv(10),
		                                                 image=self.video_play_button_img, fg_color="transparent",
		                                                 command=self.__change_video_state)
		self.video_play_button.grid(row=0, column=0)
		self.video_progressbar = customtkinter.CTkSlider(self.video_commands_frame, from_=0, to=100, width=uv(600))
		self.video_progressbar.set(self.parent.video_progressbar.get())
		self.video_progressbar.grid(row=0, column=1, sticky="ew")
		return popup

	def __change_video_state(self):
		"""Change the state of the video."""
		if self.video_play_button.cget("image") == self.video_play_button_img:
			self.video_play_button.configure(image=self.video_pause_button_img)
		else:
			self.video_play_button.configure(image=self.video_play_button_img)
