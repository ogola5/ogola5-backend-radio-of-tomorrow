# dj_voice.py

import os

# Imports the Google Cloud client library
from google.cloud import texttospeech

# Instantiates a client
client = texttospeech.TextToSpeechClient()

def generate_speech(text, output_filename):
    """Synthesizes speech from the input string of text."""

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(output_filename, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_filename}"')

# Example usage (You can keep this or move it to another file for testing)
if __name__ == "__main__":
    dj_greetings = [
        "Welcome back to Radio of Tomorrow!",
        "Hey there, music lovers! It's time for another sonic journey.",
        "Get ready for an audio experience curated just for you."
    ]

    dj_transitions = [
        "Coming up next, a track you might just love...",
        "And now, for something completely different...",
        "Let's switch gears with this next tune..."
    ]

    # Generate speech for greetings and transitions
    for i, greeting in enumerate(dj_greetings):
        generate_speech(greeting, f"greeting_{i+1}.mp3")

    for i, transition in enumerate(dj_transitions):
        generate_speech(transition, f"transition_{i+1}.mp3")