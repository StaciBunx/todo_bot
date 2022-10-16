import csv


def read_csv():
    '''Чтение файла csv, возвращает список со словарем.'''
    alltasks = []
    with open('todolist.csv', 'r', encoding='utf-8', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            alltasks.append(row)
    return alltasks


def view_tasks(alltasks):
    '''Формирует из списка со словарем строку для передачи в телеграм.'''
    task_list = []
    count = 0
    for record in alltasks:
        for key, value in record.items():
            task_list.append(f'{key}: {value}')
        count += 1
        task_list.append(' ')
    task_list.append(f'Всего задач: {count}')
    string_result = '\n'.join(task_list)
    return string_result


def write_csv(record):
    '''Принимает новые значения словаря, записывает новую задачу в cvs файл.'''
    with open('todolist.csv', 'a', encoding='utf-8', newline='') as file:
        fieldnames = ['задача', 'дата']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(record)


def delete_csv(text):
    '''
    Удаляет задачу из файла cvs. Ищет в файле строку с искомым значением, остальные строки записывает во времемнное хранилище.
    Затем значения из временного хранилища перезаписывает в файл, стирая предыдущие данные.
    Возвращает строку с информацией о ходе выполнения задачи.
    '''
    temp_string = ''
    status = ''
    status_record = ''
    with open('todolist.csv', 'r', encoding='utf-8', newline='\n') as file:
        reader = csv.reader(file)
        for row in reader:
            record = ','.join(row).lower()
            if text.lower() in record:
                status_record = record
                continue
            else:
                temp_string += f'{record}\n'
    with open('todolist.csv', 'w', encoding='utf-8', newline='\n') as file:
        file.write(temp_string)
    if (status_record == ''):
        status = f'Не найдено задач с фразой "{text}"'
    else:
        status = f'УДАЛЕНО:\n{status_record}'
    return status


def mark_csv(text):
    '''
    Помечает задачу из файла cvs, как выполненную. Ищет в файле строку с искомым значением, помечает ее.
    Вместе с остальными строками записывает во времемнное хранилище.
    Затем значения из временного хранилища перезаписывает в файл, стирая предыдущие данные.
    Возвращает строку с информацией о ходе выполнения задачи.
    '''
    temp_string = ''
    status = ''
    status_record = ''
    with open('todolist.csv', 'r', encoding='utf-8', newline='\n') as file:
        reader = csv.reader(file)
        for row in reader:
            record = ','.join(row).lower()
            if text.lower() in record:
                status_record = '✅' + record
                continue
            else:
                temp_string += f'{record}\n'
        temp_string += f'{status_record}\n'
    with open('todolist.csv', 'w', encoding='utf-8', newline='\n') as file:
        file.write(temp_string)
    if (status_record == ''):
        status = f'Не найдено задач с фразой "{text}"'
    else:
        status = f'ПОМЕЧЕНО:\n{status_record}'
    return status
