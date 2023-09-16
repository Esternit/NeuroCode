# coding=utf-8

import json

import Distance
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import os

def changer(line, tmpl):
    find=False
    for elem in line:
        for section, commands in tmpl.items():
            for all in commands:
                if Distance.distance_between(all,elem)<3:
                    commands.append(all)
                    tmpl.pop(section)
                    tmpl.update({section:commands})
                if find==True:
                    break
            if find == True:
                break
        if find == True:
            break

'''
cycle=["цикл", "цикла"]
variable=["переменную", "переменная" , "переменной"]
value=["значением", "значение"]
strng=["string", "строка", "строку"]
insider=["вложенный", "вложенных"]
repeats=["повторений", "повторение"]
name=["имя","именем"]

file=open("open_templates.json",'w',encoding='utf-8')
to_json={"cycle":cycle,"variable":variable,"value":value, "strng":strng, "insider":insider, "repeats":repeats, "name":name}
json.dump(to_json, file, sort_keys=True, indent=2, ensure_ascii=False)
file.close()'''

file=open("open_templates.json",'r',encoding='utf-8')
file_content=file.read()
templates = json.loads(file_content)
line="Создай парочкеу циклы"
find=False
for section, commands in templates.items():
    if find == True:
        break
    line=line.split()
    for elem in line:
        if find==True:
            break
        if elem!=' ':
            print(process.extract(elem,commands,limit=2))
            x=process.extract(elem,commands,limit=2)[0]
            if x[1]>80:
                templates.pop(section)
                commands.append(elem)
                templates.update({section: commands})
                find=True


file.close()
for section, commands in templates.items():
    print(section)
    print(commands)
file=open("open_templates.json",'w',encoding='utf-8')
json.dump(templates, file, sort_keys=True, indent=2, ensure_ascii=False)
file.close()