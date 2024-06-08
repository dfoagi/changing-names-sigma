import re


def del_nums(root, tree, way):
    standart_names = ['Проем', 'Блок', 'Помещение', 'Группа проемов', 'Этаж', 'Площадка', 'Марш', 'Л']
    for elem in root.iter('NAME'):
        name = elem.text
        standart_name = False
        for i in standart_names:
            if i in name:
                standart_name = True
                break

        # поиск элементов, которые переименовал руками, у которых оставил пробельный символ в конце
        if re.search(r' _\d.*', name):
            name = re.sub(r' _\d.*', ' ', name)
            elem.text = name

        # поиск элементов, у которых id приклеился к другим id _id1_id2_id3_id4 -> _id4
        if re.search(r'_\d.*_', name):
            name = re.sub(r'_\d.*_', '_', name)
            elem.text = name

        # Поиск элемента с ненужным концом и с нестандартным названием
        if re.search(r'_\d.*', name) and not standart_name:
            name = re.sub(r'_\d.*', '', name)
            elem.text = name

    tree.write(way, encoding='windows-1251')


def add_spaces(root, tree, way):
    for rooms in root.iter('ROOMLIST'):  # парсим список списков помещений
        for room in rooms:  # проходимся по списку помещений для одного этажа
            if room.tag != 'Count':  # убеждаемся что мы не в счетчике
                room_name = room.find('NAME').text
                room_id = room.find('ID').text

                if room_name != 'Помещение_' + room_id:
                    room.find('NAME').text = str(room.find('NAME').text).rstrip() + ' '

    tree.write(way, encoding='windows-1251')


def change_boxes(root, tree, way):
    for apertures in root.iter('APERTURELIST'):  # проходимся по списку проемов/групп проемов
        for aperture in apertures:
            if aperture.tag != 'Count':  # проверяем, что не попали в счетчик
                cn = aperture.find('CLASSNAME').text

                if cn == 'TAperture':  # если нашли дверь просто на этаже
                    if aperture.find('BOX1').text == '-1':
                        aperture.find('BOX1').text, aperture.find('BOX2').text = aperture.find(
                            'BOX2').text, aperture.find('BOX1').text

                elif cn == 'TPorta':  # если попали на группу проемов
                    type = aperture.find('TP').text  # определяем тип проема
                    if type == '0':  # тип 0 для двойных дверей
                        name = ''
                        cnt = 0
                        for door in aperture.find('GEOM'):  # проходимся по дверям в группе проемов
                            if door.tag != 'Count':  # проверяем, что не попали в счетчик
                                if door.find('BOX1').text == '-1':
                                    door.find('BOX1').text, door.find('BOX2').text = door.find('BOX2').text, door.find(
                                        'BOX1').text

                    else:  # тип 1 для произвольных проемов
                        for door in aperture.find('GEOM'):
                            if door.tag != 'Count':  # проверяем, что не попали в счетчик
                                if door.find('BOX1').text == '-1':
                                    door.find('BOX1').text, door.find('BOX2').text = door.find('BOX2').text, door.find(
                                        'BOX1').text

    tree.write(way, encoding='windows-1251')
