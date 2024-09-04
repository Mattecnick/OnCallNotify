# OnCallNotify
utility that produce transcript of a call and notify you when your name is called. useful to NOT follow up a call while the others think you are on it.

# Setup
The system must be configured as follows:
0) have a PC with internal speakers and mic (any laptop) and headphones
1) select PC microphone as default and PC speakers as default
2) from the call application, select headphones as output device
3) leave the heaphones on the PC mic

# Prerequisites
pip install sounddevice soundfile numpy scipy SpeechRecognition plyer

# convert ringtones
ffmpeg -i bharath-you-have-a-call.mp3 bharath-you-have-a-call.wav

# Collaborative developement
Feel free to use and commit updates!
