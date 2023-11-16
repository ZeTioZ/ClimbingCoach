"""Database gui instance class."""
from gui.abstract.singleton import Singleton

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


