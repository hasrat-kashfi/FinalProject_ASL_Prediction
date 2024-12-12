import tkinter as tk
from tkinter import Label, Button
from PIL import Image, ImageTk
import cv2
import time
import os

import gensim.downloader as api

# Load pre-trained FastText word vectors
def load_fasttext_model():
    print("Loading FastText model...")
    model = api.load("fasttext-wiki-news-subwords-300")  # Pre-trained FastText model
    print("Model loaded successfully.")
    return model

# Predict word completions
def predict_words(prefix, model, top_n=3):
    if len(prefix) < 2:
        return "Please enter at least 2 characters."
    
    # Get all words in the FastText model's vocabulary
    vocabulary = model.key_to_index.keys()
    
    # Find words that start with the given prefix
    matching_words = [word for word in vocabulary if word.startswith(prefix)]
    
    # If there are no matches
    if not matching_words:
        return f"No predictions found for prefix '{prefix}'."
    
    # Rank by frequency (model inherently provides frequency through key_to_index)
    ranked_words = sorted(matching_words, key=lambda x: model.key_to_index[x])
    
    # Return the top_n results
    return ranked_words[:top_n]

def start_gui(hand_detector, model, fasttext_model):
    root = tk.Tk()
    root.title("Sign Language to Text Conversion")
    root.attributes('-fullscreen', True)
    root.configure(bg="#1c1c1c")  # Dark theme

    # Header
    header_label = Label(
        root, text="Sign Language to Text Conversion",
        font=("Helvetica", 24, "bold"),
        bg="#1c1c1c", fg="#ffffff"
    )
    header_label.pack(pady=10)

    # Video frame
    video_label = Label(root, bg="#1c1c1c")
    video_label.pack(expand=True, padx=20, pady=10)

    # Instructions label
    instructions_label = Label(
        root, text="Put your hand inside the detection box",
        font=("Helvetica", 16), bg="#1c1c1c", fg="#cccccc"
    )
    instructions_label.pack(pady=10)

    # Prediction display
    prediction_frame = tk.Frame(root, bg="#1c1c1c")
    prediction_frame.place(relx=0.05, rely=0.85, anchor="w")

    character_label = Label(prediction_frame, text="Character: ", font=("Helvetica", 18), bg="#1c1c1c", fg="#ffffff")
    character_label.pack(anchor="w")

    confidence_label = Label(prediction_frame, text="Confidence: ", font=("Helvetica", 18), bg="#1c1c1c", fg="#ffffff")
    confidence_label.pack(anchor="w")

    sentence_label = Label(prediction_frame, text="Sentence: ", font=("Helvetica", 18), bg="#1c1c1c", fg="#ffffff")
    sentence_label.pack(anchor="w")

    word_prediction_label = Label(prediction_frame, text="Word Predictions: ", font=("Helvetica", 18), bg="#1c1c1c", fg="#ffffff")
    word_prediction_label.pack(anchor="w")

    # Variables
    captured_text = ""
    last_capture_time = 0
    resume_detection_time = 0
    capture_interval = 3  # Time between captures

    # Create directory for captures
    capture_folder = os.path.join(os.getcwd(), "Captures")
    os.makedirs(capture_folder, exist_ok=True)

    cap = cv2.VideoCapture(0)

    def update_frame():
        nonlocal captured_text, last_capture_time, resume_detection_time
        ret, frame = cap.read()
        if not ret:
            return

        current_time = time.time()

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        hand_detected, hand_landmarks = hand_detector.detect_hand(frame_rgb)

        # Bounding box in the center
        height, width, _ = frame.shape
        square_size = 300
        top_left_x = (width - square_size) // 2
        top_left_y = (height - square_size) // 2
        bottom_right_x = top_left_x + square_size
        bottom_right_y = top_left_y + square_size

        # Draw detection box
        cv2.rectangle(frame, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (0, 255, 0), 3)
        cv2.putText(frame, "Detection Box", (top_left_x, top_left_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        if hand_detected and current_time >= resume_detection_time:
            if current_time - last_capture_time > capture_interval:
                last_capture_time = current_time
                instructions_label.config(text="Hand detected! Processing...")

                # Predict
                cropped_image = hand_detector.get_cropped_hand(frame, hand_landmarks)
                letter, confidence = model.predict(cropped_image)

                # Save
                file_path = os.path.join(capture_folder, f"{letter}_{int(confidence * 100)}.jpg")
                cv2.imwrite(file_path, cropped_image)

                # Update GUI
                captured_text += letter
                character_label.config(text=f"Character: {letter}")
                confidence_label.config(text=f"Confidence: {confidence * 100:.2f}%")
                sentence_label.config(text=f"Sentence: {captured_text}")

                # Get word predictions using the whole captured_text
                if len(captured_text) >= 2:
                    word_predictions = predict_words(captured_text, fasttext_model, top_n=3)
                    word_prediction_label.config(text=f"Word Predictions: {', '.join(word_predictions)}")

                # Pause detection for 1 second
                resume_detection_time = current_time + 1
        elif not hand_detected:
            instructions_label.config(text="Put your hand inside the detection box")

        # Update video feed
        frame_pil = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=frame_pil)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
        video_label.after(10, update_frame)

    def close_app():
        cap.release()
        root.destroy()

    # Close button
    close_button = Button(
        root, text="Close", command=close_app,
        font=("Helvetica", 14), bg="#d32f2f", fg="#ffffff",
        activebackground="#b71c1c", activeforeground="#ffffff"
    )
    close_button.place(relx=0.9, rely=0.05, anchor="ne")

    # Clear Text button function
    def clear_text():
        nonlocal captured_text
        captured_text = ""
        character_label.config(text="Character: ")
        confidence_label.config(text="Confidence: ")
        sentence_label.config(text="Sentence: ")
        word_prediction_label.config(text="Word Predictions: ")

    # Clear Text button
    clear_text_button = Button(
        root, text="Clear Text", command=clear_text,
        font=("Helvetica", 14), bg="#00796b", fg="#ffffff",
        activebackground="#004d40", activeforeground="#ffffff"
    )
    clear_text_button.place(relx=0.8, rely=0.05, anchor="ne")

    update_frame()
    root.mainloop()
