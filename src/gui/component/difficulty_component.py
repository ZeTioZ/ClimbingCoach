import customtkinter as ctk

from gui.utils import COLOR_DIFFICULTY, min_max_range, uv, v

class DifficultyComponent(ctk.CTkFrame):

	def __init__(self, master, **kw):
		super().__init__(master, fg_color="transparent", **kw)
		self.__init_components()

	def __init_components(self):
		self.grid_columnconfigure((1, 2, 3, 4, 5), weight=1)
		self.grid_columnconfigure((0, 6), weight=2)

		self.difficulty = self.__create_difficulty_circles()
	
	def __create_difficulty_circles(self) -> list[ctk.CTkFrame]:
		difficulty_circles = []
		for i in range(5):
			difficulty_circle = self.__create_difficulty_circle()
			difficulty_circle.grid(row=0, column=i+1, padx=uv(5))
			difficulty_circles.append(difficulty_circle)
		return difficulty_circles
	
	def __create_difficulty_circle(self) -> ctk.CTkFrame:
		difficulty_circle = ctk.CTkFrame(
			self, corner_radius=uv(1000),
			fg_color="green", border_color="white",
			width=uv(25), height=uv(25), 
		)
		return difficulty_circle

	# Set difficulty

	def set_difficulty(self, difficulty: int):
		"""Set the difficulty of the route."""

		if difficulty < 1 or difficulty > 5:
			raise ValueError("difficulty must be in [1..5]")

		for i in range(5):
			if i <= difficulty - 1:
				self.difficulty[i].configure(fg_color=COLOR_DIFFICULTY[i], border_width=0)
			else:
				self.difficulty[i].configure(fg_color="transparent", border_width=uv(2))
	
	# Component lifecycle

	def resize(self, width: int, height: int):
		size_difficulty = min_max_range(uv(15), uv(100), v(2.5, width))
		for i in range(5):
			self.difficulty[i].configure(width=size_difficulty, height=size_difficulty)