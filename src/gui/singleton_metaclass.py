class singleton_page():

    __instance = None

    @classmethod
    def get_instance(cls, parent):
        """Return the instance of the login page."""
        if cls.__instance is None:
            cls.__instance = cls(parent)
        return cls.__instance