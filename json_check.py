import os
import json
import copy
import jsonschema
from jsonschema import validate
from datetime import datetime

path = globals()['__file__'] #получаем полное имя исполняемого файла
path = path[:path.rfind('\\')+1]+'\\task_folder\\schema\\' # отделяем путь к исполняеммому файлу от его полного имени

def check_json_item(item, file, idx = 0):
    global label_selected, cmarker_created, sleep_created, workout_created
    try:
        out_str =''
        item_type = item['event']
        if item_type == 'label_selected':
            schema = copy.deepcopy(label_selected)
        elif item_type == 'cmarker_created':
            schema = copy.deepcopy(cmarker_created)
        elif item_type == 'sleep_created':
            schema = copy.deepcopy(sleep_created)
        elif item_type == 'workout_created':
            schema = copy.deepcopy(workout_created)
        else:
            raise Exception(item_type)

        out_str = '''<tr ><td colspan = 4 style = "color : purple; text-align : center; ">Проверка на соответствие схеме {0}</td></tr>'''.format(item_type)
        out_str += '''<tr ><td colspan = 4 style = "color : green; text-align : center; ">Сущность № {0}: Начало проверки</td></tr>'''.format(idx)        
        while True: 
            try:
                validate(item, schema)
                out_str += '''<tr ><td colspan = 4 style = "color : green; text-align : center; ">Сущность № {0}: Проверека завершена</td></tr>'''.format(idx)
                return(out_str)        
            except jsonschema.exceptions.ValidationError as ve:
                err = str(ve)
                if err.find('is a required property') > -1:
                    err = err[:err.find('is a required property')]
                    out_str += '<tr><td>{0}</td><td>{1}</td><td style = "color: red;">Отсутствует обязательный параметр (ключ) {2}</td><td>1) В JSON-схеме удалите параметр <b>{2}</b> из раздела <b>required</b><br>2) Приведите в корректный формат структуру сущности {1}</td></tr>'.format(file,idx,err)
                    del schema['required'][0]


                if err.find('is not of type') > -1:
                    dtype = err[err.find("'")+1:]
                    dtype = dtype[:dtype.find("'")]
                    err = err[err.find('On instance[')+13:]
                    err = err[:err.find(']')-1]
                    out_str += '<tr><td>{0}</td><td>{1}</td><td style = "color: red;">Тип данных параметра (ключа) <b>{2}</b> не соответствует требуемому</td><td>Исправьте данные для параметра <b>{2}</b> на данные типа <b>{3}</b>.</td></tr>'.format(file,idx,err,dtype)    
                    # del item[err]
                    return out_str

        
    except KeyError:
        out_str += '<tr ><td>{0}</td><td>{1}</td><td style = "color: red;">{2} <br>Проверить сущность невозможно.</td><td>Проверьте корректность структуры сущности {1} в файле {0}</td></tr>'.format(file,idx,'(Нет ключа Event).')
        return out_str
    except Exception as e:
        out_str += '<tr ><td>{0}</td><td>{1}</td><td style = "color: red;">Не найден файл для схемы <b>{2}</b>.<br> Проверить сущность невозможно.</td><td>Положите файл схемы <b>{2}</b> в папку с другими схемами</td></tr>'.format(file,idx,e)
        return out_str





with open(path+'cmarker_created.schema','r') as f:
    # add try block
    cmarker_created = json.load(f)

with open(path+'label_selected.schema','r') as f:
    # add try block
    label_selected = json.load(f)

with open(path+'sleep_created.schema','r') as f:
    # add try block
    sleep_created = json.load(f)

with open(path+'workout_created.schema','r') as f:
    # add try block
    workout_created = json.load(f)


out_file = open(path.replace('task_folder\\schema\\','')+'README.html','a')
path  = path.replace('schema','event')
out_str = '''<table border = "1" align = "center">
            <tbody>
                <tr ><th colspan = 5 style = "color : blue;"><b>Начало теста {0}</b></th></tr>

'''.format(datetime.now())
out_file.write(out_str)
for file in os.listdir(path):
    with open(path+file,'r') as f:
        data = json.load(f)
        out_str = '''<tr ><td colspan = 4 style = "color : green; text-align : center; ">- - - - - - - -</td></tr>
                <tr ><td colspan = 4 style = "color : green; text-align : left; ">Проверяем файл: <br> <b>{}</b></td></tr>
                <tr>
                    <td align = "center">
                    <b>Имя файла</b></td>
                    <td><b>Номер сущности</b></td>
                    <td><b>Ошибка</b></td>
                    <td><b>Вариант решения</b></td>
                </tr>
        '''.format(file)
        out_file.write(out_str)  
        if type(data).__name__ == 'list':
            for idx, val in enumerate(data):
                out_file.write(check_json_item(val, file, idx)) 
        elif type(data).__name__ == 'dict':
            out_file.write(check_json_item(data, file))
        else:
            out_str = '''<tr ><td colspan = 3 style = "color : red; text-align : left; ">Содержимое файла {0} не соответствует формату JSON или файл пуст</td><td>замените файл {0}</td></tr>'''.format(file)
            out_file.write(out_str)
        
        out_str = '''<tr ><td colspan = 4 style = "color : green; text-align : left; ">Проверка файла <b>{}</b>  завершена</td></tr>
        '''.format(file)
        out_file.write(out_str)  
        

out_str = '''<tr ><td colspan = 4 style = "color : blue; text-align : center; "><b>Конец теста {0}</b></td></tr>
</tbody></table>
'''.format(datetime.now())
out_file.write(out_str)          
out_file.close()
print('Тест завершен!')