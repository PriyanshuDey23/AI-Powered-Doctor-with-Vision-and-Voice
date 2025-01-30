
# Setup Text to Speech–TTS–model with gTTS
import os
from gtts import gTTS

def text_to_speech_with_gtts_old(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)

# input_text="Hello this is Priyanshu Dey!"
# text_to_speech_with_gtts_old(input_text=input_text, output_filepath="Testing_Files\\doctor_voice_test.mp3")


# When the audio file will be saved it will be automatically played
# Use Model for Text output to Voice

import subprocess
import platform
import os
from gtts import gTTS
import pygame  # Import pygame for MP3 playback

def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"

    # Generating the speech
    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)  # Saving the audio file

    # Debugging file path
    print(f"Audio file saved to: {os.path.abspath(output_filepath)}")

    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            # Initialize pygame mixer and play the MP3
            pygame.mixer.init()
            pygame.mixer.music.load(output_filepath)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():  # Wait until music finishes
                pygame.time.Clock().tick(10)
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])  # Alternative: use 'mpg123' or 'ffplay'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

# Test the function
# input_text = "Hi this is Priyanshu Dey, autoplay testing!"
# output_filepath = os.path.join("Testing_Files", "auto_doctor_voice_test.mp3")
# text_to_speech_with_gtts(input_text=input_text, output_filepath=output_filepath)


