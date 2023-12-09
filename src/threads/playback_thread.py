from threading import Thread

import PIL.Image as Image
import customtkinter
import numpy as np
from gui.utils import v, uv, min_max_range
from gui.abstract.page import Page

from utils import draw_utils


class Playback(Thread):
	def __init__(self, image: np.ndarray, frame_rate: float, skeletons_list: list, parent_page: Page, runtime: float = 0):
		super().__init__()
		self.daemon = True
		self.frame_rate = frame_rate
		self.skeletons_list = skeletons_list
		self.image = image
		self.label_img: customtkinter.CTkLabel = parent_page.video_player
		self.runtime = runtime
		self.video_progressbar: customtkinter.CTkProgressBar = parent_page.video_progressbar
		self.play_value = False
		self.parent_page = parent_page

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

				for skeleton in skeletons:
					image_copy = draw_utils.skeleton_visualizer(image_copy, skeleton)

				size = self.get_size_img(image_copy)
				draw_image = customtkinter.CTkImage(Image.fromarray(image_copy), size=size)
				self.label_img.configure(image=draw_image, width=size[0], height=size[1])
				self.video_progressbar.set((skeletons_index / (len(self.skeletons_list) - 1)) * 100)
				skeletons_index += 1
				self.label_img.after(int(1000 / self.frame_rate), self.frame_draw_loop, skeletons_index)
			else:
				self.play_value = False

	def get_size_img(self, img: np.ndarray):
		ratio = img.shape[1] / img.shape[0]
		width = self.parent_page.app.winfo_width()
		target_width = min_max_range(uv(75), uv(1000), v(22, width))
		target_height = target_width / ratio
		return target_width, target_height

	def play(self):
		self.play_value = True

	def pause(self):
		self.play_value = False

	def stop(self):
		pass
