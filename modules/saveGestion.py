
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






def save(nbPlayers, wagons, bandits, butins):

    with open('saves/save.txt', 'w') as file:
        file.write(f'{nbPlayers}\n')
        file.write(f'{len(butins)}\n')

        for wagon in wagons:
            y = wagon.xPosition
            type = wagon.type
            marshall = wagon.marshall
            file.write(f'{y},{type},{marshall}\n')

        for bandit in bandits:
            name = bandit.name
            color = bandit.color
            x, y = bandit.position['x'], bandit.position['y']
            actions = ''
            for i, action in enumerate(bandit.actions):
                actions += action
                if i < len(bandit.actions):
                    actions += ','
            bullets = bandit.bullets

            file.write(f'{name},{color},{x},{y},{actions},{bullets}\n')

        for butin in butins:
            type = butin.type
            value = butin.value
            x, y = butin.position['x'], butin.position['y']
            bracable = butin.bracable

            file.write(f'{type},{value},{x},{y},{bracable}\n')





"""
4
10
0,loco,False
...
Clément,green,4,0,up,shoot,left,down,rob,left,3
...
magot,1000,2,out,False
...

"""







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



"""
Wagon
    self.xPosition = x
    self.marshall = False
    self.type = type #'loco' ou 'wagon' or 'queue'
    self.bandits = []
    self.butins = []

Bandit
    self.name = name
    self.color = color
    self.position = {'x':NB_WAGONS, 'y':1} #x => index du wagon dans Game.wagons, y => position dans le wagon(0=toit, 1=intérieur)
    self.actions = [] #comment on décrit une action ? (ex: 0=droite, ...5 = tirer)
    self.game = game
    self.img = None
    self.butins = []
    self.bullets = MAX_BULLETS

Butin
    self.game = game
    self.type = type
    self.value = random.choice(Butin.lootValues[type])
    self.position = {'x':x, 'y':'in'} #y = 'in' or 'out' or '{banditName}'
    # self.inOut = 1 #1 = interieur,0 = toit
    self.bracable = True
    self.img = None
"""