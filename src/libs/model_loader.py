from ultralytics import YOLO


class ModelLoader:
    def __init__(self, model_path):
        self.model = YOLO(model_path)


    def predict(self, image, classes=None):
        predictions = self.model(image, classes=classes)
        return predictions
