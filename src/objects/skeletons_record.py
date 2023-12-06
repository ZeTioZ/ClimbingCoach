class SkeletonsRecord:
	"""
	This class is used to represent a list of skeleton record.
	"""

	def __init__(self, frame_rate: float = 30.0):
		self.frame_rate = frame_rate
		self.skeletons = []

	def append(self, skeletons: list):
		"""
		Records the given skeletons for each person into the list of skeletons.

		:param skeletons: The skeletons of each person seen during the record.
		"""
		self.skeletons.append(skeletons)

	def get_skeletons(self) -> list:
		"""
		Returns the list of skeletons.

		:return: The list of skeletons.
		"""
		return self.skeletons

	def __str__(self) -> str:
		result = ""
		for skeleton in self.skeletons:
			result += str(skeleton) + "\n"
		return result
