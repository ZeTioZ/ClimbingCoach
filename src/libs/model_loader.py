from ultralytics import YOLO
from utils.torch_utils import get_device


class ModelLoader:
    def __init__(self, model_path):
        self.model = YOLO(model_path)


    def predict(self, image, classes=None, img_size=(640,640), device: str|None = None):
        if device is None:
            device = get_device()
        predictions = self.model(image, classes=classes, device=device, imgsz=img_size, verbose=False)
        return predictions
