import random 
from tkinter import * #pour générer une fenêtre et son contenu
from PIL import Image, ImageTk #pour l'import et la modification d'images


global NB_WAGONS
global NB_ACTIONS 
global NB_JOUEURS 
global MAX_BULLETS
NB_JOUEURS = 4
NB_WAGONS = NB_JOUEURS
MAX_BULLETS = (NB_JOUEURS // 2) + 1


global colors
colors = {"red":(255, 0, 0),
          "orange":(255, 128, 0),
          "yellow":(255, 255, 0),
          "green":(0, 255, 0),
          "blue":(0, 0, 255)}



# def createImg(x, y, file):
#     img = Image.open(file)
#     img = img.resize((x, y))
#     return ImageTk.PhotoImage(img)

def createLoadedImg(x, y, img):
    img = img.resize((x, y))
    return ImageTk.PhotoImage(img)


class Game(Tk):
    imgPaysage = Image.open("png/landscape.png")
    imgsOnPlaySpace = []
    wagons = []
    bandits = []

    def __init__(self):
        super().__init__()
        self.title("Colt Zeʁma")
        # self.geometry("720x480")
        self["bg"] = "orange"
        icon = './train.ico'
        img = Image.open(icon)
        img = ImageTk.PhotoImage(img)
        self.call('wm', 'iconphoto', self._w, img)

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight=1)



        #attention, il doit y avoir deux espaces, un pour le jeu (train, décor), et un pour le "menu"
        self.playSpace = Canvas(self, bg="blue")
        self.playSpace.grid(row = 0, column= 0, sticky='nsew')

        self.menuSpace = Canvas(self, bg="red")
        self.menuSpace.grid(row = 0, column= 1, sticky='nsew')



        #=== PLAY SPACE ====================================
        #chargement du background
        #le décor derrière le train
        # self.paysage = createImg(100*(NB_WAGONS + 1), 100*4, "png/landscape.png")
        # img = self.playSpace.create_image(0, 0, image=self.paysage, anchor="nw")
        # self.imgsOnPlaySpace.append(img)


        #création des wagons
        for y in range(NB_WAGONS + 1):
            #loco
            if y == 0:
                # self.wagons.append(Wagon(self, self.playSpace, y, 0))
                self.wagons.append(Wagon(self, y, type='loco'))
                continue
            #queue
            if y == NB_WAGONS:
                # self.wagons.append(Wagon(self, self.playSpace, y, 2))
                self.wagons.append(Wagon(self, y, type='wagon'))
                continue
            #wagon
            # self.wagons.append(Wagon(self, self.playSpace, y, 1))
            self.wagons.append(Wagon(self, y, type='queue'))



        #=== FIN PLAY SPACE ================================


        #=== MENU SPACE ====================================
        self.menuSpace.rowconfigure(0, weight=1)
        self.menuSpace.columnconfigure(0, weight=1)
        # grille de x = 3, y = 4+1+1+?
        self.frame = Frame(self.menuSpace, width= 400, height= 100)
        self.frame.grid(row=0,column=0,sticky='nsew')


        self.btnAction = Button(self.frame, text="Action\n(testActions)", command=self.testActions)
        self.btnAction.grid(row=5, column=1, padx=5, pady=10, sticky="news")

        self.btnRight = Button(self.frame, text="->")
        self.btnRight.grid(row=1, column=2, rowspan=2, sticky="news")
        self.btnLeft = Button(self.frame, text="<-")
        self.btnLeft.grid(row=1, column=0, rowspan=2, sticky="news")
        self.btnUp = Button(self.frame, text="Up")
        self.btnUp.grid(row=0, column=1, sticky="news")
        self.btnDown = Button(self.frame, text="Down")
        self.btnDown.grid(row=3, column=1, sticky="news")

        self.btnShoot = Button(self.frame, text="Shoot")
        self.btnShoot.grid(row=1, column=1, sticky="news")
        self.btnSteal = Button(self.frame, text="Steal\n(print Bandits of\nall wagons)", command=self.printBanditsOfAllWagons)
        self.btnSteal.grid(row=2, column=1, sticky="news")

        self.history = Label(self.menuSpace, text = "EMPTY\nHistory")
        self.history.grid(row=7, column=0, columnspan=3, sticky="news")

        #=== FIN MENU SPACE ================================



        #création des bandits
        for i in range(NB_JOUEURS):
            name = "Bandit" + str(i + 1)
            color = random.choice(list(colors.values()))
            Game.bandits.append(Bandit(self, name, color))


        #ajout du marshall
        self.wagons[0].marshall = True
        # self.printPosMarshall()

        #resize des images de self.playSpace lorsque la fenêtre est redimentionnée
        self.playSpace.bind('<Configure>', lambda e: self.resize_image())


    def testActions(self):
        #execute l'action de chaque bandit (donnée aléatoirement)
        print("Execute first action of each bandit :")
        for bandit in Game.bandits:
            bandit.test()
        print()

        #déplace le marshall
        self.moveMarshall()

        #verifie pour chaque bandit s'il le Marshall est au même endroit (déplace le dbandit si oui)
        for bandit in Game.bandits:
            bandit.checkMarshallPresence()
        print()

        #update du Canvas
        self.resize_image()

        
    def printBanditsOfAllWagons(self):
        print("list Bandits de chaque wagon :")
        for i, wagon in enumerate(Game.wagons):
            # print(f'wagon{i} => {wagon.bandits}')
            print(f'wagon {i} => [', end='')
            for bandit in wagon.bandits:
                print(f'{bandit.name}', end=' ')
            print(']')
        print()


    def resize_image(self):
            #oum: j'ai mis en commentaire cette ligne pk ça beug
            #self.update()

            #ON VIDE LE CANVAS ========================
            for img in self.imgsOnPlaySpace:
                self.playSpace.delete(img)
            self.imgsOnPlaySpace.clear()

            #ON RÉCUPÈRE LA TAILLE DU CANVAS ==========
            hauteur=self.playSpace.winfo_height()
            largeur=self.playSpace.winfo_width()


            #ON DESSINE LE BACKGROUND =================
            # self.pay = createImg(largeur, hauteur, "png/landscape.png")
            self.imgPaysage = createLoadedImg(largeur, hauteur, Game.imgPaysage)
            img = self.playSpace.create_image(0, 0, image=self.imgPaysage, anchor="nw")
            self.imgsOnPlaySpace.append(img)


            #ON DESSINE LES WAGONS ====================
            w = int(largeur / (NB_WAGONS+1))
            h = int(hauteur / 3)
            # print(w, h)

            # self.loco = createImg(w, h, "png/locomotive val.png")
            # self.wagon = createImg(w, h, "png/wagon val.png")
            # self.queue = createImg(w, h, "png/queue val.png")
            self.imgLoco = createLoadedImg(w, h, Wagon.imgLoco)
            self.imgWagon = createLoadedImg(w, h, Wagon.imgWagon)
            self.imgQueue = createLoadedImg(w, h, Wagon.imgQueue)
 

            # self.train.wagons[0].config(image = loco)
            # self.train.wagons[0].image = loco

            img = self.playSpace.create_image(0, h, image=self.imgLoco, anchor="nw")
            self.imgsOnPlaySpace.append(img)

            for i in range(1, NB_WAGONS):
                # self.train.wagons[i].config(image = wagon)
                # self.train.wagons[i].image = wagon
                img = self.playSpace.create_image(i*w, h, image=self.imgWagon, anchor="nw")
                self.imgsOnPlaySpace.append(img)

            # self.train.wagons[NB_WAGONS].config(image = queue)
            # self.train.wagons[NB_WAGONS].image = queue
            img = self.playSpace.create_image(NB_WAGONS*w, h, image=self.imgQueue, anchor="nw")
            self.imgsOnPlaySpace.append(img)


            #ON DESSINE LES BANDITS ===================
            wBandit = int(w/2.7)
            hBandit = h//2
            #les offSet sont à modifier
            # offSetX = w//4 #doit être < w
            # offSetY = h//2 - (int(h*0.2)) #doit être < h
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

                    # #!!! offSetX est mal calculer
                    # offSetX += ((w//4)*(nbBandits*(i))) // 4 #doit être < w
                    # offSetX -= ((w//4)*(nbBandits*(i))) // 4 #doit être < w

                    
                    
                    if (i % 2) == 1:
                        offSetX += ((w // nbBandits) + ((i * (w // nbBandits)))) // 4

                    else:
                        offSetX -= ((w // nbBandits) + ((i * (w // nbBandits)))) // 4


                    if y == 1:
                        offSetY -= h*0.2 #réhaussement de 20% de la hauteur du train
                        offSetY -= (h*0.02) * (i%3)
                    

                        
                    bandit.img = Game.createBanditPng(wBandit, hBandit, bandit.color)
                    # img = self.playSpace.create_image((x*(w//2))+offSetX, (y*h)+offSetY, image=bandit.img, anchor="nw")
                    img = self.playSpace.create_image((x*w)+offSetX, (y*h)+offSetY, image=bandit.img, anchor="nw")
                    self.imgsOnPlaySpace.append(img)


            

    @staticmethod
    def createBanditPng(width, height, color):
        body = Bandit.imgBody.resize((width, height))
        details = Bandit.imgDetails.resize((width, height))
        
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

        self.printPosMarshall()


    #affiche le bool "marshall" de chaque wagon
    def printPosMarshall(self):
        print("Position du Marshall")
        for wagon in self.wagons:
            print(wagon.marshall, end=" ")
        print('\n')




class Wagon():
    imgLoco = Image.open('png/locomotive val.png')
    imgWagon = Image.open('png/wagon val.png')
    imgQueue = Image.open('png/queue val.png')

    #tetewagonqueue est un entier entre 0 et 2, 0=loco, 1=wagon, 2=queue
    # def __init__(self, game:Game, playSpace:Canvas , y:int, tetewagonqueue:int):
    def __init__(self, game:Game, x:int, type:str):
        self.x = x
        self.marshall = False
        self.type = type #'loco' ou 'wagon' or 'queue'
        self.bandits = []

        # taille = 100

        #chargement de la bonne image
        # if tetewagonqueue == 0:
        #     self.img = createImg(taille, taille, "png/locomotive val.png")
        # elif tetewagonqueue == 1:
        #     self.img = createImg(taille, taille, "png/wagon val.png")
        # elif tetewagonqueue == 2:
        #     self.img = createImg(taille, taille, "png/queue val.png")

        # #(valentin)
        # if type == 'loco':
        #     self.img = Image.open('png/locomotive val.png')
        # elif type == 'wagon':
        #     self.img = Image.open('png/wagon val.png')
        # elif type == 'queue':
        #     self.img = Image.open('png/queue val.png')



        # img = playSpace.create_image((y*taille, 2*taille), image=self.img, anchor="nw")
        # game.imgsOnPlaySpace.append(img)





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

        #on ajoute le bandit dans la liste bandits du bon wagon
        self.game.wagons[self.position['x']].bandits.append(self)


    def test(self):
        act = ['right', 'left', 'up', 'down', 'shoot', 'rob']
        self.actions.append(random.choice(act))
        self.executeAction()


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
        # self.checkMarshallPresence()

    
    def checkMarshallPresence(self):
        #si le bandit est sur le toit
        if self.position['y'] == 0:
            return

        #si le Marshall est dans le même wagon
        if self.game.wagons[self.position['x']].marshall == True:
            self.getHitByMarshall()


    def shoot(self):
        #tire sur un Bandit, aléatoirement, à la même position
        print(f'{self.name} shoot')

        if self.bullets == 0:
            print(f'{self.name} has no more bullets')
            return
        
        self.bullets -= 1
        nb_targets = 0

        #on compte le nombre de cible possible
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
            if target.position['y'] == self.position['y']:
                break

        target.getHitByBandit(self.name)
            


    def rob(self):
        #vole un butin, aléatoirement, sur sa position
        print(f'{self.name} rob')


    def getHitByBandit(self, ennemy:str):
        #perd un butin, aléatoirement
        print(f'{self.name} get hit by {ennemy}')

        if len(self.butins) == 0: #le bandit n'a pas de butins
            return
        
        #on retire un butin du bandit, aléatoirement
        butin = self.butins.pop(random.randint(len(self.butins)))
        #qu'on rajoute dans la liste butins du wagon du bandit
        self.game.wagons[self.position['x']].append(butin)


    def getHitByMarshall(self):
        #perd un butin, aléatoirement, et monte sur le toit
        print(f'{self.name} get hit by the Marshall')

        if len(self.butins):
            #on retire un butin du bandit
            butin = self.butins.pop(random.choice(list(range(len(self.butins)))))
            #qu'on rajoute dans le wagon
            self.game.wagons[self.position['x']].append(butin)
            print(f'{self.name} lose a butin')
        
        #le bandit monte sur le toit
        self.position['y'] = 0
        print(f'{self.name} move on the roof')








mon_jeu = Game()





mon_jeu.mainloop()


