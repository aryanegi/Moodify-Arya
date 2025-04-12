import os
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def generate_playlist(emotion, limit=10):
    try:
        logger.debug(f"Generating playlist for emotion: {emotion}")
        
        # Verify credentials are loaded
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        
        if not client_id or not client_secret:
            logger.error("Spotify credentials not found in .env file!")
            return None

        logger.debug("Initializing Spotify client...")
        sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        ))

        # Mood mapping with more specific queries
        MOOD_MAPPING = {
            'happy': ['mood:happy', 'genre:pop', 'genre:dance'],
            'sad': ['mood:sad', 'genre:blues', 'genre:acoustic'],
            'angry': ['mood:aggressive', 'genre:rock', 'genre:metal'],
            'neutral': ['mood:calm', 'genre:chill', 'genre:indie'],
            'surprise': ['mood:energetic', 'genre:edm', 'genre:electronic'],
            'fear': ['mood:dark', 'genre:ambient', 'genre:soundtrack'],
            'disgust': ['mood:melancholic', 'genre:alternative']
        }

        query = random.choice(MOOD_MAPPING.get(emotion, ['genre:pop']))
        logger.debug(f"Searching Spotify with query: {query}")

        results = sp.search(q=query, type='track', limit=limit)
        tracks = []

        for item in results['tracks']['items']:
            track = {
                'name': item['name'],
                'artists': [artist['name'] for artist in item['artists']],
                'url': item['external_urls']['spotify'],
                'image_url': item['album']['images'][0]['url'] if item['album']['images'] else ''
            }
            tracks.append(track)
        logger.debug(f"Loaded Client ID: {os.getenv('SPOTIFY_CLIENT_ID')}")

        logger.debug(f"Found {len(tracks)} tracks")
        return tracks

    except Exception as e:
        logger.error(f"Spotify API Error: {str(e)}")
        return None