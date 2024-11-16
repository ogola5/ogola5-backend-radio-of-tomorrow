
import requests
import random
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Your YouTube API Key
YOUTUBE_API_KEY = 'AIzaSyBhMwQPvUaMS6TX8H4pmj5h47gFtqBf0wc'

# OpenWeatherMap API Key
WEATHER_API_KEY = '8cdcbdf16a18b6390bbc5b12748bd047'

# OpenCage Geocoder API Key
OPENCAGE_API_KEY = 'ea80bb199bf54ff29c7c231952675be9'

# Function to get weather data from OpenWeatherMap API
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        weather_description = data['weather'][0]['description']
        return weather_description
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {str(e)}")
        return "Unable to fetch weather data"

# Function to get city information using OpenCage Geocoder API
def get_city_details(city):
    url = f"https://api.opencagedata.com/geocode/v1/json"
    params = {
        'q': city,
        'key': OPENCAGE_API_KEY,
        'limit': 1
    }
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
        else:
            print(f"No city details found for '{city}'")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error during request for city details: {str(e)}")
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

@app.route('/get-music', methods=['POST'])
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

        youtube_links = []
        for track in music_list:
            link = search_youtube(track)
            if link:
                youtube_links.append(link)

        return jsonify({
            'weather': weather,
            'city_info': city_info,
            'curated_music': music_list,
            'youtube_links': youtube_links,
            'motivational_phrase': phrase
        })
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        data = request.json
        music_track = data.get('music_track', '')
        reaction = data.get('reaction', '')

        print(f"Feedback for {music_track}: {reaction}")
        return jsonify({'message': 'Feedback received, thank you!'})
    except Exception as e:
        print(f"Error processing feedback: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
