import cv2
import numpy as np
from keras.models import load_model
import os

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MODEL_PATH = os.path.join(BASE_DIR, "model", "model.h5")
# CASCADE_PATH = os.path.join(BASE_DIR, "model", "haarcascade_frontalface_default.xml")

# # Load model and Haar cascade
# model = load_model(MODEL_PATH)
# face_cascade = cv2.CascadeClassifier("moodify\model\haarcascade_frontalface_default.xml")
# EMOTIONS = ["angry", "disgust", "fear", "happy", "neutral", "sad", "surprise"]

model = load_model("Moodify\moodify\model\model.h5")
face_cascade = cv2.CascadeClassifier("Moodify\moodify\model\haarcascade_frontalface_default.xml")
EMOTIONS = ["angry", "disgust", "fear", "happy", "neutral", "sad", "surprise"]

def detect_emotion(image_path):
    try:
        # Read image
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        if len(faces) == 0:
            print("No face detected!")
            return None
        
        # Crop and preprocess face
        (x, y, w, h) = faces[0]
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (48, 48))
        face = face.astype("float32") / 255.0
        face = np.expand_dims(face, -1)  # Shape: (48, 48, 1)
        face = np.expand_dims(face, 0)   # Shape: (1, 48, 48, 1)
        
        # Predict and debug
        predictions = model.predict(face)[0]
        print("Raw predictions:", dict(zip(EMOTIONS, predictions)))
        
        # Return emotion with highest score
        return EMOTIONS[np.argmax(predictions)]
    
    except Exception as e:
        print(f"Error: {e}")
        return None