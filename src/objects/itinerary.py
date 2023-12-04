from .skeleton import Skeleton


class Itinerary:
	"""
	A class that represents an itinerary of a person in an image.
	"""

	def __init__(self):
		"""
		Initializes an itinerary object.
		"""
		self.itinerary = dict()

	def add_skeleton(self, millisecond: int, skeleton: Skeleton) -> tuple[bool, str]:
		"""
		Add a skeleton to the itinerary.

		:param millisecond: The millisecond of the skeleton.
		:param skeleton: The skeleton to add.
		:return: A tuple with an error indicator (bool) and error message (str).
		"""

		if not (isinstance(millisecond, int) and isinstance(skeleton, Skeleton)):
			return False, "The millisecond must be an integer and the skeleton must be a Skeleton object"
		if millisecond in self.itinerary:
			return False, "This millisecond already exist in the itinerary"
		if millisecond < 0:
			return False, "The millisecond must be positive"

		try:
			self.itinerary[millisecond] = skeleton
			return True, "The skeleton has been added to the itinerary"
		except AttributeError:
			return False, "An error occurred while adding the skeleton to the itinerary"

	def get_skeleton(self, millisecond: int) -> Skeleton | None:
		"""
		Get the skeleton at the given millisecond.

		:param millisecond: The millisecond of the skeleton.
		:return: The skeleton at the given millisecond or None.
		"""
		if not isinstance(millisecond, int):
			return None

		if millisecond in self.itinerary:
			return self.itinerary[millisecond]
		else:
			return self.__get_closest_skeleton(millisecond)

	def __get_closest_skeleton(self, millisecond: int) -> Skeleton | None:
		"""
		Get the closest skeleton to the given millisecond.

		:param millisecond: The millisecond of the skeleton.
		:return: The closest skeleton to the given millisecond or None.
		"""
		if not isinstance(millisecond, int):
			return None

		closest = None
		for key in self.itinerary:
			if closest is None or abs(key - millisecond) < abs(closest - millisecond):
				closest = key

		return self.itinerary[closest]

	def __str__(self) -> str:
		return f"Itinerary: {self.itinerary}"
