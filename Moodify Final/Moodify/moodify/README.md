# 🎵 Moodify – Emotion-Based Music Recommendation System

**Moodify** is an innovative web application that recommends and plays music based on the user's **facial expression**. It combines facial emotion detection with music streaming via the **Spotify API** to enhance the user's experience through personalized mood-based playlists.

---

## 💡 Project Idea

Traditional music players require users to search and play music manually. Moodify proposes a smart solution — by analyzing the user's facial emotion through a webcam image, the system automatically plays a playlist that matches the detected mood using **Machine Learning** and **Spotify integration**.

---

## ⚙️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (via Flask templates)
- **Backend**: Flask (Python)
- **Machine Learning**: TensorFlow, Keras
- **Computer Vision**: OpenCV
- **Spotify Integration**: Spotipy (Python wrapper for the Spotify Web API)
- **Environment Management**: Python-Dotenv
- **Model File**: Pre-trained emotion detection model (`model.h5`) and Haar Cascade (`haarcascade_frontalface_default.xml`)

---

## 🧠 Core Features

- 🎭 Detects emotions from user's uploaded facial image (angry, happy, sad, neutral, etc.)
- 🎶 Automatically generates and plays a personalized Spotify playlist based on the detected emotion
- 📸 Real-time or static image-based emotion capture using OpenCV
- 🧠 Uses a trained CNN model to classify emotions from facial images

---

## 📁 Project Structure

Moodify Final/
└── Moodify/
    └── moodify/
        ├── app.py
        ├── emotion_detection.py
        └── model/
            ├── model.h5
            └── haarcascade_frontalface_default.xml