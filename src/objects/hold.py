from .box import Box

class Hold:
    """
    A class that represents a hold of a climbing wall in an image.
    """
    def __init__(self, box : Box):
        """ 
        Initializes a Hold object with a box object.

        :param box: A box object that represents the bounding box of the hold.
        """
        self.box = box
        # TODO: Add other attributes to the Hold object.
    

    def __str__(self) -> str:
        """
        :return: A string representation of the Position object.
        """
        return str(self.box)


    def get_center(self) -> tuple:
        """
        :return: A tuple representing the center of the hold.
        """
        return self.box.get_center()
