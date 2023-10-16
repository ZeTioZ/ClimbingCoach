import os, cv2, time

# Type import
from cv2.typing import MatLike

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog

from .draw_utils import skeleton_visualizer
from objects.skeleton import Skeleton
from objects.position import Position
from objects.itinerary import Itinerary


class SkeletonScanner:
  """
  Permet de générer un squelette à partir d'un flux vidéo
  :var parcours: dictionnaire contenant les coordonnées du squelette à un temps donné.
  """
  def __init__(self, flux_video: str|int, frequency: int =1, model_device: str ="cpu", threshold: float = 0.7):
    """
    Constructeur
    
    :param self: SkeletonScanner
    :param flux_video: flux video, peut être un fichier ou une webcam
    :param frequency: fréquence de génération du squelette (Hz) [enregistre les coordonnées du squelette]
    """

    if frequency <= 0: raise ValueError("frequency must be positive")

    self.parcours: Itinerary = Itinerary()
    self.flux_video: str|int = flux_video
    self.frequency: int = 1 if flux_video in range(0,3) else frequency
    self.model_device: str = model_device
    self.threshold: float = threshold

    # default value
    self.predictor: DefaultPredictor = None
    self.video: cv2.VideoCapture = None
    self.cfg = None
    
    success, err_msg = self.loadVideo(flux_video)
    if not success: raise ValueError(err_msg)
    self.__loadModel()
    

  def loadVideo(self, flux_video: str|int) -> tuple[bool, str]:
    """
    Permet de charger le flux vidéo
    :param flux_video: flux video, peut être un fichier (str) ou une webcam (int)
    """

    if os.path.exists(flux_video):
      self.video = cv2.VideoCapture(flux_video)
      self.is_video_file = True
      return True, None
    
    elif type(flux_video) == int:
      self.video = cv2.VideoCapture(flux_video)
      if not self.video.isOpened(): return False, "webcam not found"
      self.is_video_file = False
      return True, None
    
    else:
      return False, "flux_video must be a file or a webcam"
    

  def __loadModel(self) -> tuple[bool, str]:
    """
    Permet de charger le modèle de détection de squelette
    """

    if self.predictor != None: return False, "model already loaded"
    if self.cfg != None: return False, "model already loaded"

    self.cfg = get_cfg() #config model
    self.cfg.MODEL.DEVICE = self.model_device
    self.cfg.merge_from_file(model_zoo.get_config_file("COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml"))
    self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = self.threshold  # set threshold for this model
    self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Keypoints/keypoint_rcnn_R_50_FPN_3x.yaml")
    self.predictor = DefaultPredictor(self.cfg)

    
  def generateSkeleton(self, image: MatLike) -> tuple[bool, str|Skeleton]:
    """
    Permet de générer un squelette à partir d'une image
    :param image: image à analyser (MatLike)
    """

    if self.predictor == None: return False, "model not loaded"
    # if isinstance(image, MatLike): return False, "image must be a MatLike object" Error: TypeError: issubclass() argument 2 cannot be a parameterized generic
  
    outputs = self.predictor(image)
      
    for keypoint in outputs["instances"].pred_keypoints:

      # Récupération des coordonnées des mains et des pieds
      metadata = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0])

      #('nose', 'left_eye', 'right_eye', 'left_ear', 'right_ear', 'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow', 'left_wrist', 'right_wrist', 'left_hip', 'right_hip', 'left_knee', 'right_knee', 'left_ankle', 'right_ankle')
      # Créer squelette objet
      skeleton = Skeleton(
        main_1 = Position(keypoint[metadata.keypoint_names.index("left_wrist")][0], keypoint[metadata.keypoint_names.index("left_wrist")][1]),
        main_2 = Position(keypoint[metadata.keypoint_names.index("right_wrist")][0], keypoint[metadata.keypoint_names.index("right_wrist")][1]),
        pied_1 = Position(keypoint[metadata.keypoint_names.index("left_ankle")][0], keypoint[metadata.keypoint_names.index("left_ankle")][1]),
        pied_2 = Position(keypoint[metadata.keypoint_names.index("right_ankle")][0], keypoint[metadata.keypoint_names.index("right_ankle")][1]),
        epaule_1 = Position(keypoint[metadata.keypoint_names.index("left_shoulder")][0], keypoint[metadata.keypoint_names.index("left_shoulder")][1]),
        epaule_2 = Position(keypoint[metadata.keypoint_names.index("right_shoulder")][0], keypoint[metadata.keypoint_names.index("right_shoulder")][1]),
        coude_1 = Position(keypoint[metadata.keypoint_names.index("left_elbow")][0], keypoint[metadata.keypoint_names.index("left_elbow")][1]),
        coude_2 = Position(keypoint[metadata.keypoint_names.index("right_elbow")][0], keypoint[metadata.keypoint_names.index("right_elbow")][1]),
        bassin_1 = Position(keypoint[metadata.keypoint_names.index("left_hip")][0], keypoint[metadata.keypoint_names.index("left_hip")][1]),
        bassin_2 = Position(keypoint[metadata.keypoint_names.index("right_hip")][0], keypoint[metadata.keypoint_names.index("right_hip")][1]),
        genou_1 = Position(keypoint[metadata.keypoint_names.index("left_knee")][0], keypoint[metadata.keypoint_names.index("left_knee")][1]),
        genou_2 = Position(keypoint[metadata.keypoint_names.index("right_knee")][0], keypoint[metadata.keypoint_names.index("right_knee")][1])
      )

      return True, skeleton
    return False, "no skeleton found"


  def generateParcours(self) -> tuple[bool, str|Itinerary]:
    """
    Permet de générer un parcours à partir du flux vidéo
    """
    if self.video == None: return False, "video not loaded"
    if self.predictor == None: return False, "model not loaded"

    if round(self.video.get(cv2.CAP_PROP_FPS), 0) <= self.frequency:
      local_frequency = int(self.video.get(cv2.CAP_PROP_FPS))
    else:
      local_frequency = self.frequency

    frame_count = 0
    success = True
    while success:
      time_start = time.time()
      success, image = self.video.read()
      if not success:
        print("Video finished")
        break
      
      # test_value =int(frame_count) % (int(self.video.get(cv2.CAP_PROP_FPS))/local_frequency)
      if int(frame_count) % (int(self.video.get(cv2.CAP_PROP_FPS))/local_frequency) == 0 or self.flux_video in range(0,3):
        gene_ske_success, skeleton = self.generateSkeleton(image)
        cv2.imshow("Skeleton", skeleton_visualizer(image, skeleton))
        cv2.waitKey(1)
        if not gene_ske_success: print(skeleton)
        else: 
          ms = int((frame_count/self.video.get(cv2.CAP_PROP_FPS))*1000)
          print(f"milisec: {ms}\nframe_count: {frame_count}\n{skeleton}\n")
          add_success, add_message = self.parcours.add_skeleton(ms, skeleton)
          if not add_success: print(add_message)

      # time.sleep(int((1000/self.video.get(cv2.CAP_PROP_FPS))/1000))
      if self.flux_video in range(0,3):
        dTime = time.time() - time_start
        if dTime < (1/local_frequency): time.sleep((1/local_frequency) - dTime)
      frame_count += (self.video.get(cv2.CAP_PROP_FPS))*(time.time() - time_start) if self.flux_video in range(0,3) else 1

    return True, self.parcours