from ultralytics import YOLO

class YOLOModel:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.class_names = [
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' '
        ]

    def predict(self, image):
        results = self.model(image)
        top_class_idx = results[0].probs.top1
        top_confidence = results[0].probs.top1conf
        return self.class_names[top_class_idx], top_confidence
