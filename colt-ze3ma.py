import random
from tkinter import * #pour générer une fenêtre et son contenu
from PIL import Image, ImageTk #pour l'import et la modification d'images


global NB_WAGONS
global NB_ACTIONS
global NB_JOUEURS 
global MAX_BULLETS
global COLORS

NB_JOUEURS = 4
NB_WAGONS = NB_JOUEURS
MAX_BULLETS = (NB_JOUEURS // 2) + 1


COLORS = {"red":(255, 0, 0),
          "orange":(255, 128, 0),
          "yellow":(255, 255, 0),
          "green":(0, 255, 0),
          "blue":(0, 0, 255)}




























class Game(Tk):
    imgPaysage = Image.open("png/landscape.png")
    imgMarshall = Image.open('png/marshall.png')
    imgsOnCanvasPlaySpace = [] # liste d'entiers (représentant les images sur un Canvas)
    wagons = [] # liste de classe Wagon
    bandits = [] # liste de classe Bandit


    def __init__(self):
        super().__init__()

        #window parameters
        self.title("Colt Zeʁma")
        # self.geometry("720x480")

        img = Image.open('train.ico')
        img = ImageTk.PhotoImage(img)
        self.call('wm', 'iconphoto', self._w, img)

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight=1)


        #zone sur laquelle on dessinera paysage, le train, les personnages et les butins
        self.playSpace = Canvas(self)
        self.playSpace.grid(row = 0, column= 0, sticky='nsew')

        #zone sur laquelle on placera les boutons d'interactions
        self.menuSpace = Canvas(self)
        self.menuSpace.grid(row = 0, column= 1, sticky='nsew')


        #=== PLAY SPACE ====================================
        #création des wagons
        for y in range(NB_WAGONS + 1):
            #loco
            if y == 0:
                self.wagons.append(Wagon(self, y, type='loco'))
                continue
            #queue
            if y == NB_WAGONS:
                self.wagons.append(Wagon(self, y, type='wagon'))
                continue
            #wagon
            self.wagons.append(Wagon(self, y, type='queue'))

        #=== FIN PLAY SPACE ================================


        #=== MENU SPACE ====================================
        self.menuSpace.rowconfigure(0, weight=1)
        self.menuSpace.columnconfigure(0, weight=1)

        self.buttonsZone = Frame(self.menuSpace, width= 400, height= 100)

        #boutons
        self.btnAction = Button(self.buttonsZone, text="(Actions test)", command=self.testActionsStep1on4)
        self.btnRight = Button(self.buttonsZone, text="->")
        self.btnLeft = Button(self.buttonsZone, text="<-")
        self.btnUp = Button(self.buttonsZone, text="(Wagons' bandits)", command=self.printButinsOfAllWagons)
        self.btnDown = Button(self.buttonsZone, text="(Bandits' butins)", command=self.printButinsOfAllBandits)
        self.btnShoot = Button(self.buttonsZone, text="(Bandits' bullets)", command=self.printBulletsOfAllBandits)
        self.btnSteal = Button(self.buttonsZone, text="(Wagons' butins)", command=self.printButinsOfAllWagons)

        #actions history
        self.actionsHistory = Label(self.menuSpace, text = "EMPTY\nHistory")

        #placement des widgets
        self.buttonsZone.grid(row=0,column=0,sticky='nsew')
        self.btnAction.grid(row=5, column=1, padx=5, pady=10, sticky="news")
        self.btnRight.grid(row=1, column=2, rowspan=2, sticky="news")
        self.btnLeft.grid(row=1, column=0, rowspan=2, sticky="news")
        self.btnUp.grid(row=0, column=1, sticky="news")
        self.btnDown.grid(row=3, column=1, sticky="news")
        self.btnShoot.grid(row=1, column=1, sticky="news")
        self.btnSteal.grid(row=2, column=1, sticky="news")
        self.actionsHistory.grid(row=7, column=0, columnspan=3, sticky="news")

        #=== FIN MENU SPACE ================================


        #création des bandits
        for i in range(NB_JOUEURS):
            name = "Bandit" + str(i + 1)
            color = random.choice(list(COLORS.values()))
            Game.bandits.append(Bandit(self, name, color))


        #ajout du marshall
        self.wagons[0].marshall = True


        #resize des images de l'interface lorsque la fenêtre est redimensionnée
        self.playSpace.bind('<Configure>', lambda e: self.updateCanvasImgs())




    def testActionsStep1on4(self):
        self.btnAction.config(state='disabled')
        #execute l'action de chaque bandit (donnée aléatoirement)
        print("Execute first action of each bandit :")
        for bandit in Game.bandits:
            bandit.testRandomAction()
        print()

        #update du Canvas
        self.updateCanvasImgs()

        self.after(ms=100, func=self.testActionsStep2on4)


    def testActionsStep2on4(self):
        #verifie pour chaque bandit s'il le Marshall est au même endroit (déplace le bandit si oui)
        for bandit in Game.bandits:
            bandit.checkMarshallPresence()
        
        #update du Canvas
        self.updateCanvasImgs()

        self.after(ms=500, func=self.testActionsStep3on4)


    def testActionsStep3on4(self):
        #déplace le marshall
        self.moveMarshall()

        #update du Canvas
        self.updateCanvasImgs()

        self.after(ms=100, func=self.testActionsStep4on4)
        

    def testActionsStep4on4(self):
        #verifie pour chaque bandit s'il le Marshall est au même endroit (déplace le bandit si oui)
        for bandit in Game.bandits:
            bandit.checkMarshallPresence()

        #update du Canvas
        self.updateCanvasImgs()
        self.btnAction.config(state='normal')

 


    def printBanditsOfAllWagons(self): #à supprimer
        print("Bandits de chaque wagon :")
        for wagon in Game.wagons:
            print(f'wagon {wagon.xPosition + 1} => ', end='')
            for bandit in wagon.bandits:
                print(f"({bandit.name}:{bandit.position['y']})", end=' ')
            print()
        print()


    def printButinsOfAllWagons(self): #à supprimer
        print("Butins de chaque wagon :")
        for wagon in Game.wagons:
            print(f'wagon {wagon.xPosition + 1} => ', end='')
            for butin in wagon.butins:
                print(f"[{butin.type}({butin.value}){butin.bracable}]", end=' ')
            print()
        print()


    def printButinsOfAllBandits(self): #à supprimer
        print("Butins de chaque bandits :")
        for bandit in Game.bandits:
            print(f'{bandit.name} => ', end='')
            for butin in bandit.butins:
                print(f"[{butin.type}({butin.value}){butin.bracable}]", end=' ')
            print()
        print()


    def printBulletsOfAllBandits(self): #à supprimer
        print("Bullets de chaque bandits :")
        for bandit in Game.bandits:
            print(f'{bandit.name} => {bandit.bullets}')
        print()




    def updateCanvasImgs(self):
            #oum: j'ai mis en commentaire cette ligne pk ça beug
            #self.update()

            #ON VIDE LE CANVAS ===================================
            for img in self.imgsOnCanvasPlaySpace:
                self.playSpace.delete(img)
            self.imgsOnCanvasPlaySpace.clear()

            #ON DÉFINI LES TAILLES DE TOUTES LES IMAGES ==========
            #taille du Canvas
            widthCanvas = self.playSpace.winfo_width()
            heightCanvas = self.playSpace.winfo_height()

            #taille d'un Wagon
            widthWagon = widthCanvas // (NB_WAGONS+1)
            heightWagon = heightCanvas // 3
            #taille des personnages (marshall and Bandit)
            widthCharacter = int (widthWagon * 0.4)
            heightCharacter = heightWagon//2


            #var "img" will be used as a create_image() container

            #ON DESSINE LE BACKGROUND ============================
            self.imgPaysage = Game.createLoadedImg(widthCanvas, heightCanvas, Game.imgPaysage)
            img = self.playSpace.create_image(0, 0, image=self.imgPaysage, anchor="nw")
            self.imgsOnCanvasPlaySpace.append(img)



            #ON DESSINE LES WAGONS ==============================
            self.imgLoco = Game.createLoadedImg(widthWagon, heightWagon, Wagon.imgLoco)
            self.imgWagon = Game.createLoadedImg(widthWagon, heightWagon, Wagon.imgWagon)
            self.imgQueue = Game.createLoadedImg(widthWagon, heightWagon, Wagon.imgQueue)
            
            #loco
            img = self.playSpace.create_image(0, heightWagon, image=self.imgLoco, anchor="nw")
            self.imgsOnCanvasPlaySpace.append(img)
            
            #wagon
            for xWagonPosition in range(1, NB_WAGONS):
                img = self.playSpace.create_image(xWagonPosition*widthWagon, heightWagon, image=self.imgWagon, anchor="nw")
                self.imgsOnCanvasPlaySpace.append(img)

            #queue
            img = self.playSpace.create_image(NB_WAGONS*widthWagon, heightWagon, image=self.imgQueue, anchor="nw")
            self.imgsOnCanvasPlaySpace.append(img)

            #FIN === ON DESSINE LES WAGONS =====================



            #ON DESSINE LES BANDITS ============================
            #les Offset permet de placer un personnage au centre du wagon
            xOffsetCharacter = (widthWagon//2) - (widthCharacter//2)
            yOffsetCharacter = (heightWagon-heightCharacter)

            for wagon in Game.wagons:
                nbBandits = len(wagon.bandits)

                if nbBandits == 0:
                    continue

                for i, bandit in enumerate(wagon.bandits):
                    xBanditPosition = bandit.position['x']
                    yBanditPosition = bandit.position['y']
                    xOffsetBandit = xOffsetCharacter
                    yOffsetBandit = yOffsetCharacter

                    #faire deux cas de calcul des offSet, pour y == 0, et y == 1
                    #faire un cas spécial pour x == 0 (locomotive)

                    if (i % 2) == 1: #permet de décaler les bandit les uns des autres
                        xOffsetBandit += ((widthWagon // nbBandits) + ((i * (widthWagon // nbBandits)))) // 4

                    else:
                        xOffsetBandit -= ((widthWagon // nbBandits) + ((i * (widthWagon // nbBandits)))) // 4


                    if yBanditPosition == 1: #si le Bandit est à l'intérieur du train
                        yOffsetBandit -= heightWagon*0.2 #réhaussement de 20% de la hauteur du train
                        yOffsetBandit -= (heightWagon*0.02) * (i%3) #réhaussement de 2% * 0 ou 1 ou 2


                    xImgPosition = (xBanditPosition * widthWagon) + xOffsetBandit
                    yImgPosition = (yBanditPosition * heightWagon) + yOffsetBandit

                    bandit.img = Game.createBanditPng(widthCharacter, heightCharacter, bandit.color)
                    img = self.playSpace.create_image(xImgPosition, yImgPosition, image=bandit.img, anchor="nw")
                    self.imgsOnCanvasPlaySpace.append(img)

            #FIN === ON DESSINE LES BANDITS ======================
                    


            #ON DESSINE LE MARSHALL ==============================
            self.imgMarshal = Game.createLoadedImg(widthCharacter,heightCharacter, self.imgMarshall)
            
            for wagon in self.wagons :
                if wagon.marshall == True:
                    xOffsetMarshall = xOffsetCharacter
                    yOffsetMarshall = yOffsetCharacter - (heightWagon * 0.2) #réhaussement de 20%

                    xMarshallPosition = (wagon.xPosition * widthWagon) + xOffsetMarshall
                    yMarshallPosition = heightWagon + yOffsetMarshall
                    

                    img = self.playSpace.create_image(xMarshallPosition, yMarshallPosition, image=self.imgMarshal, anchor="nw")
                    self.imgsOnCanvasPlaySpace.append(img)
                    break
        
            # FIN === ON DESSINE LE MARSHALL ======================



    @staticmethod
    def createLoadedImg(width, height, loadedImg):
        loadedImg = loadedImg.resize((width, height))
        return ImageTk.PhotoImage(loadedImg)


    @staticmethod
    def createBanditPng(width, height, color):
        body = Bandit.imgBody.resize((width, height))
        details = Bandit.imgDetails.resize((width, height))

        #on modifie la couleur de chaque pixel du png 
        for y in range(details.height):
            for x in range(details.width):
                if details.getpixel((x, y)) != (0, 0, 0, 0): #est un pixel transparent
                    tempColor = (color[0], color[1], color[2], details.getpixel((x, y))[3])
                    details.putpixel((x, y), value=tempColor)

        img = Image.alpha_composite(body, details)
        return ImageTk.PhotoImage(img)




    def moveMarshall(self):
        xWagonPosition = 0 #position du wagon où se trouve le Marshall
        for wagon in self.wagons:
            if wagon.marshall == True:
                xWagonPosition = wagon.xPosition
                break

        #Marshall en tête de train
        if xWagonPosition == 0:
            self.wagons[xWagonPosition].marshall = False
            self.wagons[xWagonPosition + 1].marshall = True
            
        #Marshall en queue de train
        elif xWagonPosition == NB_WAGONS:
            self.wagons[xWagonPosition].marshall = False
            self.wagons[xWagonPosition - 1].marshall = True

        #Marshall ni en tête/queue du train, donc on le déplace aléatoirement
        elif (random.randint(0,1)):
            self.wagons[xWagonPosition].marshall = False
            self.wagons[xWagonPosition + 1].marshall = True

        else:
            self.wagons[xWagonPosition].marshall = False
            self.wagons[xWagonPosition - 1].marshall = True























class Wagon():
    imgLoco = Image.open('png/locomotive val.png')
    imgWagon = Image.open('png/wagon val.png')
    imgQueue = Image.open('png/queue val.png')

    butinTypes = ['bourse', 'bijoux'] #'magot' only apply for type == 'loco'


    def __init__(self, game:Game, x:int, type:str):
        self.xPosition = x
        self.marshall = False
        self.type = type #'loco' ou 'wagon' or 'queue'
        self.bandits = []
        self.butins = []

        #replissage de butins, en fonction de type
        if self.type == 'loco':
            self.butins.append(Butin(game, type = 'magot'))

        else:
            for i in range(random.randint(1, 4)):
                self.butins.append(Butin(game, type=random.choice(Wagon.butinTypes)))























class Bandit():
    imgBody = Image.open("png/bandit.png")
    imgDetails = Image.open("png/bandit_details.png")


    def __init__(self, game:Game, name:str, color:tuple):
        self.name = name
        self.color = color
        self.position = {'x':NB_WAGONS, 'y':1} #x => index du wagon dans Game.wagons, y => position dans le wagon(0=toit, 1=intérieur)
        self.actions = [] #comment on décrit une action ? (ex: 0=droite, ...5 = tirer)
        self.game = game
        self.img = None
        self.butins = []
        self.bullets = MAX_BULLETS


        #on ajoute le bandit dans la liste bandits du bon wagon (en queue de train)
        self.game.wagons[NB_WAGONS].bandits.append(self)



    def testRandomAction(self):
        act = ['right', 'left', 'up', 'down', 'shoot', 'rob']
        self.actions.append(random.choice(act))
        self.executeAction()



    #execute the action at index 0 in self.actions
    def executeAction(self):
        if not len(self.actions):
            print(f'{self.name} has no actions')
            return

        if self.actions[0] in ['right', 'left', 'up', 'down']:
            self.deplacement(self.actions[0])
        elif self.actions[0] == 'shoot':
            self.shoot()
        elif self.actions[0] == 'rob':
            self.rob()

        self.actions.pop(0)



    def deplacement(self, action:str):
        xBanditPosition = self.position['x']
        yBanditPosition = self.position['y']
        banditName = self.name

        if action == 'right':
            if xBanditPosition == NB_WAGONS:
                print(f"{banditName} can't move {action}")
                return

            #on retire le bandit du wagon actuel
            for i, bandit in enumerate(self.game.wagons[xBanditPosition].bandits):
                if not bandit.name == banditName:
                    continue
                self.game.wagons[xBanditPosition].bandits.pop(i)

            #on ajoute le bandit dans le wagon destination
            self.game.wagons[xBanditPosition+1].bandits.append(self)

            self.position['x'] += 1


        if action == 'left':
            if xBanditPosition == 0:
                print(f"{banditName} can't move {action}")
                return

            #on retire le bandit du wagon actuel
            for i, bandit in enumerate(self.game.wagons[xBanditPosition].bandits):
                if not bandit.name == banditName:
                    continue
                self.game.wagons[xBanditPosition].bandits.pop(i)

            #on ajoute le bandit dans le wagon destination
            self.game.wagons[xBanditPosition-1].bandits.append(self)

            self.position['x'] -= 1


        if action == 'up':
            if yBanditPosition == 0:
                print(f"{banditName} can't move {action}")
                return
            self.position['y'] = 0

        if action == 'down':
            if yBanditPosition == 1:
                print(f"{banditName} can't move {action}")
                return
            self.position['y'] = 1
        
        print(f'{self.name} has moved {action}')



    def checkMarshallPresence(self):
        #si le bandit est sur le toit
        if self.position['y'] == 0:
            return

        #si le Marshall est dans le même wagon
        if self.game.wagons[self.position['x']].marshall == True:
            self.getHitByMarshall()



    #tire sur un Bandit, aléatoirement, à la même position
    def shoot(self):
        print(f'{self.name} prepare to shoot')

        if self.bullets == 0:
            print(f'{self.name} has no more bullets')
            return


        nb_targets = 0

        #on compte le nombre de cible possible (nombre de bandit dans le même wagon ET au même étage)
        for bandit in self.game.wagons[self.position['x']].bandits:
            if bandit.name == self.name:
                continue

            if bandit.position['y'] == self.position['y']:
                nb_targets += 1

        if nb_targets == 0:
            print(f'{self.name} has no targets to shoot')
            return


        #on tire sur un bandit
        target = None
        while(1):
            target = random.choice(self.game.wagons[self.position['x']].bandits)
            if target.name == self.name:
                continue

            if target.position['y'] == self.position['y']: #a valuable target has been found
                break


        self.bullets -= 1
        target.getHitByBandit(self.name)



    #vole un butin, aléatoirement, sur sa position
    def rob(self):
        print(f'{self.name} rob')
        wagon = self.game.wagons[self.position['x']]
        
        if len(wagon.butins) == 0:
            print('There is no loot here')
            return


        robbedButin = wagon.butins.pop(len(wagon.butins) - 1)
        self.butins.append(robbedButin)
        robbedButin.bracable = False

        print(f'{self.name} robbed {robbedButin.type}({robbedButin.value})')



    #perd un butin, aléatoirement
    def getHitByBandit(self, ennemyName:str):
        print(f'{self.name} get hit by {ennemyName}')


        if len(self.butins) == 0: #le bandit n'a pas de butins
            return

        #on retire un butin du bandit, aléatoirement
        lostButin = self.butins.pop(random.randint(0, len(self.butins) - 1))

        #qu'on rajoute dans la liste butins du wagon du bandit
        self.game.wagons[self.position['x']].butins.append(lostButin)

        print(f'{self.name} lost {lostButin.type}({lostButin.value})')



    #perd un butin, aléatoirement, et monte sur le toit
    def getHitByMarshall(self):
        print(f'{self.name} get hit by the Marshall')


        if len(self.butins):
            #on retire un butin du bandit
            lostButin = self.butins.pop(random.randint(0, len(self.butins) - 1))
            #qu'on rajoute dans le wagon
            self.game.wagons[self.position['x']].butins.append(lostButin)
            print(f'{self.name} lost {lostButin.type}({lostButin.value})')
        
        #le bandit monte sur le toit
        self.position['y'] = 0

        print(f'{self.name} move on the roof')























class Butin():
    imgBourse = Image.open("png/bourse.png")
    imgBijoux = Image.open("png/bijoux.png")
    imgMagot = Image.open("png/magot.png")
    
    lootValues = {'bourse':[100,200], 'bijoux' : [500], 'magot' : [1000]}
    
    def __init__(self, game:Game, type:str):
        self.type = type
        self.value = random.choice(Butin.lootValues[type])
        self.inOut = 1 #0 = interieur, 1 = toit
        self.bracable = True























mon_jeu = Game()

mon_jeu.mainloop()
