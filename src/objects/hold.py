from .box import Box

class Hold:
    """
    A class that represents a hold of a climbing wall in an image.

    Args:
        box : A box object that represents the bounding box of the hold.
    """
    def __init__(self, box : Box):
        """ 
        Initializes a Hold object with a box object.
        """
        self.box = box
    

    def __str__(self) -> str:
        """
        Returns a string representation of the Position object.
        """
        return str(self.box)
