import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, max_hands=1):
        self.hands = mp.solutions.hands.Hands(max_num_hands=max_hands)
        self.drawing = mp.solutions.drawing_utils

    def detect_hand(self, frame):
        results = self.hands.process(frame)
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            self.drawing.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
            return True, hand_landmarks
        return False, None

    def get_cropped_hand(self, frame, hand_landmarks, margin=30):
        height, width, _ = frame.shape
        x_coords = [int(landmark.x * width) for landmark in hand_landmarks.landmark]
        y_coords = [int(landmark.y * height) for landmark in hand_landmarks.landmark]
        x_min = max(0, min(x_coords) - margin)
        x_max = min(width, max(x_coords) + margin)
        y_min = max(0, min(y_coords) - margin)
        y_max = min(height, max(y_coords) + margin)
        return frame[y_min:y_max, x_min:x_max]
