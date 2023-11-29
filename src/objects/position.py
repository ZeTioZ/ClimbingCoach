class Position:
	"""
	A class that represents a position in the image.
	"""

	def __init__(self, x, y):
		"""
		Initializes the Position of a point in the image.

		:param x (float): The x coordinate of the position.
		:param y (float): The y coordinate of the position.
		"""
		self.x = x
		self.y = y

	def to_tuple(self) -> tuple:
		return int(self.x), int(self.y)

	def __str__(self) -> str:
		"""
		Returns a string representation of the Position object.
		"""
		return "Position: ({}, {})".format(self.x, self.y)

	def __repr__(self) -> tuple:
		return self.to_tuple()
