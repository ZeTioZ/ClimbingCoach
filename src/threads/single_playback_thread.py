import pickle
from threading import Thread

import PIL.Image as Image
import customtkinter
import numpy as np

from database.models.run import Run
from gui.abstract.page import Page
from gui.utils import v
from objects.skeletons_record import SkeletonsRecord
from utils import draw_utils


class SinglePlayback(Thread):
	def __init__(self, run: Run, image: np.ndarray, frame_rate: float, parent_page: Page, runtime: float = 0, size: tuple = None):
		super().__init__()
		self.daemon = True
		self.frame_rate = frame_rate
		self.image = image
		self.label_img: customtkinter.CTkLabel = parent_page.video_player
		self.runtime = runtime
		self.video_progressbar: customtkinter.CTkProgressBar = parent_page.video_progressbar
		self.play_value = False
		self.parent_page = parent_page
		self.size = size

		sk_record: SkeletonsRecord = pickle.loads(run.skeletons_record)
		self.skeletons_list = sk_record.get_skeletons()
		self.selected_run_hit_holds = pickle.loads(run.holds)

	def get_current_progress(self):
		index = int((self.video_progressbar.get() / 100) * (len(self.skeletons_list) - 1))
		return index

	def run(self):
		self.label_img.after(10, self.frame_draw_loop, self.get_current_progress())

	def frame_draw_loop(self, skeletons_index):
		if self.play_value:
			if skeletons_index < len(self.skeletons_list):

				skeletons = self.skeletons_list[skeletons_index]
				image_copy = self.image.copy()

				image_with_hit_hold = self.__draw_hit_holds(image_copy)
				image_with_hit_hold_and_skeleton = image_with_hit_hold
				for skeleton in skeletons:
					image_with_hit_hold_and_skeleton = draw_utils.skeleton_visualizer(image_with_hit_hold_and_skeleton, skeleton)

				if image_with_hit_hold_and_skeleton is not None:
					if self.size is None:
						size = self.get_size_img(image_with_hit_hold_and_skeleton)
					else:
						size = self.size
					draw_image = customtkinter.CTkImage(Image.fromarray(image_with_hit_hold_and_skeleton), size=size)
					self.label_img.configure(image=draw_image, width=size[0], height=size[1])
				self.video_progressbar.set((skeletons_index / (len(self.skeletons_list) - 1)) * 100)
				skeletons_index += 1
				self.label_img.after(int(1000 / self.frame_rate), self.frame_draw_loop, skeletons_index)
			else:
				self.play_value = False

	def get_size_img(self, img: np.ndarray):
		ratio = img.shape[1] / img.shape[0]
		height = self.parent_page.app.winfo_height()
		target_height = int(v(50, height))
		target_width = target_height * ratio
		
		return target_width, target_height
	
	def __draw_hit_holds(self, image: np.ndarray) -> np.ndarray:
		return draw_utils.box_visualizer(image, self.selected_run_hit_holds, color=(36, 143, 109))

	def play(self):
		self.play_value = True

	def pause(self):
		self.play_value = False
