from ultralytics import YOLO


class ModelLoader:
    def __init__(self, model_path):
        self.model = YOLO(model_path)


    def predict(self, image, classes=None, img_size=(640,640)):
        predictions = self.model(image, classes=classes, device='0', imgsz=img_size)
        return predictions
