"""
Database gui instance class.
"""
import os
import pickle

from database.models.wall import Wall
from gui.abstract.singleton import Singleton
from gui.utils import get_ressources_path
from database.models.user import User
from objects.route import Route


class AppState(metaclass=Singleton):
	CONFIG_FILE_NAME = 'configuration_app_state.pickle'

	# Constructor
	def __init__(self):
		"""Constructor. Singleton then init executed only once."""
		self.__user = None
		self.__camera_name = ""
		self.__load_configurations()
		self.__route: int | None = None
		self.__wall: int | None = None

	# Configuration
	def __load_configurations(self):
		"""Load configurations from the configuration file."""

		if self.__configuration_file_exists():
			# Load dictionary from file
			with open(self.CONFIG_FILE_NAME, 'rb') as f:
				config = pickle.load(f)
			self.__set_value_from_configuration(config)

	def __save_configurations(self):
		"""Save configurations to the configuration file."""

		# Create dictionary
		config = self.__get_value_as_dictionary()

		# Save dictionary to file
		with open(self.CONFIG_FILE_NAME, 'wb') as f:
			pickle.dump(config, f, pickle.HIGHEST_PROTOCOL)

	def __get_value_as_dictionary(self) -> dict:
		"""Return the value of the attributes as a dictionary."""
		return {
			'camera_name': self.__camera_name
		}

	def __set_value_from_configuration(self, config: dict):
		"""Set the value of the attributes from the dictionary."""
		self.__camera_name = config['camera_name']

	def __configuration_file_exists(self) -> bool:
		"""Return True if file exists, False otherwise."""
		return os.path.isfile(self.__get_configuration_file_path())

	def __get_configuration_file_path(self) -> str:
		"""Return the configuration file path."""
		return os.path.join(get_ressources_path(), self.CONFIG_FILE_NAME)

	def get_wall(self) -> Wall | None:
		"""Return the wall."""
		return self.__wall

	def set_wall(self, wall: Wall | None):
		"""Set the wall."""
		if wall is not None:
			print("set_trail error: trail < 0\nNormalize to None")
			wall = None
		else:
			self.set_route(None)
		self.__wall = wall

	def is_wall_selected(self) -> bool:
		"""Return true if a wall is selected."""
		return self.__wall is not None

	# TODO: Change the injection of this function into path_page.py
	def get_route(self) -> Route | None:
		"""Return the route."""
		return self.__route

	# TODO: Change the injection of this function into path_page.py
	def set_route(self, route: Route | None):
		"""Set the route."""
		if route is not None:
			print("set_run error: run < 0\nNormalize to None")
			route = None
		self.__route = route

	def is_route_selected(self) -> bool:
		"""Return true if a route is selected."""
		return self.__route is not None

	# Login	
	def set_user(self, user: User):
		assert user is not None, "app_state: user is set to None"
		assert user != "", "app_state: user is set to empty string"
		self.__user = user

	def get_user(self) -> User | None:
		"""Return the user."""
		if self.__user is None:
			return None
		return self.__user

	def get_camera_name(self) -> str:
		"""Return the camera name."""
		return self.__camera_name

	def get_index_camera(self) -> int:
		# """Return the index of the camera."""
		# cameras = get_available_cameras_names()
		# if self.__camera_name in cameras:
		#     return str(cameras.index(self.__camera_name))
		# else:
		# Wasn't working on macOS that's why it's commented
		return 1

	def set_camera_name(self, camera_name: str):
		"""Set the camera name."""
		assert camera_name is not None, "app_state: Camera_name is set to None"
		assert camera_name != "", "app_state: Camera_name is set to empty string"
		assert isinstance(camera_name, str), "app_state: Camera_name is not a string"

		self.__camera_name = camera_name
		self.__save_configurations()
