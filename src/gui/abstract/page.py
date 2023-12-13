from customtkinter import CTkFrame, CTk


class Page(CTkFrame):
	app = None

	def __init__(self, parent: CTkFrame, app: CTk, *args, **kwargs):
		"""Constructor."""
		super().__init__(parent)
		self.app = app

	def on_size_change(self, width, height):
		"""Called when the window size change."""
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
