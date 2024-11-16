import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API Setup
client_id = 'fbb92e3854ed4ba29a14c463527043b3'
client_secret = '22d68a75ed7147edbcb68126cf5ee08f'

# client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# # Fetch Music Data
# track_ids = ['6rqhFgbbKwnb9MLmUQDhG6', '1r9xUipOqoNwggBpENDsvJ', '5CQ30WqJwcep0pYcV4AMNc']
# audio_features = sp.audio_features(track_ids)

# # Hardcode User Preferences
# user_preferences = {
#     'preferred_genres': ['rock', 'pop'],
#     'desired_mood': 'energetic',
#     'preferred_tempo': 120  # BPM
# }

# # Implement Matching Algorithm
# def match_preferences(audio_features, user_preferences):
#     matched_tracks = []
#     for features in audio_features:
#         if features is not None:
#             # Adjust the thresholds as needed
#             if features['energy'] > 0.3 and features['tempo'] > 100:
#                 matched_tracks.append(features)
#     return matched_tracks

# matched_tracks = match_preferences(audio_features, user_preferences)

# # Create Playlist
# playlist = []

# for track in matched_tracks:
#     track_info = sp.track(track['id'])
#     playlist.append({
#         'name': track_info['name'],
#         'artist': track_info['artists'][0]['name'],
#         'album': track_info['album']['name'],
#         'duration_ms': track_info['duration_ms']
#     })

# # Print the playlist
# print("Playlist:", playlist)
# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials

# # 1. Spotify API Setup (Replace with your credentials)
# client_id = 'YOUR_SPOTIFY_CLIENT_ID'
# client_secret = 'YOUR_SPOTIFY_CLIENT_SECRET'

# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials

# # 1. Spotify API Setup (Replace with your credentials)
# client_id = 'YOUR_SPOTIFY_CLIENT_ID'
# client_secret = 'YOUR_SPOTIFY_CLIENT_SECRET'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# 2. Fetch Music Data
track_ids = ['6rqhFgbbKwnb9MLmUQDhG6', '1r9xUipOqoNwggBpENDsvJ', '5CQ30WqJwcep0pYcV4AMNc'] 
audio_features = sp.audio_features(track_ids)
print("Audio Features:", audio_features)  # Debug print

# 3. Hardcode User Preferences
user_preferences = {
    'preferred_genres': ['rock', 'pop'],
    'desired_mood': 'energetic',
    'preferred_tempo': 100  # BPM (adjusted)
}

# 4. Implement Matching Algorithm (Using Valence and Danceability)
def match_preferences(audio_features, user_preferences):
    matched_tracks = []
    for features in audio_features:
        if features is not None and features['valence'] >= 0.7 and features['danceability'] >= 0.6:  # New logic
            matched_tracks.append(features)
    return matched_tracks

matched_tracks = match_preferences(audio_features, user_preferences)
print("Matched Tracks:", matched_tracks)  # Debug print

# 5. Create Playlist
playlist = []
for track in matched_tracks:
    track_info = sp.track(track['id'])
    playlist.append({
        'name': track_info['name'],
        'artist': track_info['artists'][0]['name'],
        # ... other relevant information
    })

# Print the playlist
print("Playlist:", playlist)