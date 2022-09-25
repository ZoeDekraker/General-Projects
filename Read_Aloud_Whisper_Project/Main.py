""" MSFT Words 'Read Aloud' function in Python. 

This program records your audio and speaks it back to you.
Added option of writing the results to a txt file.
Check if what you say makes sense before you send it.

"""

import pyaudio
import wave
import whisper
import pyttsx3

frames = []

# capture audio from microphone
def capture_audio():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    print("Start talking now.")
    print("To end the audio recording enter ctrl + c in the terminal")
    try: 
        while True:
            input = stream.read(1024)
            frames.append(input)
    except KeyboardInterrupt:
        pass
    stream.stop_stream()
    stream.close()
    audio.terminate()
    audio_to_file(audio)

# write audio to file
def audio_to_file(audio):
    file_name = "sound_smart.wav"
    audio_file = wave.open(file_name, "wb")
    audio_file.setnchannels(1)
    audio_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    audio_file.setframerate(44100)
    audio_file.writeframes(b''.join(frames))
    audio_file.close()
    voice_to_text(file_name)

# translate audio to text
def voice_to_text(file_name):
    model = whisper.load_model("base")
    result = model.transcribe(file_name)
    text_result = result["text"]
    print(text_result)
    text_to_voice(text_result)

# translate text to audio and play result.
def text_to_voice(text_result):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text_result)
    engine.runAndWait()
    repeat_audio(text_result)
    
# repeat the audio 
def repeat_audio(text_result):
    relisten_choice = input("Would you like to listen again? y/n")
    if relisten_choice == 'y':
        text_to_voice(text_result)
    else:
        voice_to_file(text_result)
    
# option to write the result to txt file
def voice_to_file(text_result):
    user_input = input("Would you like to export your dictation to a txt file? y/n ")
    if user_input == 'y':
        with open("voice_to_text_results.txt", "w") as f:
            f.write(text_result)
        print("File created: voice_to_text_results.txt")
    else:
        print("Thank you for playing")
   

capture_audio()
