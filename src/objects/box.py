from .position import Position

class Box:
    """
    A class that represents a box of an object in the image.
    """
    def __init__(self, position_1: Position, position_2: Position) -> None:
        """
        Initializes the box of an object in the image.

        :param position_1 (Position): The first position of the box.
        :param position_2 (Position): The second position of the box.
        """
        self.positions = [position_1, position_2]
    

    def __str__(self) -> str:
        """
        :return: A string representation of the Position object.
        """
        return "Box: ({}, {})".format(self.positions[0], self.positions[1])
    

    def get_center(self) -> Position:
        """
        :return: The center of the box.
        """
        return Position((self.positions[0].x + self.positions[1].x) / 2, (self.positions[0].y + self.positions[1].y) / 2)
    

    def get_width(self) -> float:
        """
        :return: The width of the box.
        """
        return abs(self.positions[0].x - self.positions[1].x)
    

    def get_height(self) -> float:
        """
        :return: The height of the box.
        """
        return abs(self.positions[0].y - self.positions[1].y)
    

    def get_area(self) -> float:
        """
        :return: The area of the box.
        """
        return self.get_width() * self.get_height()
    
    
    def position_collide(self, position: Position, margin = 0) -> bool:
        """
        Returns whether the given position collides with the box.
        
        :param position: The position to check.
        :param margin: The margin to add to the position turning it into a box.
        :return: A boolean indicating whether the given position collides with the box.
        """
        if margin > 0:
            max_pos_x = position.x + margin
            min_pos_x = position.x - margin
            max_pos_y = position.y + margin
            min_pos_y = position.y - margin
            margin_box = Box(Position(min_pos_x, min_pos_y), Position(max_pos_x, max_pos_y))
            return self.box_collide(margin_box)

        max_x1 = max(self.positions[0].x, self.positions[1].x)
        min_x1 = min(self.positions[0].x, self.positions[1].x)
        max_y1 = max(self.positions[0].y, self.positions[1].y)
        min_y1 = min(self.positions[0].y, self.positions[1].y)

        return min_x1 <= position.x <= max_x1 and min_y1 <= position.y <= max_y1
    

    def box_collide(self, box) -> bool:
        """
        Returns whether the given box collides with the box.

        :param box: The box to check.
        :return: A boolean indicating whether the given box collides with the box.
        """
        return self.position_collide(box.positions[0]) or \
               self.position_collide(box.positions[1]) or \
               self.position_collide(Position(box.positions[0].x, box.positions[1].y)) or \
               self.position_collide(Position(box.positions[1].x, box.positions[0].y))
