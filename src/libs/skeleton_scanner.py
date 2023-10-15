class SkeletonScanner:
  """
  Permet de générer un squelette à partir d'un flux vidéo
  :var parcours: dictionnaire contenant les coordonnées du squelette à un temps donné.
  """
  

  def __init__(self, flux_video: str, frequency: int =1):
    """
    Constructeur
    :param self: SkeletonScanner
    :param flux_video: flux video, peut être un fichier ou une webcam
    :param frequency: fréquence de génération du squelette (Hz) [enregistre les coordonnées du squelette]
    """
    self.parcours: list[dict(str, tuple)] = []
    self.frequency: int = frequency
    self.flux_video: str = flux_video

  def getSkeleton(self, targetTime: int) -> dict({str: tuple}):
    """
    Permet de récupérer les coordonnées du squelette à un temps donné
    :param self: SkeletonScanner
    :param targetTime: squelette d'un moment donné. (en minisecondes)
    :return: dictionnaire contenant les coordonnées du squelette.
    """
    pass

  def getParcours(self) -> list[dict({str: tuple})]:
    """
    Permet de récupérer le parcours du squelette
    :param self: SkeletonScanner
    :return: liste contenant les coordonnées du squelette à chaque instant
    """
    pass

if(__name__ == "__main__"):
  import torch, detectron2
  from detectron2.utils.logger import setup_logger
  setup_logger()

  import numpy as np
  import os, json, cv2, random

  # import some common detectron2 utilities
  from detectron2 import model_zoo
  from detectron2.engine import DefaultPredictor
  from detectron2.config import get_cfg
  from detectron2.utils.visualizer import Visualizer
  from detectron2.data import MetadataCatalog, DatasetCatalog

  MODEL_DEVICE = "cpu"
  MODEL_DIRECTORY = "./resources/model/COCO/keypoint/"
  VIDEO_DIRECTORY = "./resources/videos/"
  frame_count = 0
  frame_rate = 1

  video = cv2.VideoCapture(os.path.join(VIDEO_DIRECTORY, "Escalade_Fixe.mp4"))
  # im = cv2.imread("resources/images/image0.jpg")

  if not video.isOpened():
    print("Error: Could not open video file.")
    exit()

  cfg = get_cfg()
  cfg.MODEL.DEVICE = MODEL_DEVICE
  # cfg.merge_from_file(os.path.join(MODEL_DIRECTORY, "keypoint_rcnn_R_50_FPN_3x.yaml"))
  cfg.merge_from_file(model_zoo.get_config_file("COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml"))
  cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7  # set threshold for this model
  # cfg.MODEL.WEIGHTS = os.path.join(MODEL_DIRECTORY, "keypoint_rcnn_R_50_FPN_3x.yaml")
  cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml")
  predictor = DefaultPredictor(cfg)

  success, image = video.read()
  while success:
    success, image = video.read()
    if not success:
      print("Error: Could not read frame.")
      break
    
    if frame_count % (frame_rate * round(video.get(cv2.CAP_PROP_FPS), 0)) == 0:
      print("Frame count: " + str(frame_count))
      outputs = predictor(image)
      
      for keypoint in outputs["instances"].pred_keypoints:
        # Récupération des coordonnées des mains et des pieds
        # keypoints = outputs["instances"].pred_keypoints[0]  # Points clés du premier objet détecté
        metadata = MetadataCatalog.get(cfg.DATASETS.TRAIN[0])

        # Obtenez les indices des points clés pour les mains et les pieds
        mains_indices = [metadata.keypoint_names.index("left_wrist"), metadata.keypoint_names.index("right_wrist")]
        pieds_indices = [metadata.keypoint_names.index("left_ankle"), metadata.keypoint_names.index("right_ankle")]

        # Récupérez les coordonnées des mains et des pieds
        coordonnees_mains = keypoint[mains_indices][:, :2]
        coordonnees_pieds = keypoint[pieds_indices][:, :2]

        print("Coordonnées des mains :")
        print(coordonnees_mains)
        print("Coordonnées des pieds :")
        print(coordonnees_pieds)

    frame_count += 1

  # v = Visualizer(im[:,:,::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
  # out = v.draw_instance_predictions(outputs["instances"].to(MODEL_DEVICE))
  # cv2.imshow("test", out.get_image()[:, :, ::-1])
  # cv2.waitKey()