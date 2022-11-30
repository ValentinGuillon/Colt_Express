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
    imgsOnPlaySpace = [] # liste d'entiers (représentant les images sur un Canvas)
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

        self.frame = Frame(self.menuSpace, width= 400, height= 100)

        #boutons
        self.btnAction = Button(self.frame, text="(testActions)", command=self.testActions)
        self.btnRight = Button(self.frame, text="->")
        self.btnLeft = Button(self.frame, text="<-")
        self.btnUp = Button(self.frame, text="Up")
        self.btnDown = Button(self.frame, text="Down")
        self.btnShoot = Button(self.frame, text="Shoot")
        self.btnSteal = Button(self.frame, text="(print Bandits of\nall wagons)", command=self.printBanditsOfAllWagons)

        #actions history
        self.history = Label(self.menuSpace, text = "EMPTY\nHistory")

        #placement des widgets
        self.frame.grid(row=0,column=0,sticky='nsew')
        self.btnAction.grid(row=5, column=1, padx=5, pady=10, sticky="news")
        self.btnRight.grid(row=1, column=2, rowspan=2, sticky="news")
        self.btnLeft.grid(row=1, column=0, rowspan=2, sticky="news")
        self.btnUp.grid(row=0, column=1, sticky="news")
        self.btnDown.grid(row=3, column=1, sticky="news")
        self.btnShoot.grid(row=1, column=1, sticky="news")
        self.btnSteal.grid(row=2, column=1, sticky="news")
        self.history.grid(row=7, column=0, columnspan=3, sticky="news")

        #=== FIN MENU SPACE ================================


        #création des bandits
        for i in range(NB_JOUEURS):
            name = "Bandit" + str(i + 1)
            color = random.choice(list(COLORS.values()))
            Game.bandits.append(Bandit(self, name, color))


        #ajout du marshall
        self.wagons[0].marshall = True


        #resize des images de l'interface lorsque la fenêtre est redimensionnée
        self.playSpace.bind('<Configure>', lambda e: self.resize_image())




    def testActions(self):
        #execute l'action de chaque bandit (donnée aléatoirement)
        print("Execute first action of each bandit :")
        for bandit in Game.bandits:
            bandit.test()
        print()

        #update du Canvas
        self.resize_image()

        self.after(ms=100, func=self.testaled)


    def testaled(self):
        #verifie pour chaque bandit s'il le Marshall est au même endroit (déplace le bandit si oui)
        for bandit in Game.bandits:
            bandit.checkMarshallPresence()
        print()
        
        #update du Canvas
        self.resize_image()

        self.after(ms=500, func=self.test2)


    def test2(self):
        #déplace le marshall
        self.moveMarshall()

        #update du Canvas
        self.resize_image()

        self.after(ms=100, func=self.test3)
        

    def test3(self):
        #verifie pour chaque bandit s'il le Marshall est au même endroit (déplace le bandit si oui)
        for bandit in Game.bandits:
            bandit.checkMarshallPresence()
        print()

        #update du Canvas
        self.resize_image()

 


    #affiche le bool "marshall" de chaque wagon
    def printPosMarshall(self):
        print("Position du Marshall")
        for wagon in self.wagons:
            print(wagon.marshall, end=" ")
        print('\n')


    def printBanditsOfAllWagons(self): #à supprimer
        print("Bandits de chaque wagon :")
        for i, wagon in enumerate(Game.wagons):
            print(f'wagon {i} => ', end='')
            for bandit in wagon.bandits:
                print(f"({bandit.name}:{bandit.position['y']})", end=' ')
            print()
        print()




    def resize_image(self):
            #oum: j'ai mis en commentaire cette ligne pk ça beug
            #self.update()

            #ON VIDE LE CANVAS ===================================
            for img in self.imgsOnPlaySpace:
                self.playSpace.delete(img)
            self.imgsOnPlaySpace.clear()

            #ON DÉFINI LES TAILLES DE TOUTES LES IMAGES ==========
            #taille du Canvas
            hauteur=self.playSpace.winfo_height()
            largeur=self.playSpace.winfo_width()
            #taille d'un Wagon
            w = int(largeur / (NB_WAGONS+1))
            h = int(hauteur / 3)
            #taille du marshall
            wMarshall = int(w * 0.4)
            hMarshall = h//2
            #taille des Bandit
            wBandit = int(w * 0.4)
            hBandit = h//2



            #ON DESSINE LE BACKGROUND ============================
            self.imgPaysage = Game.createLoadedImg(largeur, hauteur, Game.imgPaysage)
            img = self.playSpace.create_image(0, 0, image=self.imgPaysage, anchor="nw")
            self.imgsOnPlaySpace.append(img)



            #ON DESSINE LES WAGONS ==============================
            self.imgLoco = Game.createLoadedImg(w, h, Wagon.imgLoco)
            self.imgWagon = Game.createLoadedImg(w, h, Wagon.imgWagon)
            self.imgQueue = Game.createLoadedImg(w, h, Wagon.imgQueue)
            
            #loco
            img = self.playSpace.create_image(0, h, image=self.imgLoco, anchor="nw")
            self.imgsOnPlaySpace.append(img)
            
            #wagon
            for i in range(1, NB_WAGONS):
                img = self.playSpace.create_image(i*w, h, image=self.imgWagon, anchor="nw")
                self.imgsOnPlaySpace.append(img)

            #queue
            img = self.playSpace.create_image(NB_WAGONS*w, h, image=self.imgQueue, anchor="nw")
            self.imgsOnPlaySpace.append(img)

            #FIN === ON DESSINE LES WAGONS =====================



            #ON DESSINE LES BANDITS ============================
            baseOffSetX = (w//2) - (wBandit//2)
            baseOffSetY = (h-hBandit)

            for wagon in Game.wagons:
                nbBandits = len(wagon.bandits)

                if nbBandits == 0:
                    continue

                for i, bandit in enumerate(wagon.bandits):
                    x = bandit.position['x']
                    y = bandit.position['y']
                    offSetX = baseOffSetX
                    offSetY = baseOffSetY

                    #faire deux cas de calcul des offSet, pour y == 0, et y == 1
                    #faire un cas spécial pour x == 0 (locomotive)

                    if (i % 2) == 1: #permet de décaler les bandit les uns des autres
                        offSetX += ((w // nbBandits) + ((i * (w // nbBandits)))) // 4

                    else:
                        offSetX -= ((w // nbBandits) + ((i * (w // nbBandits)))) // 4


                    if y == 1: #si le Bandit est à l'intérieur du train
                        offSetY -= h*0.2 #réhaussement de 20% de la hauteur du train
                        offSetY -= (h*0.02) * (i%3)
                    

                    bandit.img = Game.createBanditPng(wBandit, hBandit, bandit.color)
                    img = self.playSpace.create_image((x*w)+offSetX, (y*h)+offSetY, image=bandit.img, anchor="nw")
                    self.imgsOnPlaySpace.append(img)

            #FIN === ON DESSINE LES BANDITS ======================
                    


            #ON DESSINE LE MARSHALL ==============================
            self.imgMarshal = Game.createLoadedImg(wMarshall,hMarshall, self.imgMarshall)
            
            base__OffSetX = (w//2) - (wMarshall//2)
            base__OffSetY = (h-hMarshall)
            
            i = 2
            for i, wagon in enumerate(self.wagons) :
                if wagon.marshall == True:
                    img = self.playSpace.create_image(((i*w)+base__OffSetX), (h * 0.8)+base__OffSetY, image=self.imgMarshal, anchor="nw")
                    self.imgsOnPlaySpace.append(img)
                    break
        
            # FIN === ON DESSINE LE MARSHALL ======================



    @staticmethod
    def createLoadedImg(x, y, img):
        img = img.resize((x, y))
        return ImageTk.PhotoImage(img)


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
        i = 0 #position du wagon où se trouve le Marshall
        for wagon in self.wagons:
            if wagon.marshall == True:
                
                break
            i += 1

        #Marshall en tête de train
        if i == 0:
            self.wagons[i].marshall = False
            i += 1
            self.wagons[i].marshall = True
            
        #Marshall en queue de train
        elif i == NB_WAGONS:
            self.wagons[i].marshall = False
            i -= 1
            self.wagons[i].marshall = True

        #Marshall ni en tête/queue du train, donc on le déplace aléatoirement
        elif (random.randint(0,1)):
            self.wagons[i].marshall = False
            i -= 1
            self.wagons[i].marshall = True

        else:
            self.wagons[i].marshall = False
            i += 1
            self.wagons[i].marshall = True























class Wagon():
    imgLoco = Image.open('png/locomotive val.png')
    imgWagon = Image.open('png/wagon val.png')
    imgQueue = Image.open('png/queue val.png')

    butinTypes = ['bourse', 'bijoux'] #'magot' only apply for type == 'loco'


    def __init__(self, game:Game, x:int, type:str):
        self.x = x
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
        self.game.wagons[self.position['x']].bandits.append(self)



    def test(self):
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
        x = self.position['x']
        y = self.position['y']
        name = self.name

        if action == 'right':
            if x == NB_WAGONS:
                print(f"{name} can't move {action}")
                return

            #on retire le bandit du wagon actuel
            for i, bandit in enumerate(self.game.wagons[x].bandits):
                if not bandit.name == name:
                    continue
                self.game.wagons[x].bandits.pop(i)

            #on ajoute le bandit dans le wagon destination
            self.game.wagons[x+1].bandits.append(self)

            self.position['x'] += 1


        if action == 'left':
            if x == 0:
                print(f"{name} can't move {action}")
                return

            #on retire le bandit du wagon actuel
            for i, bandit in enumerate(self.game.wagons[x].bandits):
                if not bandit.name == name:
                    continue
                self.game.wagons[x].bandits.pop(i)

            #on ajoute le bandit dans le wagon destination
            self.game.wagons[x-1].bandits.append(self)

            self.position['x'] -= 1


        if action == 'up':
            if y == 0:
                print(f"{name} can't move {action}")
                return
            self.position['y'] = 0

        if action == 'down':
            if y == 1:
                print(f"{name} can't move {action}")
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
    def getHitByBandit(self, ennemy:str):
        print(f'{self.name} get hit by {ennemy}')


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
            lostButin = self.butins.pop(random.randint(0, len(self.butins)  - 1))
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
        self. value = random.choice(Butin.lootValues[type])
        self.inOut = 1 #0 = interieur, 1 = toit
        self.bracable = True























mon_jeu = Game()

mon_jeu.mainloop()
