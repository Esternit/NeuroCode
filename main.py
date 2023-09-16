# coding=utf-8

from jinja2 import Template
from turtle import left
import speech_recognition as sr
import importlib
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import numpy
import pyautogui
from jinja2 import Template
import json
import time
import Translator
import SameSearcher




def compare(list_1, list_2):
    for elem in list_1:
        if elem in list_2:
            return list_1.index(elem)
    return -1
def do_smth(num,line):

    filename="test.py"
    cyclecounter = numerate_cycle(filename)
    getimports=get_imports(filename)
    #num = int(input('0-Создать 1-Изменить 2-Удалить: '))
    list_names_for_cycles = ['i', 'k', 'o', 'l', 'm', 'n', 'd', 'f', 'j', 't']
    #line = input('Введите что нужно сделать: ')
    line = line.split()
    file_json=open("open_templates.json",'r',encoding='utf-8')
    file_content = file_json.read()
    file_json.close()
    templates = json.loads(file_content)
    amountofspaces=get_current_pos()
    num_line=get_line_to_work_on()
    func_tmpl=get_tmpl_func()
    variable = compare(line, templates.get("variable"))
    val = compare(line, templates.get("value"))
    check_str = compare(line, templates.get("strng"))
    cycle = compare(line, templates.get("cycle"))
    rep = compare(line, templates.get("repeats"))
    insider = compare(line, templates.get("insider"))
    name_for_variable=compare(line,templates.get("name"))
    method_usage=compare(line,templates.get("method"))
    if num == 0:
        countline=1
        #fileinfo = open("fileinfo.txt", 'a')
        file = open(filename, 'r', encoding="utf-8")
        all_lines = file.readlines()
        file.close()
        if variable!=-1 and val!=-1:
            file = open(filename, 'w', encoding="utf-8")
            value = line[val + 1]
            name = Translator.translator(line[variable + 1]).lower()
            if check_str!=-1:
                tm = Template(" " * amountofspaces + "{{name}} = '{{value}}' \n\n")
                msg = tm.render(value=value, name=name)

            else:
                if method_usage!=-1:
                    name_variable = search_for_var(line[method_usage + 1])
                    name_function = get_funct_or_class_name(line[method_usage + 2])
                    tm = Template("{{name_of_var}} = {{name}}.{{func}}()   \n\n")
                    msg = tm.render(name_of_var= name,name=name_variable, func=name_function)
                else:
                    if not value.isdigit():
                        value=get_funct_or_class_name(value)
                        tm = Template(" " * amountofspaces + "{{name}} = {{value}}() \n\n")
                    else:
                        tm = Template(" " * amountofspaces + "{{name}} = {{value}} \n\n")
                    msg = tm.render(value=value, name=name)
            for elem in all_lines:
                if countline==num_line:

                    file.write(msg)

                file.write(elem)
                countline+=1
            file.close()
            #file_info_updater(filename)
            pyautogui.hotkey('ctrl', 'alt','y')
            pyautogui.hotkey('ctrl', 'alt', 'y')
            pyautogui.hotkey('ctrl', 'alt', 'y')
            move_file(filename,num_line)
        elif cycle!=-1 and rep!=-1:
            file = open(filename, 'w', encoding="utf-8")
            if insider!=-1:
                msg=""
                l=0
                for i in range(int(line[insider - 1])):
                    cyclecounter += 1
                    repeats = line[insider - int(line[insider - 1]) + i]
                    tm = Template(
                        " " * amountofspaces + "for {{name_cycle_counter}} in range({{value}}): " + " " * 7 + '# ' + str(
                            cyclecounter) + ' цикл' + '\n\n\n')
                    msg = tm.render(value=repeats, name_cycle_counter=list_names_for_cycles[i])
                    amountofspaces += 4
                    l=i
                in_cycle_changer(l)

            else:

                cyclecounter += 1
                repeats = line[rep - 1]
                tm = Template(
                    " " * amountofspaces + "for {{name_cycle_counter}} in range({{value}}): " + " " * 7 + '# ' + str(
                        cyclecounter) + ' цикл' + '\n\n\n')
                msg = tm.render(value=repeats, name_cycle_counter=list_names_for_cycles[0])
                amountofspaces += 4
                in_cycle_changer(1)
            for elem in all_lines:
                if countline==num_line:

                    file.write(msg)

                file.write(elem)
                countline+=1
        file.close()
        #fileinfo.close()
        pyautogui.hotkey('ctrl', 'alt', 'y')
        move_file(filename, num_line)
    if num == 1:
        countline=0
        if variable!=-1:
            if name_for_variable!=-1:
                file = open(filename, 'r')
                name = Translator.translator(line[line.index("на") - 1]).lower()
                new_name = Translator.translator(line[line.index("на") + 1]).lower()
                lines = file.readlines()
                file.close()
                f=False
                file = open(filename, 'w')
                for elem in lines:
                    if name not in elem and name + '=' not in elem:
                        file.write(elem)
                    else:
                       file.write(elem.replace(name, new_name))
                       f=True
                    if f==False:
                        countline+=1
                file.close()
            elif val!=-1:
                file = open(filename, 'r')
                name = Translator.translator(line[variable + 1]).lower()
                new_value = line[line.index("на") + 1]
                lines = file.readlines()
                file.close()
                f=False
                file = open(filename, 'w')
                for elem in lines:
                    if name not in elem and name + '=' not in elem:
                        file.write(elem)
                    else:
                        if check_str!=-1:
                            tm = Template(count_first_spaces(elem) * " " + "{{name}} = '{{new_value}}' \n\n")
                            msg = tm.render(name=name, new_value=new_value)
                            file.write(msg)
                        else:
                            tm = Template(count_first_spaces(elem) * " " + "{{name}} = {{new_value}} \n\n")
                            msg = tm.render(name=name, new_value=new_value)
                            file.write(msg)
                        f=True
                    if f==False:
                        countline+=1
                file.close()
            pyautogui.hotkey('ctrl', 'alt', 'y')
            pyautogui.hotkey('ctrl', 'alt', 'y')
            move_file(filename,countline)
    if num == 2:
        file = open(filename, 'r', encoding="utf-8")
        countline=0
        if variable!=-1:
            name = Translator.translator(line[variable + 1]).lower()
            lines = file.readlines()
            file.close()
            file = open(filename, 'w', encoding="utf-8")
            f=False
            for elem in lines:
                if name not in elem:
                    file.write(elem)
                    f=True
                if f==False:
                    countline+=1
        if cycle!=-1:
            name = line[cycle + 1]
            lines = file.readlines()
            file.close()
            file = open("test.py", 'w', encoding="utf-8")
            countspaces = 0
            find = False
            for elem in lines:
                if find == True and count_first_spaces(elem) <= countspaces:
                    file.write(elem)
                if "# " + name + " цикл" not in elem and find == False:
                    file.write(elem)
                else:
                    countspaces = count_first_spaces(elem)

                    find = True
                if find==False:
                    countline+=1
        pyautogui.hotkey('ctrl', 'alt','y')
        pyautogui.hotkey('ctrl', 'alt', 'y')

        file.close()
        move_file(filename,countline)
    if num==3:
        countline = 1
        file = open(filename, 'r', encoding="utf-8")
        all_lines = file.readlines()
        file.close()
        msg=""
        file = open(filename, 'w', encoding="utf-8")
        if method_usage!=-1:
            name_variable=search_for_var(line[method_usage+1])
            name_function=get_funct_or_class_name(line[method_usage+2])
            tm = Template("{{name}}.{{func}}()   \n\n")
            msg = tm.render(name=name_variable, func=name_function)
            file.write(msg)
        pyautogui.hotkey('ctrl', 'alt', 'y')
        pyautogui.hotkey('ctrl', 'alt', 'y')
        pyautogui.hotkey('ctrl', 'alt', 'y')
        for elem in all_lines:
            if countline == num_line:
                file.write(msg)

            file.write(elem)
            countline += 1
        file.close()
        write_tmpl_for_func(msg)

    if num==4:
        if check_str!=-1:
            name_line=line[check_str+1]
            pyautogui.hotkey('ctrl', 'alt', 'y')
            pyautogui.hotkey('ctrl', 'alt', 'y')
            move_file(filename,name_line)
            in_cycle_changer(0)
