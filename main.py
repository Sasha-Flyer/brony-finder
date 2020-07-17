import re
from time import time
from array import array

if __name__ == '__main__':
    now = time()
    namesIds = dict()
    idsNames = dict()
    i = 0
    imageIdConverter = array('L', [0 for i in range(2499287)])# этот айди лучше ставить вручную - количество артов на момент получения дампа.
    print(time() - now)
    print("создаю картинки...")
    with open('images.txt', 'r', encoding='utf-8') as f:
        for l in f:
            parsed = re.split('([	]+)', l)
            if len(parsed) > 8:
                id = int(parsed[0])
                score = int(parsed[14])
                if score < 300:
                    imageIdConverter[id] = 0
                else:
                    i += 1
                    imageIdConverter[id] = i
        else:
            total = i
    print(time() - now)
    print("создание картинок завершено. создаю юзеров...")
    with open('users.txt', 'r', encoding='utf-8') as f:
        for l in f:
            idName = l.split('	')
            if len(idName) == 2:
                Id = int(idName[0])
                name = idName[1][:-1]
                namesIds[name] = Id
                idsNames[Id] = name

    ids = idsNames.keys()
    totalUsers = len(ids)
    favesBinary = dict()
    print(time() - now)
    print("Иницилизирую данные для хранения фаворитов. Программа начнет потреблять до 8ГБ оперативки...")
    for k in ids:
        favesBinary[k] = array('L', [0 for i in range(int(total/31)+1)])
    print(time() - now)
    print("Смотрю на фовориты всех Дерпибуровцев...")
    with open('favs.txt', 'r', encoding='utf-8') as f:
        for l in f:

            parsed = re.split('([	]+)', l)
            if len(parsed) == 5:
                convertedId = imageIdConverter[int(parsed[2])]
                favesBinary[int(parsed[4][:-1])][convertedId // 32] |= (2 ** (convertedId % 32))
    print(time() - now)
    print("Исключаю из списка тех у кого слишком мало фаворитов...")
    excludes = []
    for k in ids:
        if sum(favesBinary[k]) < 3:
            excludes.append(k)
    for ex in excludes:
        del favesBinary[ex]
        name = idsNames.pop(ex)
        namesIds.pop(name)
    while True:
        print(time() - now)
        print("Готово! Введите свой ник для поиска друзей:")
        nick = input("")
        stat = []
        if nick in namesIds:
            id = namesIds[nick]
            myFaves = favesBinary[id]
            if id not in excludes:
                myFaves = favesBinary[id]
                for name, id in namesIds.items():
                    hisFaves = favesBinary[id]
                    all = 0
                    cross = 0
                    for my, his in zip(myFaves, hisFaves):
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
                print("у вас очень мало артов в избранном с рейтингом 300+")
        else:
            print("на буре нет такого ника")


