"""Database gui instance class."""
from gui.singleton import Singleton

class AppState(metaclass=Singleton):

    # Constructor
    def __init__(self):
        """Constructor. Singleton then init executed only once."""
        pass

    # Trail
    __trail: int | None = None


    def get_trail(self) -> int | None:
        """Return the trail. (Id of the current selected trail)"""
        return self.__trail
    

    def set_trail(self, trail: int | None):
        """Set the trail. (Id of the current selected trail)"""
        self.__trail = trail


    def is_trail_selected(self) -> bool:
        """Return true if a trail is selected."""
        return self.__trail is not None