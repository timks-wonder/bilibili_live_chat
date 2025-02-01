from gtts import gTTS
from playsound import playsound


class Speaker:
    def __init__(self):
        self.voice = gTTS
        self.tts = None
        self.mp3 = r'D:\pythonProject\output.mp3'

    def speak(self, text):
        self.tts = self.voice(text=text, lang='zh-cn')
        self.tts.save(self.mp3)
        playsound(self.mp3)
