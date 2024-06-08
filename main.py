import PySimpleGUI as sg
import xml.etree.ElementTree as ET
import os
from del_nums import del_nums, add_spaces
from handlers import backup_folder, make_back, change_heights
from door_names_chng import change_names


# Define the window's contents
layout = [[sg.Text("Укажите путь к файлу, с которым будем работать")],
          [sg.Input(key='-FN-', enable_events=True, visible=True),
           sg.FileBrowse(file_types=(('XML', '*.xml'), ), target='-FN-')],
          [sg.Text(size=(40,1), key='-OUTPUT-')],
          [sg.Button('добавить пробелы', visible=False)],
          [sg.Button('убрать лишние id', visible=False)],
          [sg.Button('переименовать двери', visible=False)],
          [sg.Button('сменить высоту', visible=False)],
          [sg.Button('Ok'), sg.Button('Quit')]]

# Create the window
window = sg.Window('Меняем имена', layout)

tree = None
root = None
way = None

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.Read()
    # print(event)
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    if event == '-FN-':
        window['добавить пробелы'].update(visible=False)
        window['убрать лишние id'].update(visible=False)
        window['переименовать двери'].update(visible=False)
        window['сменить высоту'].update(visible=False)
        way = values['-FN-'].split('/')
        dir = "\\".join(way[:-1])
        file_name = way[-1]
        way = os.path.join(dir, file_name)
        if os.path.isfile(way):
            if way.endswith('.xml'):
                if '_people' in way:
                    window['-OUTPUT-'].update('Выбран файл с людьми')
                elif '_furniture' in way:
                    window['-OUTPUT-'].update('Выбран файл с мебелью')
                elif '_doors' in way:
                    window['-OUTPUT-'].update('Выбран файл с дверьми')
                else:
                    backup_folder(dir)
                    tree = ET.parse(way)
                    root = tree.getroot()
                    window['-OUTPUT-'].update('Файл найден')
                    window['добавить пробелы'].update(visible=True)
                    window['убрать лишние id'].update(visible=True)
                    window['переименовать двери'].update(visible=True)
                    window['сменить высоту'].update(visible=True)
            else:
                window['-OUTPUT-'].update('Выбран не xml файл')
        else:
            window['-outfn-'].update('Выбран некорректный путь')

    if event == 'добавить пробелы':
        make_back(way)
        add_spaces(root, tree, way)
        print('Добавлены пробелы')

    if event == 'убрать лишние id':
        make_back(way)
        del_nums(root, tree, way)
        print('Убраны id')

    if event == 'переименовать двери':
        make_back(way)
        change_names(root, tree, way)
        print('Названия поменяны')

    if event == 'сменить высоту':
        make_back(way)
        change_heights(root, tree, way)
        print('Высоты изменены')

# Finish up by removing from the screen
window.close()
