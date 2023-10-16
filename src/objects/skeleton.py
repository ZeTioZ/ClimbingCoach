from .position import Position

class Skeleton:
  """
  A class that represents keypoint of a person in an image.
  
  :param main1: (Position): The first hand of the person.
  :param main2 (Position): The second hand of the person.
  :param pied1 (Position): The first foot of the person.
  :param pied2 (Position): The second foot of the person.
  
  Note: Droite Gauche, comment faire différence si de dos ou de face ?
  """

  def __init__(self, 
    main1: Position, 
    main2: Position, 
    pied1: Position, 
    pied2: Position,
    epaule1: Position,
    epaule2: Position,
    coude1: Position,
    coude2: Position,
    bassin1: Position,
    bassin2: Position,
    genou1: Position,
    genou2: Position
  ):
    """
    Initialize the skeleton.
    """
    
    self.main1 = main1
    self.main2 = main2
    self.pied1 = pied1
    self.pied2 = pied2
    self.epaule1 = epaule1
    self.epaule2 = epaule2
    self.coude1 = coude1
    self.coude2 = coude2
    self.bassin1 = bassin1
    self.bassin2 = bassin2
    self.genou1 = genou1
    self.genou2 = genou2

  def __str__(self) -> str:
    return f"Skeleton:\n\tmain1: {self.main1}\n\tmain2: {self.main2}\n\tpied1: {self.pied1}\n\tpied2: {self.pied2}\n\tcoude1: {self.coude1}\n\tcoude2: {self.coude2}\n\tepaule1: {self.epaule1}\n\tepaule2: {self.epaule2}\n\tbassin1: {self.bassin1}\n\tbassin2: {self.bassin2}\n\tgenou1: {self.genou1}\n\tgenou2: {self.genou2}\n"

  def __repr__(self) -> str:
    return f"Skeleton:\n\tmain1: {self.main1}\n\tmain2: {self.main2}\n\tpied1: {self.pied1}\n\tpied2: {self.pied2}\n\tcoude1: {self.coude1}\n\tcoude2: {self.coude2}\n\tepaule1: {self.epaule1}\n\tepaule2: {self.epaule2}\n\tbassin1: {self.bassin1}\n\tbassin2: {self.bassin2}\n\tgenou1: {self.genou1}\n\tgenou2: {self.genou2}\n"