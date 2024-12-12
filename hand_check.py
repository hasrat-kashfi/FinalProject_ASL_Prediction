import cv2
from gui import start_gui
from hand_detector import HandDetector
from model_prediction import YOLOModel
from gui import load_fasttext_model

# Initialize Hand Detector and YOLO Model
hand_detector = HandDetector(max_hands=1)
model = YOLOModel(r'C:\Users\user\Downloads\NewBase\ComputerVision\Updated files\best.pt')
fasttext_model = load_fasttext_model()

def main():
    # Start GUI
    start_gui(hand_detector, model, fasttext_model)

if __name__ == "__main__":
    main()
