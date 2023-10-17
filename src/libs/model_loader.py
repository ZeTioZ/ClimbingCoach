from ultralytics import YOLO


class ModelLoader:
    def __init__(self, model_path):
        self.model = YOLO(model_path)


    def predict(self, image):
        predictions = self.model(image)
        return predictions