def write_tmpl_for_func(line):
    file = open("tmpl_func.txt", 'w', encoding="utf-8")
    if len(line>2):

        file.write(line[0:line.index(")")]+":"+')')
    else:
        file.write("None")
    file.close()
def get_tmpl_func():
    file = open("tmpl_func.txt", 'r', encoding="utf-8")
    line=file.readline()
    file.close()
    if line!="None":
        return line.split(':')
    else:
        return []
def in_cycle_changer(num):
    file = open("in_cycle.txt", 'w', encoding="utf-8")
    file.write(str(num))
    file.close()

def get_current_pos():
    file=open("file_pos.txt",'r',encoding="utf-8")
    line=file.readline()
    file.close()
    return int(line)


def get_line_to_work_on():
    if get_current_pos()==-1:
        return get_current_pos()
    file=open("project.dic",'r', encoding="utf-8")
    line=file.read()
    file.close()
    return int(line)
def move_file(filename, num_line):
    if num_line==0:
        file=open(filename,'r',encoding="utf-8")
        countlines=0
        for line in file:
            countlines+=1
        file.close()
    else:
        countlines=num_line
    file=open("project.dic",'w', encoding="utf-8")
    file.write(str(countlines))
    file.close()
def count_first_spaces(line):
    count=0
    for i in range(len(line)):
        if line[i]!=" ":
            break
        else:
            count+=1
    return count
