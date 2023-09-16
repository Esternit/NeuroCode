# coding=utf-8

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json

import Translator


def searcher_for_func(line,lst_of_function_lst):
    max=-1
    mostcommonname=""
    for elem in lst_of_function_lst:
        x=process.extract(line,elem,limit=2)[0]
        if x[1]>max:
            mostcommonname=x[0]
            max=x[1]
    return mostcommonname

def find_most_similar(name,lst):
    x=process.extract(name,lst,limit=2)[0]
    return x[0]
'''
file=open("library_templates.json",'r',encoding='utf-8')
file_content=file.read()
templates = json.loads(file_content)
data=templates["tensorflow.keras.models"]
data1=templates["tensorflow.keras.layers"]
lst=[data,data1]
print(Translator.translator("секвентиал"))
print(searcher(Translator.translator("секвентиал"),lst))'''