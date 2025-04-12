from dotenv import load_dotenv
load_dotenv()  

from flask import Flask, render_template, request, jsonify
import os
from emotion_detection import detect_emotion
from spotify_integration import generate_playlist
import webbrowser
import threading

app = Flask(__name__)

# Ensure the upload folder exists
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect-emotion', methods=['POST'])
def emotion_detection():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    # Save the image temporarily
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp.jpg')
    image_file.save(image_path)
    
    # Detect emotion
    emotion = detect_emotion(image_path)
    
    # Clean up
    if os.path.exists(image_path):
        os.remove(image_path)
    
    if emotion:
        return jsonify({'emotion': emotion})
    else:
        return jsonify({'error': 'Could not detect emotion'}), 400

@app.route('/generate-playlist', methods=['POST'])
def playlist_generation():
    data = request.get_json()
    emotion = data.get('emotion')
    
    if not emotion:
        return jsonify({'error': 'No emotion provided'}), 400
    
    # Generate playlist based on emotion
    tracks = generate_playlist(emotion)
    
    if tracks:
        return jsonify({'tracks': tracks})
    else:
        return jsonify({'error': 'Could not generate playlist'}), 500

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()
    app.run(debug=True)