from .position import Position


class Skeleton:
	"""
	A class that represents keypoint of a person in an image.
	"""

	def __init__(self,
	             main_1: Position,
	             main_2: Position,
	             pied_1: Position,
	             pied_2: Position,
	             epaule_1: Position,
	             epaule_2: Position,
	             coude_1: Position,
	             coude_2: Position,
	             bassin_1: Position,
	             bassin_2: Position,
	             genou_1: Position,
	             genou_2: Position
	             ):
		"""
		Initialize the skeleton.

		:param main_1: The first hand of the person.
		:param main_2: The second hand of the person.
		:param coude_1: The first elbow of the person.
		:param coude_2: The second elbow of the person.
		:param epaule_1: The first shoulder of the person.
		:param epaule_2: The second shoulder of the person.
		:param bassin_1: The first hip of the person.
		:param bassin_2: The second hip of the person.
		:param genou_1: The first knee of the person.
		:param genou_2: The second knee of the person.
		:param pied_1: The first foot of the person.
		:param pied_2: The second foot of the person.
		"""
		self.body = {"main_1": main_1,
		             "main_2": main_2,
		             "pied_1": pied_1,
		             "pied_2": pied_2,
		             "epaule_1": epaule_1,
		             "epaule_2": epaule_2,
		             "coude_1": coude_1,
		             "coude_2": coude_2,
		             "bassin_1": bassin_1,
		             "bassin_2": bassin_2,
		             "genou_1": genou_1,
		             "genou_2": genou_2}

	def exist(self, key: str) -> bool:
		"""
		Check if the given key position (x and y) is not 0.
		"""
		if key not in self.body:
			return False
		if self.body[key].x != 0 and self.body[key].y != 0:
			return True

	def __str__(self) -> str:
		result = "body:{"
		for member in self.body:
			result += f"{member}: {self.body[member]}, "
		return result.strip(", ") + "}"

	def __repr__(self) -> str:
		return self.__str__()
