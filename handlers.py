import os
import shutil


def backup_folder(way):
    dirs = os.walk(way)
    if 'backups' not in next(dirs)[1]:
        nbf = os.path.join(way, 'backups')
        os.mkdir(nbf)


def make_back(way):
    file_way = way
    file_name = way.split('\\')[-1][:4]
    fold = os.path.join(os.path.abspath(way), os.pardir)
    backup_fold_way = os.path.join(fold, 'backups')
    cnt = len(next(os.walk(backup_fold_way))[2])
    backup_name = file_name + '_back_' + str(cnt+1) + '.xml'
    new_back = os.path.join(backup_fold_way, backup_name)
    shutil.copy(file_way, new_back)


def change_heights(root, tree, way):
    for rooms in root.iter('ROOMLIST'):                     # парсим список списков помещений
        for room in rooms:                                  # проходимся по списку помещений для одного этажа
            if room.tag != 'Count':                         # убеждаемся что мы не в счетчике
                blocks = room.find('GEOM')
                for block in blocks:                        # проходимся по блокам внутри помещений
                    if block.tag != 'Count':
                        down = block.find('DOWNXYZ').text
                        up = block.find('UPXYZ').text
                        if list(up.split())[2] == '48.54':
                            new_up = list(up.split())
                            new_up[2] = '48.7'
                            new_up[5] = '48.7'
                            new_up[8] = '48.7'
                            new_up[11] = '48.7'
                            block.find('UPXYZ').text = ' '.join(new_up)

    tree.write(way, encoding='windows-1251')
    print('Finished')

