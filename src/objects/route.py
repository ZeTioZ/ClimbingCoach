from .hold import Hold


class Route:
	"""
	Route class representing a climbing route using a list of holds
	"""

	def __init__(self, name: str, route: list = list()):
		"""
		Initializes the RouteConfigurator object with the given list of holds.
		:param name: The name of the route.
		:param route: A list of Hold objects representing the available holds in the route.
		"""
		self.name = name
		self.route = route

	def add_step(self, hold: Hold) -> None:
		"""
		Adds a new step to the route.

		:param hold: The hold of the new step.
		"""
		self.route.append(hold)

	def remove_step(self, hold: Hold) -> None:
		"""
		Removes a step from the route.

		:param hold: The hold of the step to remove.
		"""
		self.route.remove(hold)

	def clear(self) -> None:
		"""
		Clears the route.
		"""
		self.route.clear()

	def get_name(self) -> str:
		"""
		:return: The name of the route.
		"""
		return self.name

	def get_route(self) -> list:
		"""
		:return: A list of Hold objects representing the holds in the current route.
		"""
		return self.route
