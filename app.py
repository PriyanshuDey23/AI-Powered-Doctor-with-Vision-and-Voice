# Api
from dotenv import load_dotenv
load_dotenv()
import os

GROQ_API_KEY=os.getenv("GROQ_API_KEY")

# VoiceBot UI with Gradio
import os
import gradio as gr

from Workflow.brain_of_doctor import encode_image,analyze_image_with_query
from Workflow.voice_of_patient import record_audio,transcribe_with_groq
from Workflow.voice_of_doctor import text_to_speech_with_gtts



system_prompt="""You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""



# Joining all the different components and give us a proper output
def process_inputs(audio_filepath, image_filepath):
    # Speech to text
    speech_to_text_output = transcribe_with_groq(GROQ_API_KEY=GROQ_API_KEY, 
                                                 audio_filepath=audio_filepath,
                                                 stt_model="whisper-large-v3-turbo")

    # Handle the image input
    if image_filepath:
        doctor_response = analyze_image_with_query(query=system_prompt+speech_to_text_output, encoded_image=encode_image(image_filepath), model="llama-3.2-90b-vision-preview")
    else:
        doctor_response = "No image provided for me to analyze"

    voice_of_doctor = text_to_speech_with_gtts(input_text=doctor_response, output_filepath="final.mp3") 

    return speech_to_text_output, doctor_response, voice_of_doctor


# Create the interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"), # access to microphone (allow to browser)
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio("Temp.mp3")
    ],
    title="AI Doctor with Vision and Voice"
)

iface.launch(debug=True)


# http://127.0.0.1:7860/