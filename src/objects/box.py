from .position import Position

class Box:
    """
    A class that represents a box of an object in the image.

    Args:
        position1 (Position): The first position of the box.
        position2 (Position): The second position of the box.
    """
    def __init__(self, position1: Position, position2: Position) -> None:
        """
        Initializes the box of an object in the image.
        """
        self.position1 = position1
        self.position2 = position2
    

    def __str__(self) -> str:
        """
        Returns a string representation of the Position object.
        """
        return "Box: ({}, {})".format(self.position1, self.position2)
    

    def get_center(self) -> Position:
        """
        Returns the center of the box.
        """
        return Position((self.position1.x + self.position2.x) / 2, (self.position1.y + self.position2.y) / 2)
    

    def get_width(self) -> float:
        """
        Returns the width of the box.
        """
        return abs(self.position1.x - self.position2.x)
    

    def get_height(self) -> float:
        """
        Returns the height of the box.
        """
        return abs(self.position1.y - self.position2.y)
    

    def get_area(self) -> float:
        """
        Returns the area of the box.
        """
        return self.get_width() * self.get_height()
    
    
    def collide(self, position: Position) -> bool:
        """
        Returns whether the given position collides with the box.
        """
        max_x1 = max(self.position1.x, self.position2.x)
        min_x1 = min(self.position1.x, self.position2.x)
        max_y1 = max(self.position1.y, self.position2.y)
        min_y1 = min(self.position1.y, self.position2.y)
        return min_x1 <= position.x <= max_x1 and min_y1 <= position.y <= max_y1
    

    def collide(self, box) -> bool:
        """
        Returns whether the given box collides with the box.
        """
        return self.collide(box.position1) or \
               self.collide(box.position2) or \
               self.collide(Position(box.position1.x, box.position2.y)) or \
               self.collide(Position(box.position2.x, box.position1.y))
