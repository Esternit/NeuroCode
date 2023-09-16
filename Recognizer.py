# coding=utf-8
import time

import speech_recognition as sr



listener = sr.Recognizer()
while True:
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source, phrase_time_limit=4)
            command = listener.recognize_google(voice, language="ru-RU")
            print(command)
    except:
        pass