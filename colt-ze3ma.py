import random
from tkinter import * #pour générer une fenêtre et son contenu
from PIL import Image, ImageTk #pour l'import et la modification d'images
from modules.saveGestion import * #for loadSave(win)


global NB_WAGONS
global NB_ACTIONS
global NB_JOUEURS 
global MAX_BULLETS
global COLORS
global LOAD_SAVE
global WIDGET_COLORS

NB_JOUEURS = 4
NB_WAGONS = NB_JOUEURS
MAX_BULLETS = (NB_JOUEURS // 2) + 1


COLORS = {"red":(255, 0, 0),
          "orange":(255, 128, 0),
          "yellow":(255, 255, 0),
          "green":(0, 255, 0),
          "blue":(0, 0, 255)}

WIDGET_COLORS = {"red":"#b13001",
                "redLight":"#ca3904",
                "sand":"#c1880b",
                "train":"#854a04"}

LOAD_SAVE = FALSE



























class Game(Tk):
    wagons = [] # liste de classe Wagon
    bandits = [] # liste de classe Bandit
    butins = [] # liste de classe Bandit


    imgsOnCanvasPlaySpace = [] # liste "stockant" ce qui est dessiné sur un Canvas (afin de les pouvoir les supprimer par la suite)
    imgsOnCanvasMenuSpace = []

    #chargement de toutes les images
    #certaines images ont un % en commentaire, % par rapport à un wagon
    imgMenuSpace = Image.open('png/menuSpaceBackground.png')
    imgMenuButton = Image.open('png/menuSpaceButton.png')

    imgPaysage = Image.open("png/landscape.png")
    imgMarshall = Image.open('png/marshall_v0.png') #width = 26%, height = 42%

    imgLoco = Image.open('png/loco_v2.png') #width = 200%
    imgWagon = Image.open('png/wagon_v2.png')
    imgQueue = Image.open('png/queue_v2.png')

    imgBourse = Image.open("png/bourse_v0.png") #width = 13%, height = 11%
    imgBijoux = Image.open("png/bijoux_v0.png") #width = 7%, height = 6%
    imgMagot = Image.open("png/magot_v0.png") #width = 35%, height = 20%

    imgBody = Image.open("png/bandit_body_v0.png") #width = 26%, height = 42%
    imgDetails = Image.open("png/bandit_details_v0.png") #width = 26%, height = 42%



    def __init__(self):
        super().__init__()
        self.turn = 1

        #window parameters
        self.title("Colt Zeʁma")
        self.geometry("900x415")

        img = Image.open('train.ico')
        img = ImageTk.PhotoImage(img)
        self.call('wm', 'iconphoto', self._w, img)

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight=1)

        self.btnLoad = Button(self, text='Load', command=self.loadSave)
        self.btnNew = Button(self, text='New', command=self.continueInit)

        self.btnLoad.grid()
        self.btnNew.grid(column=1)


    def loadSave(self):
        global LOAD_SAVE
        LOAD_SAVE = True
        self.continueInit()


    def continueInit(self):
        self.btnLoad.destroy()
        self.btnNew.destroy()

        #la fenêtre est coupée en 2 parties :
        #    playSpace: Canvas sur lequel on dessine l'aspect visuel du jeu (bg, train, personnages...)
        #    menuSpace: Canvas sur lequel on interagit avec le jeu (bouttons d'action, log, save, exit...)



        #=== PLAY SPACE ====================================
        self.playSpace = Canvas(self, highlightthickness=0)
        self.playSpace.grid(row = 0, column= 0, sticky='nsew')

        #=== FIN PLAY SPACE ================================


        #=== MENU SPACE ====================================
        self.menuSpace = Canvas(self, bg=WIDGET_COLORS['redLight'], highlightthickness=2, border=0, highlightbackground=WIDGET_COLORS['red'])
        self.menuSpace.grid(row = 0, column= 1, sticky='nsew')

        for i in range(9):
            self.menuSpace.rowconfigure(i, weight=1)
        for i in range(3):
            self.menuSpace.columnconfigure(i, weight=1)


        #boutons
        self.btnAction = Button(self.menuSpace, text="Action", command=self.testActionsStep1on4)
        self.btnRight = Button(self.menuSpace, text="->", command=self.saveGame)
        self.btnLeft = Button(self.menuSpace, text="<-")
        self.btnUp = Button(self.menuSpace, text="Up")
        self.btnDown = Button(self.menuSpace, text="Down")
        self.btnShoot = Button(self.menuSpace, text="Shoot")
        self.btnSteal = Button(self.menuSpace, text="Rob")

        #placement des buttons
        self.btnAction.grid(row=5, column=1, padx=5, pady=10, sticky="nsew")
        self.btnRight.grid(row=1, column=2, rowspan=2, sticky="ew")
        self.btnLeft.grid(row=1, column=0, rowspan=2, sticky="ew")
        self.btnUp.grid(row=0, column=1, sticky="nsew")
        self.btnDown.grid(row=3, column=1, sticky="nsew")
        self.btnShoot.grid(row=1, column=1, sticky="nsew")
        self.btnSteal.grid(row=2, column=1, sticky="nsew")


        #actions history
        self.logSpace = Canvas(self.menuSpace, border=0)
        self.logSpace.rowconfigure(0, weight=1)
        self.logSpace.rowconfigure(3, weight=1)
        self.logSpace.columnconfigure(0, weight=1)
        self.logSpace.columnconfigure(3, weight=1)


        self.lbLog = Label(self.logSpace, text="History", font=("Ariel", 12), fg=WIDGET_COLORS["sand"], bg=WIDGET_COLORS["train"])
        self.log = Text(self.logSpace, font=("Ariel", 10), highlightthickness=1, border=0, highlightbackground=WIDGET_COLORS['train'], bg=WIDGET_COLORS["sand"])
        vbar = Scrollbar(self.logSpace, orient=VERTICAL, bg=WIDGET_COLORS['train'], highlightthickness=1, border=0, highlightbackground=WIDGET_COLORS['train'], activebackground=WIDGET_COLORS['red'], troughcolor=WIDGET_COLORS['sand'], width=15)

        vbar.config(command=self.log.yview)
        self.log.config(yscrollcommand=vbar.set)

        self.log.insert(END,"EMPTY\nHistory\n")
        self.log.config(state=DISABLED)

        #placement du log
        self.logSpace.grid(row=9, column=0, columnspan=3)
        self.lbLog.grid(row=1, column=1, columnspan=2, sticky="nsew")
        self.log.grid(row=2, column=2, sticky="nsew")
        vbar.grid(row=2, column=1, sticky='NS')

        #=== FIN MENU SPACE ================================


        #créations des wagons, personnages et butins
        global NB_JOUEURS

        #create from new game
        if not LOAD_SAVE:
            #création des wagons
            for y in range(NB_WAGONS + 1):
                #loco
                if y == 0:
                    self.wagons.append(Wagon(self, y, 'loco'))
                    continue
                #queue
                if y == NB_WAGONS:
                    self.wagons.append(Wagon(self, y, 'wagon'))
                    continue
                #wagon
                self.wagons.append(Wagon(self, y, 'queue'))


            #création des bandits
            for i in range(NB_JOUEURS):
                name = "Bandit" + str(i + 1)
                color = random.choice(list(COLORS.keys()))
                Game.bandits.append(Bandit(self, name, color))


            #ajout du marshall
            self.wagons[0].marshall = True


        #create from loaded game
        else:
            #import save
            NB_JOUEURS, tempWagons, tempBandits, tempButins = loadSave()

            #load Wagon(s)
            for wagonElement in tempWagons:
                xPos = wagonElement[0]
                type = wagonElement[1]
                marshall = wagonElement[2]

                loadedWagon = Wagon(self, xPos, type, marshall=marshall)
                self.wagons.append(loadedWagon)

            #load Bandit(s)
            for banditElement in tempBandits:
                name = banditElement[0]
                color = banditElement[1]
                xPos, yPos = banditElement[2], banditElement[3]
                actions = banditElement[4:-1]
                bullets = banditElement[-1]

                loadedBandit = Bandit(self, name, color, position=(xPos, yPos), actions=actions, bullets=bullets)
                self.bandits.append(loadedBandit)

            #load Butin(s)
            for butinElement in tempButins:
                type = butinElement[0]
                value = butinElement[1]
                xPos, yPos = butinElement[2], butinElement[3]
                bracable = butinElement[4]

                loadedButin = Butin(self, type, None, value=value, position=(xPos, yPos), bracable=bracable)
                # le Butin s'auto append dans self.butins


            # butins' distribution
            for butin in self.butins:
                #in a Wagon
                if butin.position['y'] in ['in', 'out']:
                    self.wagons[butin.position['x']].butins.append(butin)
                
                #in a Bandit
                else:
                    for bandit in self.bandits:
                        if bandit.name == butin.position['y']:
                            bandit.butins.append(butin)
                            break



        #resize des images de l'interface lorsque la fenêtre est redimensionnée
        self.playSpace.bind('<Configure>', lambda e: self.updateCanvasImgs())




    def saveGame(self):
        save(NB_JOUEURS, self.wagons, self.bandits, self.butins)



    def insertTextInLog(self, text):
        self.log.config(state="normal")
        self.log.insert(END, text)
        self.log.see(END)
        self.log.config(state="disabled")



    def testActionsStep1on4(self):
        self.btnAction.config(state='disabled')
        #execute l'action de chaque bandit (donnée aléatoirement)

        self.insertTextInLog(f"\nTurn {self.turn} :\n")
        self.turn += 1

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







    def updateCanvasImgs(self):
        #ON VIDE LE CANVAS ===================================
        for img in self.imgsOnCanvasPlaySpace:
            self.playSpace.delete(img)
        for img in self.imgsOnCanvasMenuSpace:
            self.menuSpace.delete(img)
        self.imgsOnCanvasPlaySpace.clear()
        self.imgsOnCanvasMenuSpace.clear()



        #ON DÉFINI LES TAILLES DE TOUTES LES IMAGES ==========
        #taille du Canvas
        widthCanvas = self.playSpace.winfo_width()
        heightCanvas = self.playSpace.winfo_height()

        #taille d'un Wagon
        widthWagon = widthCanvas // (NB_WAGONS+1+1)
        heightWagon = heightCanvas // 3
        #taille des personnages (marshall and Bandit)
        widthCharacter = int (widthWagon *0.26)
        heightCharacter = int (heightWagon *0.42)

        #taille des butins
        widthButin = int(widthWagon * 0.1)
        heightButin = heightWagon//4



        #resize du log
        self.log.config(width=int((widthCanvas//2)*0.075), height=int((heightCanvas//3)*0.08))


        #var "img" will be used as a create_image() container

        #ON DESSINE LE BACKGROUND ============================
        self.imgPaysage = Game.createLoadedImg(widthCanvas, heightCanvas, Game.imgPaysage)
        img = self.playSpace.create_image(0, 0, image=self.imgPaysage, anchor="nw")
        self.imgsOnCanvasPlaySpace.append(img)



        #ON DESSINE LES WAGONS ==============================
        self.imgLoco = Game.createLoadedImg(widthWagon*2, heightWagon, Game.imgLoco)
        self.imgWagon = Game.createLoadedImg(widthWagon, heightWagon, Game.imgWagon)
        self.imgQueue = Game.createLoadedImg(widthWagon, heightWagon, Game.imgQueue)

        #loco
        img = self.playSpace.create_image(0, heightWagon, image=self.imgLoco, anchor="nw")
        self.imgsOnCanvasPlaySpace.append(img)

        #wagon
        for xWagonPosition in range(1, NB_WAGONS):
            img = self.playSpace.create_image((xWagonPosition +1)*widthWagon, heightWagon, image=self.imgWagon, anchor="nw")
            self.imgsOnCanvasPlaySpace.append(img)

        #queue
        img = self.playSpace.create_image((NB_WAGONS +1)*widthWagon, heightWagon, image=self.imgQueue, anchor="nw")
        self.imgsOnCanvasPlaySpace.append(img)

        #FIN === ON DESSINE LES WAGONS =====================



        #ON DESSINE LES BANDITS ============================
        #les Offset permet de placer un personnage au centre du wagon
        xOffsetCharacter = widthWagon + (widthWagon//2) - (widthCharacter//2)
        yOffsetCharacter = (heightWagon-heightCharacter) - (heightWagon * 0.3) #hauteaur à l'intérieur du wagon


        for wagon in Game.wagons:
            nbBandits = len(wagon.bandits)

            if nbBandits == 0:
                continue

            # for i, bandit in enumerate(wagon.bandits):
            for i in range(nbBandits):
                bandit = wagon.bandits[i]

                xBanditPosition = bandit.position['x']
                yBanditPosition = bandit.position['y']
                xOffsetBandit = xOffsetCharacter
                yOffsetBandit = yOffsetCharacter

                #décalage selon le nombre de bandits dans le même wagon
                if (i % 2) == 1:
                    xOffsetBandit += ((widthWagon // nbBandits) + ((i * (widthWagon // nbBandits)))) // 4

                else:
                    xOffsetBandit -= ((widthWagon // nbBandits) + ((i * (widthWagon // nbBandits)))) // 4


                #décalage selon l'étage
                if yBanditPosition == 0: #sur le toit
                    yOffsetBandit += heightWagon*0.4
                    yOffsetBandit -= (heightWagon*0.01) * (i%3)
                if yBanditPosition == 1: #dans le wagon
                    yOffsetBandit -= (heightWagon*0.01) * (i%3) #réhaussement de 1% * 0 ou 1 ou 2


                xImgPosition = (xBanditPosition * widthWagon) + xOffsetBandit
                yImgPosition = (yBanditPosition * heightWagon) + yOffsetBandit

                bandit.img = Game.createBanditPng(widthCharacter, heightCharacter, COLORS[bandit.color])
                img = self.playSpace.create_image(xImgPosition, yImgPosition, image=bandit.img, anchor="nw")
                self.imgsOnCanvasPlaySpace.append(img)

        #FIN === ON DESSINE LES BANDITS ======================



        #ON DESSINE LE MARSHALL ==============================
        self.imgMarshal = Game.createLoadedImg(widthCharacter,heightCharacter, Game.imgMarshall)

        for wagon in self.wagons :
            if wagon.marshall == True:
                xOffsetMarshall = xOffsetCharacter
                yOffsetMarshall = yOffsetCharacter #réhaussement de 20%

                xMarshallPosition = (wagon.xPosition * widthWagon) + xOffsetMarshall
                yMarshallPosition = heightWagon + yOffsetMarshall


                img = self.playSpace.create_image(xMarshallPosition, yMarshallPosition, image=self.imgMarshal, anchor="nw")
                self.imgsOnCanvasPlaySpace.append(img)
                break
    
        # FIN === ON DESSINE LE MARSHALL ======================
                    


        #ON DESSINE LES BUTINS DANS LES WAGONS ==============================
        
        for wagon in self.wagons:
            # print(wagon.xPosition)
            # print()
            nbButins = len(wagon.butins)
            for i,butin in enumerate(wagon.butins) :
                xOffsetButin = xOffsetCharacter + widthButin
                yOffsetButin = heightWagon   
                if butin.position['y'] == 'toit':
                    yOffsetButin =  heightButin
                # print(butin.type)
                # print()
                if butin.type == 'magot':
                    butin.img=  Game.createLoadedImg(widthButin,heightButin, self.imgMagot)
                elif butin.type == 'bijoux' : 
                    butin.img=  Game.createLoadedImg(widthButin,heightButin, self.imgBijoux) 
                else:
                    butin.img=  Game.createLoadedImg(widthButin,heightButin, self.imgBourse)  
                
                if (i % 2) == 1: #permet de décaler les bandit les uns des autres
                    xOffsetButin += ((widthWagon //nbButins) + ((i * (widthWagon // nbButins)))) // 8

                else:
                    xOffsetButin -= ((widthWagon // nbButins) + ((i * (widthWagon // nbButins)))) // 8
                img = self.playSpace.create_image((wagon.xPosition * widthWagon) + xOffsetButin , heightCharacter+yOffsetButin, image = butin.img, anchor="nw")
                self.imgsOnCanvasPlaySpace.append(img)

        # FIN === ON DESSINE LES BUTINS DANS LES WAGONS ======================



    @staticmethod
    def createLoadedImg(width, height, loadedImg):
        loadedImg = loadedImg.resize((width, height))
        return ImageTk.PhotoImage(loadedImg)


    @staticmethod
    def createBanditPng(width, height, color):
        body = Game.imgBody.resize((width, height))
        details = Game.imgDetails.resize((width, height))

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
    butinTypes = ['bourse', 'bijoux'] #'magot' only apply for type == 'loco'


    def __init__(self, game:Game, x:int, type:str, marshall:bool=None):
        self.xPosition = x
        self.marshall = False
        self.type = type #'loco' ou 'wagon' or 'queue'
        self.bandits = []
        self.butins = []


        if LOAD_SAVE: #load from a save
            self.marshall = marshall

        else:
            #replissage de butins, en fonction de type
            if self.type == 'loco':
                self.butins.append(Butin(game, 'magot', self.xPosition))

            else:
                for i in range(random.randint(1, 4)):
                    self.butins.append(Butin(game, random.choice(Wagon.butinTypes), self.xPosition))























class Bandit():
    def __init__(self, game:Game, name:str, color:str, position:tuple[int]=None, actions:list[str]=None, bullets:int=None):
        self.name = name
        self.color = color
        self.position = {'x':NB_WAGONS, 'y':1} #x => index du wagon dans Game.wagons, y => position dans le wagon(0=toit, 1=intérieur)
        self.actions = [] #action = 'right', 'left', 'up', 'down', 'shoot' or 'rob'
        self.game = game
        self.img = None
        self.butins = []
        self.bullets = MAX_BULLETS



        if not LOAD_SAVE:
            #on ajoute le bandit dans la liste bandits du bon wagon (en queue de train)
            self.game.wagons[NB_WAGONS].bandits.append(self)

        else: #load from save
            self.position['x'] = position[0]
            self.position['y'] = position[1]
            self.actions = actions
            self.bullets = bullets
            self.game.wagons[self.position['x']].bandits.append(self)




    def testRandomAction(self):
        if not len(self.actions):
            act = ['right', 'left', 'up', 'down', 'shoot', 'rob']
            self.actions.append(random.choice(act))
        self.executeAction()



    #execute the action at index 0 in self.actions
    def executeAction(self):
        if not len(self.actions):
            self.game.insertTextInLog(f"{self.name} has no actions\n")
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
                self.game.insertTextInLog(f"{banditName} can't move {action}\n")
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
                self.game.insertTextInLog(f"{banditName} can't move {action}\n")
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
                self.game.insertTextInLog(f"{banditName} can't move {action}\n")
                return
            self.position['y'] = 0

        if action == 'down':
            if yBanditPosition == 1:
                self.game.insertTextInLog(f"{banditName} can't move {action}\n")
                return
            self.position['y'] = 1


        self.game.insertTextInLog(f"{self.name} has moved {action}\n")

        self.checkForButin()



    def checkMarshallPresence(self):
        #si le bandit est sur le toit
        if self.position['y'] == 0:
            return

        #si le Marshall est dans le même wagon
        if self.game.wagons[self.position['x']].marshall == True:
            self.getHitByMarshall()



    #tire sur un Bandit, aléatoirement, à la même position
    def shoot(self):
        self.game.insertTextInLog(f"{self.name} prepare to shoot\n")

        if self.bullets == 0:
            self.game.insertTextInLog(f"{self.name} has no more bullets\n")
            return


        nb_targets = 0

        #on compte le nombre de cible possible (nombre de bandit dans le même wagon ET au même étage)
        for bandit in self.game.wagons[self.position['x']].bandits:
            if bandit.name == self.name:
                continue

            if bandit.position['y'] == self.position['y']:
                nb_targets += 1

        if nb_targets == 0:
            self.game.insertTextInLog(f"{self.name} has no targets to shoot\n")
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
        self.game.insertTextInLog(f"{self.name} rob\n")

        wagon = self.game.wagons[self.position['x']]

        if len(wagon.butins) == 0:
            self.game.insertTextInLog(f"There is no loot here\n")
            return

        if self.position['y'] == 0:
            self.game.insertTextInLog(f"You have to be inside the wagon to rob\n")
            return

        robbedButin = wagon.butins.pop(len(wagon.butins) - 1)
        self.butins.append(robbedButin)
        robbedButin.bracable = False
        robbedButin.position['y'] = self.name
        self.game.insertTextInLog(f"{self.name} robbed {robbedButin.type}({robbedButin.value})\n")



    #perd un butin, aléatoirement
    def getHitByBandit(self, ennemyName:str):
        self.game.insertTextInLog(f"{self.name} get hit by {ennemyName}\n")


        if len(self.butins) == 0: #le bandit n'a pas de butins
            return

        #on retire un butin du bandit, aléatoirement
        lostButin = self.butins.pop(random.randint(0, len(self.butins) - 1))
        if self.position['y'] == 0:
            lostButin.position['y'] = 'out'
        elif self.position['y'] == 1:
            lostButin.position['y'] = 'int'
        #qu'on rajoute dans la liste butins du wagon du bandit
        self.game.wagons[self.position['x']].butins.append(lostButin)
        self.game.insertTextInLog(f"{self.name} lost {lostButin.type}({lostButin.value})\n")



    #perd un butin, aléatoirement, et monte sur le toit
    def getHitByMarshall(self):
        self.game.insertTextInLog(f"{self.name} get hit by the Marshall\n")


        if len(self.butins):
            #on retire un butin du bandit
            lostButin = self.butins.pop(random.randint(0, len(self.butins) - 1))

            if self.position['y'] == 0:
                lostButin.position['y'] = 'out'
            elif self.position['y'] == 1:
                lostButin.position['y'] = 'int'

            #qu'on rajoute dans le wagon
            self.game.wagons[self.position['x']].butins.append(lostButin)
            self.game.insertTextInLog(f"{self.name} lost {lostButin.type}({lostButin.value})\n")

        #le bandit monte sur le toit
        self.position['y'] = 0
        self.game.insertTextInLog(f"{self.name} move on the roof\n")


    def checkForButin(self):
        wagon = self.game.wagons[self.position['x']]

        for i, butin in enumerate(wagon.butins):
            if butin.bracable == False:
                if self.position['x'] == wagon.xPosition: 
                    robbedButin = wagon.butins.pop(i)
                    self.butins.append(robbedButin)
                    self.game.insertTextInLog(f"{self.name} got {robbedButin.type}({robbedButin.value})\n")




    def butinAtSamePosition(self, butin):
        pos:str = butin.position['y']

        if pos == 'out' and self.position['y'] == 0:
            return True
        if pos == 'int' and self.position['y'] == 1:
            return True

        return False


























class Butin():
    lootValues = {'bourse':[100,200], 'bijoux' : [500], 'magot' : [1000]}

    def __init__(self, game:Game, type:str, x:int, value:int=None, position:tuple[int|str]=None, bracable:bool=None):
        self.game = game
        self.type = type
        self.value = random.choice(Butin.lootValues[type])
        self.position = {'x':x, 'y':'in'} #y = 'in' or 'out' or '{banditName}'
        # self.inOut = 1 #1 = interieur,0 = toit
        self.bracable = True
        self.img = None

        if LOAD_SAVE: #load from save
            self.value = value
            self.position['x'] = position[0]
            self.position['y'] = position[1]
            self.bracable = bracable

        self.game.butins.append(self)



























mon_jeu = Game()

mon_jeu.mainloop()
