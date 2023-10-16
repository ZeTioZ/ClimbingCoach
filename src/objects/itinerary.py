from .skeleton import Skeleton

class Itinerary:
  """
  A class that represents an itinerary of a person in an image.
  """

  def __init__(self, itinerary: dict = dict()):
    """
    Initializes an itinerary object.

    :param itinerary: The itinerary of the person.
    """
    self.itinerary = dict()
    pass

  def add_skeleton(self, milisec: int, skeleton: Skeleton) -> tuple[bool, str]:
    """
    Add a skeleton to the itinerary.

    :param milisec: The milisec of the skeleton.
    :param skeleton: The skeleton to add.
    :return: A tuple with a error indicator (bool) and error message (str).
    """

    if not (isinstance(milisec, int) and isinstance(skeleton, Skeleton)):
      return (False, "The milisec must be an integer and the skeleton must be a Skeleton object")
    if milisec in self.itinerary:
      return (False, "This milisec already exist in the itinerary")
    if milisec < 0:
      return (False, "The milisec must be positive")
    
    try:
      self.itinerary[milisec] = skeleton
      return (True, "The skeleton has been added to the itinerary")
    except:
      return (False, "An error occured while adding the skeleton to the itinerary")
    
  def get_skeleton(self, milisec: int) -> Skeleton:
    """
    Get the skeleton at the given milisec.

    :param milisec: The milisec of the skeleton.
    :return: The skeleton at the given milisec or None.
    """
    if not isinstance(milisec, int):
      return None
    
    if milisec in self.itinerary:
      return self.itinerary[milisec]
    else:
      return self.__get_closest_skeleton(milisec)

  def __get_closest_skeleton(self, milisec: int) -> Skeleton:
    """
    Get the closest skeleton to the given milisec.
    
    :param milisec: The milisec of the skeleton.
    :return: The closest skeleton to the given milisec or None.
    """
    if not isinstance(milisec, int):
      return None
    
    closest = None
    for key in self.itinerary:
      if closest == None or abs(key - milisec) < abs(closest - milisec):
        closest = key
        
    
    return self.itinerary[closest]

  def __str__(self) -> str:
    return f"Itinerary: {self.itinerary}"