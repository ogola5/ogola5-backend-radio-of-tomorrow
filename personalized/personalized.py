import requests
import random
from flask import Blueprint, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Create a blueprint
personalized_bp = Blueprint('personalized', __name__)
CORS(personalized_bp)

# Load environment variables from .env file
load_dotenv()

# API keys
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
OPENCAGE_API_KEY = os.getenv('OPENCAGE_API_KEY')

# Function to get weather data from OpenWeatherMap API
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['weather'][0]['description']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return "Unable to fetch weather data"

# Function to get city details using OpenCage Geocoder API
def get_city_details(city):
    url = f"https://api.opencagedata.com/geocode/v1/json"
    params = {'q': city, 'key': OPENCAGE_API_KEY, 'limit': 1}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data['results']:
            city_info = data['results'][0]
            return {
                'name': city_info['formatted'],
                'country': city_info['components'].get('country', ''),
                'region': city_info['components'].get('state', ''),
                'latitude': city_info['geometry']['lat'],
                'longitude': city_info['geometry']['lng']
            }
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching city details: {e}")
        return None

# Function to curate music based on weather, time of day, and feeling
def curate_music(weather, time_of_day, feeling):
    music_tracks = {
        'clear sky': ['Sunny Side Up', 'Morning Breeze', 'Open Road'],
        'rain': ['Raindrops', 'Stay Inside', 'Puddle Jumping'],
        'cloudy': ['Cloudy Day', 'Gray Skies', 'Calm Winds'],
        'snow': ['Winter Wonderland', 'Frozen', 'Snowy Morning'],
    }
    
    time_based_tracks = {
        'morning': ['Rise and Shine', 'Good Morning Sunshine', 'Early Start'],
        'afternoon': ['Afternoon Vibes', 'Midday Groove', 'Lunch Break'],
        'evening': ['Relaxing Evening', 'Chill Night', 'Sunset Calm'],
        'night': ['Starry Night', 'Night Drive', 'Sleep Tight'],
    }

    feeling_tracks = {
        'happy': ['Joyful Tune', 'Good Vibes Only', 'Happy Dance'],
        'sad': ['Sad Story', 'Melancholy', 'Tears'],
        'energetic': ['Power Up', 'Feel the Beat', 'Rave Time'],
        'chill': ['Relax', 'Calm Waves', 'Easy Listening'],
    }
    
    recommended_music = []
    weather_music = music_tracks.get(weather.lower(), [])
    time_music = time_based_tracks.get(time_of_day, [])
    feeling_music = feeling_tracks.get(feeling, [])
    
    recommended_music.extend(weather_music)
    recommended_music.extend(time_music)
    recommended_music.extend(feeling_music)
    
    random.shuffle(recommended_music)
    
    return recommended_music[:5]

# Function to generate a phrase based on mood and weather
def generate_phrase(feeling, weather):
    phrases = {
        'happy': [
            "Keep smiling, you're doing great!",
            "Happiness is contagious, spread it!",
            "Your positivity is inspiring!",
        ],
        'sad': [
            "Don't worry, this too shall pass.",
            "Sometimes, tears cleanse the soul.",
            "Stay strong, brighter days are ahead.",
        ],
        'energetic': [
            "Keep up the energy, the world needs it!",
            "Push harder, you're unstoppable!",
            "Your energy is infectious, keep it going!",
        ],
        'chill': [
            "Take a deep breath, everything will be fine.",
            "Relax, you've got this.",
            "Chill out and enjoy the little moments.",
        ]
    }

    weather_phrases = {
        'clear sky': "The sun is shining just for you!",
        'rain': "A little rain makes everything grow, just like you.",
        'cloudy': "Even cloudy days have their own charm.",
        'snow': "Snowflakes are like thoughts, each unique and special.",
    }

    mood_phrases = phrases.get(feeling, [])
    weather_phrase = weather_phrases.get(weather, "Stay positive!")

    # Combine the weather and mood phrases
    selected_mood_phrase = random.choice(mood_phrases) if mood_phrases else "You're amazing just the way you are."
    return f"{selected_mood_phrase} {weather_phrase}"

# Function to search for YouTube videos based on a music track name
def search_youtube(video_title):
    youtube_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': video_title,
        'key': YOUTUBE_API_KEY,
        'type': 'video',
        'maxResults': 1
    }
    try:
        response = requests.get(youtube_url, params=params)
        response.raise_for_status()
        data = response.json()

        if 'items' in data and len(data['items']) > 0:
            video_id = data['items'][0]['id']['videoId']
            return f"https://www.youtube.com/watch?v={video_id}"
        else:
            print(f"No YouTube videos found for '{video_title}'")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error searching YouTube for '{video_title}': {str(e)}")
        return None

def init_routes(bp):
    @bp.route('/get-music', methods=['POST'])
    def get_music():
        try:
            data = request.json
            city = data.get('city', 'New York')
            time_of_day = data.get('time_of_day', 'morning')
            feeling = data.get('feeling', 'happy')

            weather = get_weather(city)
            city_info = get_city_details(city)
            music_list = curate_music(weather, time_of_day, feeling)
            phrase = generate_phrase(feeling, weather)

            youtube_links = [search_youtube(track) for track in music_list if search_youtube(track)]

            return jsonify({
                'weather': weather,
                'city_info': city_info,
                'curated_music': music_list,
                'youtube_links': youtube_links,
                'motivational_phrase': phrase
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @bp.route('/feedback', methods=['POST'])
    def feedback():
        try:
            data = request.json
            music_track = data.get('music_track', '')
            reaction = data.get('reaction', '')
            print(f"Feedback for {music_track}: {reaction}")
            return jsonify({'message': 'Feedback received, thank you!'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

init_routes(personalized_bp)