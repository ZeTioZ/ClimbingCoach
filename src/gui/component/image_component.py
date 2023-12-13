import customtkinter as ctk
import numpy as np
from PIL import Image

from gui.utils import min_max_range, uv, v


class ImageComponent(ctk.CTkLabel):

	def __init__(self, master, app_width: int | None = None, app_height: int | None = None, width_percentage: int = 22, **kw):
		super().__init__(master, text= "", **kw)
		self.__set_max_size(app_width, app_height)
		self.wp = width_percentage
	
	# Set image

	def set_image(self, image: Image.Image | np.ndarray):

		if isinstance(image, np.ndarray):
			image_usable = self.__array_to_image(image)
		else:
			image_usable = image

		image_size = self.__get_image_ration_safe(image_usable)

		route_image = ctk.CTkImage(image_usable, size= image_size)
		self.configure(image= route_image)

	def __array_to_image(self, image: np.ndarray) -> Image.Image:
		return Image.fromarray(image)

	# Utils
	
	def __get_image_ration_safe(self, image: Image.Image) -> tuple[int, int]:
		raw_size = image.size
		return self.__get_image_ration_safe_by_size(raw_size)

	def __get_image_ration_safe_by_size(self, size: tuple[int, int]) -> tuple[int, int]:
		if size[0] > size[1]:
			rate = self.max_size[0] / size[0]
			image_size = (size[0] * rate, size[1] * rate)
		else:
			rate = self.max_size[1] / size[1]
			image_size = (size[0] * rate, size[1] * rate)

		return image_size
	
	def __set_max_size(self, width: int | None, height: int | None):
		if width is None or width < 1 or height is None or height < 1:
			self.max_size = (1, 1)
		else:
			max_dim_size = min_max_range(uv(75), uv(1000), v(self.wp, width))
			self.max_size = (max_dim_size, max_dim_size)

	# Component lifecycle

	def resize(self, width: int, height: int):
		self.__set_max_size(width, height)

		image_ctk: ctk.CTkImage = self.cget("image")
		
		if image_ctk is not None:
			image_size = self.__get_image_ration_safe_by_size(image_ctk.cget("size"))
			image_ctk.configure(size=image_size)
