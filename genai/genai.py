from flask import jsonify, request, send_file, Blueprint
import google.generativeai as genai
from google.cloud import texttospeech
import os
import re
from dotenv import load_dotenv

# Create a blueprint
genai_bp = Blueprint('genai', __name__)

# Load environment variables from .env file
load_dotenv()

# Configure API Keys
GENAI_API_KEY = os.getenv('GENAI_API_KEY')
genai.configure(api_key=GENAI_API_KEY)

# Initialize Google TTS Client
tts_client = texttospeech.TextToSpeechClient()

# Folder to store audio files
AUDIO_FOLDER = 'generated_audio'
os.makedirs(AUDIO_FOLDER, exist_ok=True)  # Create folder if it doesn't exist

def generate_text_discussion(topic):
    """Generate text discussion on a topic using Gemini."""
    model = genai.GenerativeModel("gemini-1.5-pro")  # Use appropriate Gemini model
    response = model.generate_content(topic)
    return response.text

def clean_text(text):
    """Remove unwanted characters like newlines, extra spaces, etc."""
    cleaned_text = re.sub(r'[\n\t]+', ' ', text)  # Replace newlines and tabs with a space
    cleaned_text = cleaned_text.strip()  # Remove leading/trailing spaces
    return cleaned_text

def convert_text_to_speech(text, filename):
    """Convert text to speech and save it as an audio file."""
    # Clean the text to remove unnecessary characters before generating speech
    cleaned_text = clean_text(text)
    
    # Convert cleaned text to speech
    synthesis_input = texttospeech.SynthesisInput(text=cleaned_text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    # Perform the text-to-speech request
    tts_response = tts_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Write the response to an audio file
    with open(filename, "wb") as out:
        out.write(tts_response.audio_content)
    return filename

def init_routes(bp):
    @bp.route('/genai-endpoint', methods=['GET', 'POST'])
    def genai_route():
        return {"message": "This is the GenAI module"}

    @bp.route('/generate-discussion', methods=['POST'])
    def generate_discussion():
        data = request.get_json()
        topic = data.get("topic")  # Get the topic dynamically from the frontend

        if not topic:
            return jsonify({"error": "Topic is required"}), 400

        # Step 1: Generate the discussion text
        discussion_text = generate_text_discussion(topic)

        # Step 2: Generate a unique filename for each audio
        audio_file_name = os.path.join(AUDIO_FOLDER, f"discussion_{len(os.listdir(AUDIO_FOLDER)) + 1}.mp3")

        # Step 3: Convert generated text to audio
        audio_file = convert_text_to_speech(discussion_text, audio_file_name)

        # Respond with both text and audio file path
        return jsonify({
            "text": discussion_text,
            "audio_file": audio_file
        })

    @bp.route('/get-audio/<int:audio_id>', methods=['GET'])
    def get_audio(audio_id):
        """Endpoint to download a specific generated audio file based on ID."""
        audio_file = os.path.join(AUDIO_FOLDER, f"discussion_{audio_id}.mp3")

        if os.path.exists(audio_file):
            return send_file(audio_file, as_attachment=True)
        else:
            return jsonify({"error": "Audio file not found."}), 404

init_routes(genai_bp)
