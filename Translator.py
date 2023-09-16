# coding=utf-8


from googletrans import Translator
import json
def translator(name):
    translator = Translator(service_urls=['translate.googleapis.com'])
    trans=translator.translate(name, dest='en')
    return trans.text