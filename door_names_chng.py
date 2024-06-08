def change_names(root, tree, way):
    hm_room_to_block = {'-1': False}  # заводим словарь с ключом -1 для выходов наружу

    def parse_names(hm: dict, roomlist: str):
        for rooms in root.iter(roomlist):  # парсим список списков помещений
            for room in rooms:  # проходимся по списку помещений для одного этажа
                if room.tag != 'Count':  # убеждаемся что мы не в счетчике
                    room_name = room.find('NAME').text  # запоминаем имя помещения
                    blocks = room.find('GEOM')
                    for block in blocks:  # проходимся по блокам внутри помещений
                        if block.tag != 'Count':
                            block_id = block.find('ID').text  # запоминаем айди блока
                            hm[block_id] = room_name  # сохраняем в словарь пару айди блока : имя помещения

    def change_name(door):  # меняем имя для *проема
        type = door.find('TP').text  # запоминаем тип (0 - дверь, 2 - проем, 3 -выход)
        box1 = hm_room_to_block[door.find('BOX1').text]  # имя первого блока
        box2 = hm_room_to_block[door.find('BOX2').text]  # имя второго блока
        new_name = ''
        if door.find('NAME').text.startswith('Проем_'):
            if (
                    type == '0' or type == '2') and box1 != box2 and box1 and box2:  # проверяем, что это дверь или проем между помещениями
                # print(door.find('NAME').text, (box1, box2))
                new_name = box1.rstrip() + ' - ' + box2.lstrip()
            elif (type == '0' or type == '2') and box1 == box2 and box1 and box2:
                new_name = 'Проем в ' + box1.lstrip()
            elif type == '3':  # если это выход наружу
                new_name = 'ВЫХОД ' + box1.lstrip() if box1 else 'ВЫХОД ' + box2.lstrip()
            else:  # если это окно или дверь/проем внутри одного помещения
                return  # не трогаем
            door.find('NAME').text = new_name  # записываем в файл
            return new_name  # возвращаем имя, если нужно переименовтаь двустворчатую дверь

    def door_iter(root):
        for apertures in root.iter('APERTURELIST'):  # проходимся по списку проемов/групп проемов
            for aperture in apertures:
                if aperture.tag != 'Count':  # проверяем, что не попали в счетчик
                    cn = aperture.find('CLASSNAME').text

                    if cn == 'TAperture':  # если нашли дверь просто на этаже
                        change_name(aperture)  # меняем для нее имя

                    elif cn == 'TPorta':  # если попали на группу проемов
                        type = aperture.find('TP').text  # определяем тип проема
                        if type == '0':  # тип 0 для двойных дверей
                            name = ''
                            cnt = 0
                            for door in aperture.find('GEOM'):  # проходимся по дверям в группе проемов
                                if door.tag != 'Count':  # проверяем, что не попали в счетчик
                                    name = change_name(door)  # меняем имя для двери сохраняем его
                                else:
                                    cnt = int(door.text)  # смотрим сколько дверей в группе
                            if cnt == 2 and name:  # проверяем, что в группе 2 двери, а не забыли сменить тип
                                aperture.find('NAME').text = name  # меняем имя для самой группы
                        else:  # тип 1 для произвольных проемов
                            for door in aperture.find('GEOM'):
                                if door.tag != 'Count':  # проверяем, что не попали в счетчик
                                    if door.find('TP').text != '2':
                                        name = change_name(door)  # меняем имя для двери

    # парсим блоки и создаем из них хешмапу "ид_блока: название помещения, в котором этот блок"
    parse_names(hm_room_to_block, 'ROOMLIST')
    parse_names(hm_room_to_block, 'STAIRWAYLIST')
    door_iter(root)

    tree.write(way, encoding='windows-1251')  # сохраняем xml-файл
