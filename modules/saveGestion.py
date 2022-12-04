
def loadSave():

    nbPlayers = 0
    nbButinsTotal = 0 #value not returned
    wagons = []
    bandits = []
    butins = []


    #extract datas
    i = 1
    j = 0
    with open('saves/save.txt', 'rt') as file:
        for line in file:
            # print(i, line)
            data = ""

            if i == 1: #nb players
                nbPlayers = int(line)
                i += 1

            elif i == 2: #nb butins
                nbButinsTotal = int(line)
                i += 1


            elif i == 3: #wagons
                datas = []
                for char in line:
                    if char == '\n':
                        datas.append(''.join(data))
                        break
                    if char == ',':
                        datas.append(''.join(data))
                        data = []
                        continue
                    data += char
                
                wagons.append(datas)
                j += 1

                if j == nbPlayers + 1:
                    i += 1
                    j = 0


            elif i == 4: #bandits
                datas = []
                for char in line:
                    if char == '\n':
                        datas.append(''.join(data))
                        break
                    if char == ',':
                        datas.append(''.join(data))
                        data = []
                        continue
                    data += char
                
                bandits.append(datas)
                j += 1

                if j == nbPlayers:
                    i += 1
                    j = 0

            elif i == 5: #butins
                datas = []
                for char in line:
                    if char == '\n':
                        datas.append(''.join(data))
                        break
                    if char == ',':
                        datas.append(''.join(data))
                        data = []
                        continue
                    data += char
                
                butins.append(datas)
                j += 1

                if j == nbButinsTotal:
                    i += 1
                    j = 0




    #convert some data to the good type

    for wagon in wagons:
        wagon[0] = int(wagon[0])
        if wagon[2] == 'False':
            wagon[2] = False
        elif wagon[2] == 'True':
            wagon[2] = True
        else:
            wagon[2] = int(wagon[2])

    for bandit in bandits:
        bandit[2] = int(bandit[2])
        bandit[3] = int(bandit[3])
        bandit[-1] = int(bandit[-1])

    for butin in butins:
        butin[1] = int(butin[1])
        butin[2] = int(butin[2])
        if butin[4] == 'False':
            butin[4] = False
        elif butin[4] == 'True':
            butin[4] = True
        else:
            butin[4] = int(butin[4])

    


    return nbPlayers, wagons, bandits, butins



# b, c, d, e = loadSave()


# print(b)

# for n in c:
#     print(n)
# print()

# for n in d:
#     print(n)
# print()

# for n in e:
#     print(n)
# print()


# print(d[0][4:-1])