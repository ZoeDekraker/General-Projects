""" MSFT Words 'Read Aloud' function in Python. 

This program records your audio and speaks it back to you.
You can also edit the text and export results to .txt file.

"""

import tkinter
import pyaudio
import wave
import whisper
import pyttsx3
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox

frames = []
flag = True



# start recording
def start_recording():
    global stream
    global audio
    global flag
    st = 1
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, 
                        channels=1, 
                        rate=44100, 
                        input=True, 
                        frames_per_buffer=1024)
    while st == 1:
        input = stream.read(1024)
        frames.append(input)
        main.update()
        flag = False

# end recording
def stop_recording():
    if flag == True:
        messagebox.showinfo(title= "Error", message= "You need to start recording before you can stop recording.")
    else:
        stream.stop_stream()
        stream.close()
        audio.terminate()
        audio_to_file(audio)

# write audio to file
def audio_to_file(audio):
    recording = True
    file_name = "sound_smart.wav"
    audio_file = wave.open(file_name, "wb")
    audio_file.setnchannels(1)
    audio_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    audio_file.setframerate(44100)
    audio_file.writeframes(b''.join(frames))
    audio_file.close()
    voice_to_text(file_name)

# translate voice to text
def voice_to_text(file_name):
    global text_result
    model = whisper.load_model("base")
    result = model.transcribe(file_name)
    text_result = result["text"]
    insert_text(text_result)

# display text in text box
def insert_text(text_result):
    text_area.insert('1.0', text_result)
    text_to_voice()

# translate text to audio and play result.
def text_to_voice():
    update_text = text_area.get('1.0', 'end')
    if len(update_text) > 1: # check if empty
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
        engine.say(update_text)
        engine.runAndWait()
    else:
        messagebox.showinfo(title= "Erorr", message= "There is no text to speak of")

# write text to file
def export_to_file():
    area = text_area.get('1.0', 'end')
    if len(area) > 1:
        export_name = filedialog.asksaveasfilename(
        initialdir="C:/Users/MainFrame/Desktop/", 
        title="Save Results To", 
        filetypes=(("Text Document", "*.txt"),))
        with open(export_name, "w") as f:
            f.write(area)
        messagebox.showinfo(title= "Export", message= "Your file has been saved.")
    else:
        messagebox.showinfo(title= "Error", message= "There is no text to save")

# close program
def exit_editor():
    if tkinter.messagebox.askokcancel("Quit?", "Really quit?"):
        root.destroy()

# clear text function
def clear_text():
    text_area.delete(1.0, END)





#<-------------------GUI--------------------->#


root = Tk()
root.title('Read Aloud')
root.resizable(FALSE, FALSE)
main = ttk.Frame(root)

main.grid(column=0, row=0, sticky=(N, W, E, S), padx=20)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

start_record_btn = ttk.Button(main, text='Start recording', padding=15, command=start_recording)
start_record_btn.grid(column=0, row=0, padx=30, pady=30)

sep1 = ttk.Separator(main, orient=VERTICAL)
sep1.grid(column=1, row=0, pady=10, sticky=NSEW )

stop_record_btn = ttk.Button(main, text='Stop recording', padding=15, command=stop_recording)
stop_record_btn.grid(column=2, row=0, padx=30, pady=30)

sep2 = ttk.Separator(main, orient=VERTICAL)
sep2.grid(column=3, row=0, pady=10, sticky=NSEW )

read_btn = ttk.Button(main, text='Read Aloud', padding =15, command=text_to_voice)
read_btn.grid(column=4, row=0, padx=30, pady=30)

sep3 = ttk.Separator(main, orient=VERTICAL)
sep3.grid(column=5, row=0, pady=10, sticky=NSEW )

export_btn = ttk.Button(main, text='Export txt', padding=15, command=export_to_file)
export_btn.grid(column=6, row=0, padx=30, pady=30)

sep4 = ttk.Separator(main, orient=VERTICAL)
sep4.grid(column=7, row=0, pady=10, sticky=NSEW )

clear_btn = ttk.Button(main, text='Clear All', padding=15, command=clear_text)
clear_btn.grid(column=8, row=0, padx=30, pady=30)

text_area = Text(main, wrap="word")
text_area.grid(column=0, row=1, columnspan=9, rowspan=2, pady=20)

scrollbary = ttk.Scrollbar(main, orient=VERTICAL, command= text_area.yview)
scrollbary.grid(column= 8, row = 1, rowspan=2, sticky= (N, S))
text_area.configure(yscrollcommand= scrollbary.set)

quit_btn = ttk.Button(main, text="Quit", padding=10, command=exit_editor)
quit_btn.grid(column=8, row=3, padx=10, pady=20)




root.mainloop()
