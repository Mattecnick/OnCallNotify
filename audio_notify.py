import sounddevice as sd
import soundfile as sf
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import queue
import threading
from plyer import notification

# Nome da riconoscere
nome = "matteo"
time_rec = 4
time_update = 3
filename_from_mic = "Recording.WAV"
ringtone = "bharath-you-have-a-call.wav"
r = sr.Recognizer()
audio_queue = queue.Queue()

# Funzione per inviare la notifica
def invia_notifica():
    notification.notify(
        title="Notifica Importante",
        message=f"Hanno pronunciato il tuo nome: {nome}",
        timeout=10
    )
    data, samplerate = sf.read(ringtone)
    sd.play(data, samplerate)


# Funzione per catturare l'audio in tempo reale e salvarlo su file
def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(indata.copy())

def recognize_and_notify():
    SAMPLE_RATE = 44100
    buffer_audio = np.zeros((0,), dtype=np.int32)
    
    while True:
        audio_data = audio_queue.get()
        audio_data = np.frombuffer(audio_data, dtype=np.int32)
        buffer_audio = np.concatenate((buffer_audio, audio_data))
        
        if len(buffer_audio) >= SAMPLE_RATE * time_rec:  # 20 seconds of audio
            wav.write(filename_from_mic, SAMPLE_RATE, buffer_audio)
            #print("File written, starting recognition.")
            # Recognize the audio from file
            
            threading.Thread(target=recognize_from_file).start()
                
            # Keep the last 10 seconds of audio in the buffer
            buffer_audio = buffer_audio[-SAMPLE_RATE*(time_rec-time_update):]

def recognize_from_file():
    with sr.AudioFile(filename_from_mic) as source:
        audio_data = r.record(source)
        try:
            text = r.recognize_google(audio_data, language="it-IT")
            print(f"*** {text}")
            if nome.lower() in text.lower():
                print("\n\n\n\n\n\nTHAT'S YOU!\n\n\n\n\n")
                invia_notifica()
        except sr.UnknownValueError:
            print("Non ho capito l'audio")
        except sr.RequestError as e:
            print(f"Errore nel servizio di riconoscimento vocale; {e}")

def ascolta_audio():
    SAMPLE_RATE = 44100
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=SAMPLE_RATE, dtype='int32'):
        print("Ascoltando in tempo reale...")
        processing_thread = threading.Thread(target=recognize_and_notify)
        processing_thread.daemon = True
        processing_thread.start()

        while True:
            sd.sleep(10000)  # Mantiene lo stream attivo

if __name__ == "__main__":
    invia_notifica()
    #ascolta_audio()
