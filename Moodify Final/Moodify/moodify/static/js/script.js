document.addEventListener('DOMContentLoaded', function () {
    // DOM Elements
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const captureBtn = document.getElementById('capture-btn');
    const toggleCameraBtn = document.getElementById('toggle-camera-btn');
    const generateBtn = document.getElementById('generate-btn');
    const emotionResult = document.getElementById('emotion-result');
    const playlistContainer = document.getElementById('playlist-container');

    // Avatar elements
    const avatar = document.getElementById('moodify-avatar');
    const emoji = document.getElementById('emoji');
    const tip = document.getElementById('avatar-tip');

    // State variables
    let currentEmotion = null;
    let cameraStream = null;
    let isCameraOn = false;

    // Initialize camera
    function initCamera() {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(function (stream) {
                    cameraStream = stream;
                    video.srcObject = stream;
                    video.play();
                    isCameraOn = true;
                    toggleCameraBtn.textContent = 'Stop Camera';
                    console.log('Camera initialized successfully');
                })
                .catch(function (error) {
                    console.error("Camera access error:", error);
                    emotionResult.textContent = "Could not access camera. Please check permissions.";
                });
        } else {
            console.error("Camera API not available");
            emotionResult.textContent = "Camera not supported in this browser.";
        }
    }

    // Toggle camera on/off
    toggleCameraBtn.addEventListener('click', function () {
        if (isCameraOn) {
            video.pause();
            if (cameraStream) {
                cameraStream.getTracks().forEach(track => track.stop());
            }
            toggleCameraBtn.textContent = 'Start Camera';
            isCameraOn = false;
            console.log('Camera stopped');
        } else {
            initCamera();
        }
    });

    // Capture emotion button
    captureBtn.addEventListener('click', function () {
        if (!isCameraOn) {
            emotionResult.textContent = "Please start the camera first.";
            return;
        }

        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        canvas.toBlob(function (blob) {
            const formData = new FormData();
            formData.append('image', blob, 'mood-capture.jpg');

            emotionResult.textContent = "Detecting emotion...";

            fetch('/detect-emotion', {
                method: 'POST',
                body: formData
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.emotion) {
                        currentEmotion = data.emotion;
                        emotionResult.textContent = `You seem ${currentEmotion}`;
                        generateBtn.disabled = false;
                        console.log(`Detected emotion: ${currentEmotion}`);

                        // ✨ Animate Avatar with detected emotion
                        animateAvatar(currentEmotion);
                    } else {
                        emotionResult.textContent = "Couldn't detect emotion clearly. Please try again.";
                        generateBtn.disabled = true;
                    }
                })
                .catch(error => {
                    console.error("Detection error:", error);
                    emotionResult.textContent = "Error detecting emotion. Please try again.";
                    generateBtn.disabled = true;
                });
        }, 'image/jpeg', 0.95);
    });

    // Generate playlist button
    generateBtn.addEventListener('click', function () {
        if (!currentEmotion) {
            alert("Please capture your mood first.");
            return;
        }

        playlistContainer.innerHTML = '<div class="loading">Loading your playlist...</div>';
        generateBtn.disabled = true;

        fetch('/generate-playlist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ emotion: currentEmotion })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Playlist generation failed');
                }
                return response.json();
            })
            .then(data => {
                generateBtn.disabled = false;
                if (data.tracks && data.tracks.length > 0) {
                    displayPlaylist(data.tracks);
                } else {
                    playlistContainer.innerHTML = '<div class="error">No tracks found for this mood. Try again.</div>';
                }
            })
            .catch(error => {
                console.error("Playlist error:", error);
                playlistContainer.innerHTML = '<div class="error">Error generating playlist. Please try again.</div>';
                generateBtn.disabled = false;
            });
    });

    // Display playlist function
    function displayPlaylist(tracks) {
        playlistContainer.innerHTML = '';

        tracks.forEach(track => {
            const trackElement = document.createElement('div');
            trackElement.className = 'track';

            trackElement.innerHTML = `
                <img src="${track.image_url || 'static/images/default-album.png'}" alt="${track.name}">
                <div class="track-info">
                    <h3>${track.name}</h3>
                    <p>${track.artists.join(', ')}</p>
                </div>
                <a href="${track.url}" target="_blank" class="play-button">▶ Play</a>
            `;

            playlistContainer.appendChild(trackElement);
        });
    }

    // ✨ Avatar Animation Function
    function animateAvatar(emotion) {
        if (!avatar || !emoji || !tip) return;

        const moods = {
            happy: { emoji: '😄', tip: "Yay! You're feeling happy!" },
            sad: { emoji: '😢', tip: "I'm here for you 💜" },
            angry: { emoji: '😠', tip: "Deep breaths. Let it go." },
            surprise: { emoji: '😲', tip: "Whoa! That’s surprising!" },
            neutral: { emoji: '😌', tip: "Just vibing..." }
        };

        const effects = {
            happy: 'bounce',
            sad: 'droop',
            angry: 'shake',
            surprise: 'zoom',
            neutral: 'pulse'
        };

        const selected = moods[emotion] || { emoji: '🤖', tip: "Feeling mysterious..." };
        emoji.textContent = selected.emoji;
        tip.textContent = selected.tip;

        avatar.className = 'floating-avatar'; // Reset
        void avatar.offsetWidth; // Force reflow

        avatar.classList.add(effects[emotion] || 'pulse');
        avatar.classList.add(emotion); // For border styling
    }

    // Initialize the app
    initCamera();
});
