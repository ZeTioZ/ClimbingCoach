"""Module for tkinter interface of run page."""
import os.path
import pickle

import customtkinter
from PIL import Image

from database.models.run import Run
from database.queries import run_queries
from gui.abstract.page import Page
from gui.app_state import AppState
from gui.utils import FONT, SECONDARY_COLOR, SECONDARY_HOVER_COLOR
from gui.utils import get_ressources_path, get_font_style_default, get_font_style_title
from gui.utils import v, uv, iuv
from threads import single_playback_thread, multi_playback_thread
from utils import stats_utils
from utils.serializer_utils import deserialize_skeletons_record

state = AppState()


class RunViewerPage(Page):
	"""Class of the run viewer page."""

	def __init__(self, parent: customtkinter.CTkFrame, app: customtkinter.CTk = None):
		super().__init__(parent, app)

		self.app = app
		self.popup = None
		self.choose_index = 0

		parent.grid_rowconfigure(0, weight=1)
		parent.grid_columnconfigure(0, weight=1)

		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=7)
		self.grid_rowconfigure((0, 2), weight=0, minsize=uv(80))
		self.grid_rowconfigure(1, weight=1)

		self.run_list_frame = customtkinter.CTkScrollableFrame(self, width=uv(150))
		self.run_list_frame.grid(row=1, column=0, sticky="nswe")
		self.run_list_frame.grid_columnconfigure((0, 1), weight=1)

		self.run_list_title = customtkinter.CTkLabel(self, text="Your runs", font=(FONT, iuv(28), "bold"))
		self.run_list_title.grid(row=0, column=0, sticky="nswe")

		self.run_back_button = customtkinter.CTkButton(self, text="Back", width=uv(10)
		                                               , command=self.__show_run_page
		                                               )
		self.run_back_button.grid(row=2, column=0)

		# TITLE
		self.run_detail_title = customtkinter.CTkLabel(self, text="Run", font=(FONT, iuv(32)))
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

		self.video_player_img = customtkinter.CTkImage(Image.fromarray(self.load_img),
		                                               size=(iuv(500), iuv(500 / self.ratio_img)))
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

		# RUN INFORMATIONS
		self.run_detail_description = customtkinter.CTkLabel(self.run_detail_frame, text="Run informations",
		                                                     font=(FONT, iuv(30)))
		self.run_detail_description.grid(row=4, column=0, columnspan=4, pady=uv(20))

		self.run_information_frame = customtkinter.CTkFrame(self.run_detail_frame, bg_color="transparent",
		                                                    width=uv(200))
		self.run_information_frame.grid(row=5, column=0, columnspan=4, sticky="nswe", padx=uv(20), pady=uv(20))
		self.run_information_frame.grid_columnconfigure((0, 1), weight=1)

		self.user_record_label = customtkinter.CTkLabel(self.run_information_frame, text="User record",
		                                                font=(FONT, iuv(26)))
		self.user_record_label.grid(row=0, column=0, pady=uv(5))

		self.user_derivation_label = customtkinter.CTkLabel(self.run_information_frame, text="Derivation : ",
		                                                    font=(FONT, iuv(18)))
		self.user_derivation_label.grid(row=1, column=0, pady=uv(10))

		self.user_time_label = customtkinter.CTkLabel(self.run_information_frame, text="Time : ",
		                                              font=(FONT, iuv(18)))
		self.user_time_label.grid(row=2, column=0, pady=uv(10))

		self.all_time_record_label = customtkinter.CTkLabel(self.run_information_frame, text="Best records",
		                                                    font=(FONT, iuv(26)))
		self.all_time_record_label.grid(row=0, column=1, pady=uv(5))

		self.best_derivation_label = customtkinter.CTkLabel(self.run_information_frame, text="Derivation : ",
		                                                    font=(FONT, iuv(18)))
		self.best_derivation_label.grid(row=1, column=1, pady=uv(10))

		self.best_time_label = customtkinter.CTkLabel(self.run_information_frame, text="Time : ",
		                                              font=(FONT, iuv(18)))
		self.best_time_label.grid(row=2, column=1, pady=uv(10))

		# OTHER RUNS
		self.other_runs_frame = customtkinter.CTkFrame(self.run_detail_frame)
		self.other_runs_frame.grid(row=6, column=0, columnspan=4, sticky="nswe", padx=uv(20), pady=uv(20))
		self.other_runs_frame.grid_columnconfigure(0, weight=1)

		self.other_runs_label = customtkinter.CTkLabel(self.other_runs_frame, text="Other climbers runs",
		                                               font=(FONT, iuv(26)))
		self.other_runs_label.grid(row=0, column=0, pady=uv(5), columnspan=2)

		self.scrollable_record_frame = customtkinter.CTkScrollableFrame(self.other_runs_frame, width=uv(200),
		                                                                height=uv(250), bg_color="transparent",
		                                                                fg_color="transparent")
		self.scrollable_record_frame.grid(row=1, column=0, columnspan=2, sticky="nswe")
		self.scrollable_record_frame.grid_columnconfigure((0, 1), weight=1)

		self.single_playback_thread = None

	def set_active(self):
		"""Called when the page is set as active page."""
		# get all the run in the db
		self.run_list = stats_utils.get_user_route_records(state)
		self.all_runs_button_list: list[customtkinter.CTkLabel] = []

		if len(self.run_list) > 0:
			self.derivation_stat = stats_utils.get_derivation_stat(state, self.run_list[self.choose_index])
			self.best_runs_list = stats_utils.get_all_users_route_records(state)
			self.best_time_derivation = stats_utils.get_derivation_stat(state, self.best_runs_list[0])

			self.__set_title((self.run_list[self.choose_index]).id)

			self.show_stats(self.derivation_stat,
			                self.run_list[self.choose_index].runtime,
			                self.best_time_derivation,
			                self.best_runs_list[0].runtime)

			self.button_list: list[customtkinter.CTkButton] = []
			for run in self.run_list:
				self.run_button = self.create_button(run.id, self.run_list.index(run))
				self.button_list.append(self.run_button)

			if self.best_runs_list is not None:
				index = 1
				for run in self.best_runs_list:
					self.run_label = self.create_run_label(run, index)
					self.all_runs_button_list.append(self.run_label)
					index += 1

	def __change_video_state(self):
		"""Change the state of the video."""
		if self.video_play_button.cget("image") == self.video_play_button_img:
			if not (self.popup is not None and self.popup.winfo_exists()):
				self.video_play_button.configure(image=self.video_pause_button_img)
				self.video_progressbar.configure(state='disabled')

				chosen_run: Run = self.run_list[self.choose_index]
				deserialized_skeletons_record = deserialize_skeletons_record(chosen_run.skeletons_record)
				if self.single_playback_thread is None or \
						(self.single_playback_thread.skeletons_list != deserialized_skeletons_record.skeletons):
					self.single_playback_thread = single_playback_thread.SinglePlayback(
						chosen_run,
						pickle.loads(state.get_route().image),
						deserialized_skeletons_record.frame_rate,
						self, chosen_run.runtime
					)
					self.single_playback_thread.start()
				self.single_playback_thread.play()
		else:
			self.video_play_button.configure(image=self.video_play_button_img)
			self.video_progressbar.configure(state='normal')
			if self.single_playback_thread is not None:
				self.single_playback_thread.pause()

	def show_stats(self, user_variation: float, user_time: float, best_variation: float, best_time: float):
		"""Show the stats of the run."""
		self.user_derivation_label.configure(text=f"Derivation : {user_variation} %")
		self.user_time_label.configure(text=f"Time : {user_time} s")
		self.best_derivation_label.configure(text=f"Derivation : {best_variation} %")
		self.best_time_label.configure(text=f"Time : {best_time} s")

	def __show_run_page(self):
		"""Show the page passed in parameter."""
		from gui.run_page import RunPage

		if self.app is not None:
			self.app.show_page(RunPage)

	def create_run_label(self, run: Run, index: int):
		"""Creates a label with the given text."""

		run_time = run.runtime
		display_text = f"Run {run.id} - Time : {run_time}s"

		label = customtkinter.CTkLabel(
			self.scrollable_record_frame,
			text=display_text,
			anchor="center",
			corner_radius=uv(100),
			font=get_font_style_default(self.app.winfo_width(), self.app.winfo_height())
		)

		replay_img = customtkinter.CTkImage(Image.open(self.__get_image_path("replay.png")),
		                                    size=(25, 25))
		replay_button = customtkinter.CTkButton(
			self.scrollable_record_frame,
			text="",
			width=uv(10),
			command=lambda: self.__popup_window(run, self.run_list[self.choose_index]),
			image=replay_img,
			fg_color="transparent"
		)
		label.grid(row=index, column=0, pady=uv(10), sticky="e")
		replay_button.grid(row=index, column=1, pady=uv(10), sticky="w")

		return label, replay_button

	def create_button(self, display_text, index):
		"""Creates a button with the given text."""

		is_first = index == 0
		display_text = f"Run {display_text}"

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
		display_text = f"Run {title}"
		self.run_detail_title.configure(text=display_text)

	def show_run_detail(self, run_chosen):
		"""Shows the run detail page."""
		if not self.button_list or run_chosen == self.choose_index:
			return

		for button in self.button_list:
			button.configure(fg_color="transparent")

		self.video_progressbar.set(0)

		derivation_stat = stats_utils.get_derivation_stat(state, self.run_list[self.choose_index])
		best_runs_list = stats_utils.get_all_users_route_records(state)
		best_time_derivation = stats_utils.get_derivation_stat(state, best_runs_list[0])

		self.choose_index = run_chosen
		self.button_list[run_chosen].configure(fg_color=SECONDARY_COLOR, hover_color=SECONDARY_HOVER_COLOR)

		if self.video_play_button.cget("image") == self.video_pause_button_img:
			self.__change_video_state()

		self.__set_title((self.run_list[self.choose_index]).id)
		self.show_stats(derivation_stat,
		                self.run_list[self.choose_index].runtime,
		                best_time_derivation,
		                best_runs_list[0].runtime)
		self.__update_all_runs()

	def __update_all_runs(self):
		"""Update all the runs."""
		for run in self.all_runs_button_list:
			run[0].destroy()
			run[1].destroy()
		self.all_runs_button_list = []
		index = 1
		best_runs_list = stats_utils.get_all_users_route_records(state)
		if best_runs_list is not None:
			for run in best_runs_list:
				self.run_label = self.create_run_label(run, index)
				self.all_runs_button_list.append(self.run_label)
				index += 1

	def __get_image_path(self, image_name: str):
		"""Return the path of the icon passed in parameter."""
		path = os.path.join(get_ressources_path(), 'images', image_name)
		if os.path.exists(path):
			return path
		else:
			return None

	def on_size_change(self, width, height):
		super().on_size_change(width, height)

		font_style_default = get_font_style_default(width)
		font_style_title = get_font_style_title(width)

		self.run_back_button.configure(height=v(4, height), width=uv(100),
		                               font=font_style_default)

		self.resize_image(width, height)

		if len(self.run_list) > 0:
			for button in self.button_list:
				button.configure(height=v(5, height), width=v(22, width), font=font_style_default)
		self.run_list_title.configure(font=font_style_title)
		self.run_detail_title.configure(font=font_style_title)
		self.run_detail_description.configure(font=font_style_title)

		self.user_derivation_label.configure(font=font_style_default)
		self.user_time_label.configure(font=font_style_default)
		self.best_derivation_label.configure(font=font_style_default)
		self.best_time_label.configure(font=font_style_default)
		for label in self.all_runs_button_list:
			label[0].configure(font=font_style_default)

		self.user_record_label.configure(font=font_style_title)
		self.all_time_record_label.configure(font=font_style_title)
		self.other_runs_label.configure(font=font_style_title)

	def get_name(self):
		return "Run selection"

	def __popup_window(self, run: Run, user_run: Run):
		"""Create the pop-up window."""
		if self.single_playback_thread is not None:
			self.single_playback_thread.pause()
		self.video_play_button.configure(state='disabled', image=self.video_play_button_img)
		self.video_progressbar.configure(state='disabled')
		popup = PopUp(self, run=run, user_run=user_run)
		popup.show_popup()
		popup.mainloop()

	def resize_image(self, width: int, height: int):
		image_height = int(v(50, height))
		image_width = int(image_height * self.ratio_img)
		image_size = (image_width, image_height)
		self.video_player_img.configure(size=image_size)
		self.video_player.configure(height=image_height, width=image_width)
		self.video_commands_frame.configure(width=image_width)
		self.video_progressbar.configure(width=image_width)


