# Setup Audio Recorder


import logging
import speech_recognition as sr
from gtts import gTTS # Text to audio

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# From Microphon to audio file
def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Simplified function to record audio from the microphone and save it as an MP3 file.

    Args:
    file_path (str): Path to save the recorded audio file.
    timeout (int): Maximum time to wait for a phrase to start (in seconds).
    phrase_time_lfimit (int): Maximum time for the phrase to be recorded (in seconds).
    """
    recognizer = sr.Recognizer() # speech recognition functionality.(Record audio and process and store it)
    
    try:
        with sr.Microphone() as source: # access the microphone
            logging.info("Adjusting for ambient noise...")
            # adjust for ambient noise(Remove Background noise)
            recognizer.adjust_for_ambient_noise(source, duration=1)  # duration:- the amount of time (in seconds) that the recognizer should listen to the ambient noise before adjusting for it.
            logging.info("Start speaking now...") # Now it will record
            
            # Record the audio
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit) # Recognizer will listen to microphone #Other information doc string
            logging.info("Recording complete.")

            # Convert the recorded audio to text
            text = recognizer.recognize_google(audio_data)
            logging.info(f"Recognized text")

            # Use gTTS to convert the recognized text back to speech
            tts = gTTS(text=text)
            tts.save(audio_filepath)
            
            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Save the audio to path
audio_filepath="Testing_Files\\patient_voice_test_for_patient.mp3"
# record_audio(file_path=audio_filepath)



# Setup Speech to text(stt)  for transcription

import os
from groq import Groq


GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
stt_model = "whisper-large-v3-turbo"

client = Groq()

def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    client = Groq(api_key=GROQ_API_KEY)

    with open(audio_filepath, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=(audio_filepath, audio_file.read()),  
            model=stt_model,
            language="en"
        )

    # Return the transcription text
    return transcription.text




      