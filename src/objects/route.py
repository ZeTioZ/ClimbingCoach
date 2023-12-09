from objects.box import Box


class Route:
	"""
	Route class representing a climbing route using a list of holds
	"""

	def __init__(self, name: str | None = None, holds: list[Box] = None):
		"""
		Initializes the Route object with the given name and list of holds.
		:param name: The name of the route.
		:param holds: A list of Hold objects representing the available holds in the route.
		"""
		self.name = name
		self.holds = holds if holds is not None else []

	def add_step(self, hold: Box) -> None:
		"""
		Adds a new step to the route.

		:param hold: The hold of the new step.
		"""
		self.holds.append(hold)

	def remove_step(self, hold: Box) -> None:
		"""
		Removes a step from the route.

		:param hold: The hold of the step to remove.
		"""
		self.holds.remove(hold)

	def clear(self) -> None:
		"""
		Clears the route.
		"""
		self.holds.clear()
	
	def set_name(self, name: str) -> None:
		"""
		Sets the name of the route.

		:param name: The new name of the route.
		:raises Exception: If the name of the route is already set.
		"""
		if not self.is_name_set():
			self.name = name
		else:
			raise AttributeError("The name of the route is already set.")

	def is_name_set(self) -> bool:
		"""
		:return: True if the name of the route is set, False otherwise.
		"""
		return self.name is not None

	def get_name(self) -> str:
		"""
		:return: The name of the route.
		"""
		return self.name

	def get_holds(self) -> list:
		"""
		:return: A list of Hold objects representing the holds in the current route.
		"""
		return self.holds

	def is_hold_in_route(self, hold: Box) -> bool:
		"""
		Checks if a hold is in the route.

		:param hold: The hold to check.
		:return: True if the hold is in the route, False otherwise.
		"""
		return hold in self.holds
