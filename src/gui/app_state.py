"""Database gui instance class."""
from gui.abstract.singleton import Singleton
import pickle
import os
from gui.utils import RESSOURCES_PATH
from utils.camera_discover_utils import get_available_cameras_names

class AppState(metaclass=Singleton):

    CONFIG_FILE_NAME = 'configuration_app_state.pickle'

    # Constructor
    def __init__(self):
        """Constructor. Singleton then init executed only once."""
        self.__load_configurations()
    
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
        return os.path.join(RESSOURCES_PATH, self.CONFIG_FILE_NAME)


    # Trail
    __trail: int | None = None


    def get_trail(self) -> int | None:
        """Return the trail. (Id of the current selected trail)"""
        return self.__trail
    

    def set_trail(self, trail: int | None):
        """Set the trail. (Id of the current selected trail)"""
        if trail is not None and trail < 0: 
            print("set_trail error: trail < 0\nNormalize to None")
            trail = None
        if trail is None: self.set_run(None)
        self.__trail = trail


    def is_trail_selected(self) -> bool:
        """Return true if a trail is selected."""
        return self.__trail is not None
    

    # Run
    __run: int | None = None


    def get_run(self) -> int | None:
        """Return the run. (Id of the current selected run)"""
        return self.__run
    

    def set_run(self, run: int | None):
        """Set the run. (Id of the current selected run)"""
        if run is not None and run < 0: 
            print("set_run error: run < 0\nNormalize to None")
            run = None
        self.__run = run
    

    def is_run_selected(self) -> bool:
        """Return true if a run is selected."""
        return self.__run is not None

    #Login
    def set_username(self, username: str):
        
        assert username is not None, "app_state: Username is set to None"
        assert username != "", "app_state: Username is set to empty string"
        assert isinstance(username, str), "app_state: Username is not a string"

        self.__username = username


    def get_username(self) -> str:
        """Return the username."""
        if self.__username is None: return ""
        return self.__username

    # Camera
    __camera_name: str = None


    def get_camera_name(self) -> str:
        """Return the camera name."""
        return self.__camera_name
    

    def get_index_camera(self) -> int:
        """Return the index of the camera."""
        cameras = get_available_cameras_names()
        if self.__camera_name in cameras: 
            return str(cameras.index(self.__camera_name))
        else: 
            return "0"


    def set_camera_name(self, camera_name: str):
        """Set the camera name."""

        assert camera_name is not None, "app_state: Camera_name is set to None"
        assert camera_name != "", "app_state: Camera_name is set to empty string"
        assert isinstance(camera_name, str), "app_state: Camera_name is not a string"

        self.__camera_name = camera_name
        self.__save_configurations()



if __name__ == "__main__":
    app_state = AppState()
    print(app_state.get_camera_name())
    app_state.set_camera_name(get_available_cameras_names()[0])
    print(app_state.get_camera_name())
    print(app_state.get_index_camera())
    app_state.set_camera_name("")