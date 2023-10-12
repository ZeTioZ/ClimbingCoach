class SkeletonScanner:
  """
  Permet de générer un squelette à partir d'un flux vidéo
  :var parcours: dictionnaire contenant les coordonnées du squelette à un temps donné.
  """
  

  def __init__(self, flux_video: str | any, frequency: int =1):
    """
    Constructeur
    :param self: SkeletonScanner
    :param flux_video: flux video, peut être un fichier ou une webcam
    :param frequency: fréquence de génération du squelette (Hz) [enregistre les coordonnées du squelette]
    """
    self.parcours: list[dict(str, tuple(float, float))] = []
    self.frequency: int = frequency
    self.flux_video: str | any = flux_video

  def getSkeleton(self, targetTime: int) -> dict({str: tuple(float, float)}):
    """
    Permet de récupérer les coordonnées du squelette à un temps donné
    :param self: SkeletonScanner
    :param targetTime: squelette d'un moment donné. (en minisecondes)
    :return: dictionnaire contenant les coordonnées du squelette.
    """
    pass

  def getParcours(self) -> list[dict({str: tuple(float, float)})]:
    """
    Permet de récupérer le parcours du squelette
    :param self: SkeletonScanner
    :return: liste contenant les coordonnées du squelette à chaque instant
    """
    pass

if(__name__ == "__main__"):
  SkSc = SkeletonScanner("test.mp4")