class PopUp(Page):
	"""Class of the pop-up page."""

	def __init__(self, parent: customtkinter.CTkFrame, run: Run, user_run: Run, app: customtkinter.CTk = None):
		super().__init__(parent, app)
		self.app = app
		self.popup = None
		self.parent = parent
		self.run = run
		self.user_run = user_run

		self.run_list = run_queries.get_runs_by_user_and_route(state.get_user().username, state.get_route().name)

		self.multi_playback_thread = None

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
		self.ratio_img = self.load_img.shape[1] / self.load_img.shape[0]

		self.video_player_img = customtkinter.CTkImage(Image.fromarray(self.load_img),
		                                               size=(iuv(500), iuv(500 / self.ratio_img)))
		self.video_player = customtkinter.CTkLabel(self.popup_frame, image=self.video_player_img,
		                                           bg_color="transparent", text="")
		self.video_player.grid(row=0, column=0, columnspan=4)

		# Video commands
		self.video_commands_frame = customtkinter.CTkFrame(self.popup_frame, bg_color="transparent")
		self.video_commands_frame.grid(row=1, column=0, sticky="nsew")
		self.video_commands_frame.grid_columnconfigure((0, 1), weight=1)

		self.video_play_button_img = customtkinter.CTkImage(Image.open(self.__get_image_path("play_button.png")),
		                                                    size=(31, 31))
		self.video_pause_button_img = customtkinter.CTkImage(Image.open(self.__get_image_path("pause_button.png")),
		                                                     size=(30, 30))
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
			self.video_progressbar.configure(state='disabled')

			chosen_run = self.run
			deserialized_skeletons_record = deserialize_skeletons_record(chosen_run.skeletons_record)
			size = (iuv(500), iuv(500 / self.ratio_img))
			if self.multi_playback_thread is None or \
					(self.multi_playback_thread.main_skeletons_list != deserialized_skeletons_record.skeletons):
				self.multi_playback_thread = multi_playback_thread.MultiPlayback(chosen_run,
				                                                                 self.user_run,
				                                                                 pickle.loads(state.get_route().image),
				                                                                 deserialized_skeletons_record.frame_rate,
				                                                                 self,
				                                                                 chosen_run.runtime,
				                                                                 size)
				self.multi_playback_thread.start()
			self.multi_playback_thread.play()
		else:
			self.video_play_button.configure(image=self.video_play_button_img)
			self.video_progressbar.configure(state='normal')
			if self.multi_playback_thread is not None:
				self.multi_playback_thread.pause()

	def __get_image_path(self, image_name: str):
		"""Return the path of the icon passed in parameter."""
		path = os.path.join(get_ressources_path(), 'images', image_name)
		if os.path.exists(path):
			return path
		else:
			return None
