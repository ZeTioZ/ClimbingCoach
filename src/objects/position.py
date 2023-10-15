class Position:
    """
    A class that represents a position in the image.

    Args:
        x (float): The x coordinate of the position.
        y (float): The y coordinate of the position.
    """
    def __init__(self, x, y):
        """
        Initializes the Position of a point in the image.
        """
        self.x = x
        self.y = y
    

    def __str__(self):
        """
        Returns a string representation of the Position object.
        """
        return "Position: ({}, {})".format(self.x, self.y)