def search_for_var(name):
    file_info=open("fileinfo.txt",'r',encoding="utf-8")
    lines=file_info.readlines()
    file_info.close()
    lst=['variable_not_found']
    for elem in lines:
        if ';' in elem:
            lst=elem.split(';')
    return SameSearcher.find_most_similar(name,lst)
def get_funct_or_class_name(name):
    new_name=Translator.translator(name)
    file_info=open("fileinfo.txt",'r',encoding="utf-8")
    lines=file_info.readlines()
    file_info.close()
    lst=[]
    for elem in lines:
        if ':' in elem:
            lst=elem.split(':')
    file = open("library_templates.json", 'r', encoding='utf-8')
    file_content = file.read()
    file.close()
    templates = json.loads(file_content)
    lst_of_data=[]
    for elem in lst:
        if elem != '':
            lst_of_data.append(templates[elem])
    return SameSearcher.searcher_for_func(new_name,lst_of_data)



def file_info_updater(filename):
    countcycle=0
    countfunc=0
    file = open(filename, 'r')
    fileinfo = open("fileinfo.txt", 'w')
    lines = file.readlines()
    line_of_imports=""
    for elem in lines:
        if "from " in elem or "import " in elem:
            elem=elem.split()
            print(elem)
            line_of_imports=line_of_imports+elem[1]+":"

        elif '=' in elem and "#" not in elem:
            if elem[elem.index("=")-1]==' ':
                fileinfo.write(elem[0:elem.index('=')-1]+';')
            else:
                fileinfo.write(elem[0:elem.index('=')] + ';')
        elif "for" in elem and "range" in elem:
            countcycle+=1
        elif "(" in elem and ")" in elem and "for" not in elem and "range" not in elem:
            countfunc+=1
    file.close()
    fileinfo.write('\n')
    fileinfo.write("cycle:"+str(countcycle)+'\n')
    fileinfo.write("func:"+str(countfunc)+'\n')
    fileinfo.write(line_of_imports)
    fileinfo.close()
def get_imports(file):
    file_info_updater(file)
    file=open("fileinfo.txt", 'r')
    lines = file.readlines()
    file.close()
    for elem in lines:
        if ":" in elem:
            return elem.split(':')
    return []
def numerate_cycle(file):
    file_info_updater(file)
    file=open("fileinfo.txt", 'r')
    lines = file.readlines()
    file.close()
    for elem in lines:
        if "cycle" in elem:
            return int(elem.split(":")[1])
    return 0

listener = sr.Recognizer()
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)
model = load_model("what_to_do.h5")
max_len=17

while True:

    with sr.Microphone() as source:

        listener.adjust_for_ambient_noise(source)
        print('listening...')
        voice = listener.listen(source, phrase_time_limit=6)
        command = listener.recognize_google(voice, language="ru-RU")

        print(command)
        sequence = tokenizer.texts_to_sequences([command])
        data = pad_sequences(sequence, maxlen=max_len)
        result = model.predict(data)
        print(numpy.argmax(result))
        do_smth(numpy.argmax(result),command)





