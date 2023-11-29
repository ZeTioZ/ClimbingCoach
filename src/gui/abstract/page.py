from customtkinter import CTkFrame, CTk

from gui.abstract.singleton import Singleton


class Page(CTkFrame, metaclass=Singleton):
	app = None

	def __init__(self, parent: CTkFrame, app: CTk, *args, **kwargs):
		"""Constructor. Singleton then init executed only once."""
		super().__init__(parent)
		self.app = app

	def on_size_change(self, width, height):
		"""Called when the windows size change."""
		pass

	def update(self, *args, **kwargs):
		"""Update the page."""
		pass

	def set_inactive(self):
		"""Set the page inactive."""
		pass

	def set_active(self):
		"""Set the page active."""
		pass

	def get_name(self):
		"""Return the name of the page."""
		return self.__class__.__name__
