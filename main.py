import re
from time import time
from array import array

def initImages(min_score=300):
    i = 0
    print("создаю картинки...")
    image_converter = array('L', [0 for i in range(2499287)])  # этот айди лучше ставить вручную - количество артов на момент получения дампа.
    with open('images.txt', 'r', encoding='utf-8') as f:
        for l in f:
            parsed = re.split('([	]+)', l)
            if len(parsed) > 8:
                id = int(parsed[0])
                score = int(parsed[14])
                if score < min_score:
                    image_converter[id] = 0
                else:
                    i += 1
                    image_converter[id] = i
        else:
            total = i
    return total, image_converter


def initUsers(names_id, ids_name):
    print("Создаю юзеров...")
    with open('users.txt', 'r', encoding='utf-8') as f:
        for l in f:
            idName = l.split('	')
            if len(idName) == 2:
                Id = int(idName[0])
                name = idName[1][:-1]
                names_id[name] = Id
                ids_name[Id] = name
    ids = ids_name.keys()
    return len(ids), ids

def generateFaves(names_id, ids_name):
    print("Иницилизирую данные для хранения фаворитов. Программа начнет потреблять до 8ГБ оперативки...")
    faves_binary = dict()
    for k in ids:
        faves_binary[k] = array('L', [0 for i in range(int(total/31)+1)])
    print(time() - now)
    print("Смотрю на фовориты всех Дерпибуровцев...")
    with open('favs.txt', 'r', encoding='utf-8') as f:
        for l in f:
            parsed = re.split('([	]+)', l)
            if len(parsed) == 5:
                converted_id = image_id_converter[int(parsed[2])]
                faves_binary[int(parsed[4][:-1])][converted_id // 32] |= (2 ** (converted_id % 32))
    print(time() - now)
    print("Исключаю из списка тех у кого слишком мало фаворитов...")
    excludes = []
    for k in ids:
        if sum(faves_binary[k]) < 3:
            excludes.append(k)
    for ex in excludes:
        del faves_binary[ex]
        name = ids_name.pop(ex)
        names_id.pop(name)
    return excludes, faves_binary


if __name__ == '__main__':
    now = time()
    names_id = dict()
    ids_name = dict()

    total, image_id_converter = initImages()
    print(time() - now)

    totalUsers, ids = initUsers(names_id, ids_name)
    print(time() - now)

    excludes, faves_binary = generateFaves(names_id, ids_name)

    while True:
        print(time() - now)
        print("Готово! Введите свой ник для поиска друзей:")
        nick = input("")
        stat = []
        if nick in names_id:
            id = names_id[nick]
            my_faves = faves_binary[id]
            if id not in excludes:
                my_faves = faves_binary[id]
                for name, id in names_id.items():
                    his_faves = faves_binary[id]
                    all = 0
                    cross = 0
                    for my, his in zip(my_faves, his_faves):
                        all += bin(my | his).count("1")
                        cross += bin(my & his).count("1")
                    if all == 0:
                        stat.append([name, 0])
                    else:
                        stat.append([name, cross/all])
                else:
                    stat.sort(key = lambda x: x[1], reverse=True)
                    print("лучшие совпадения:")
                    for i in range(10):
                        print(stat[i])
            else:
                print("у вас очень мало артов в избранном с рейтингом минимальным рейтингом")
        else:
            print("на буре нет такого ника")


