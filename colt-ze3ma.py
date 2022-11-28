import random 
from tkinter import * #pour générer une fenêtre et son contenu
from PIL import Image, ImageTk #pour l'import et la modification d'images


global NB_WAGONS
global NB_ACTIONS 
global NB_JOUEURS 
global NB_BALLES
NB_WAGONS = 4
NB_JOUEURS = NB_WAGONS




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


        self.btnAction = Button(self.frame, text="Action", command=self.moveMarshall)
        self.btnAction.grid(row=5, column=1, padx=5, pady=10, sticky="news")

        self.btnRight = Button(self.frame, text="->")
        self.btnRight.grid(row=1, column=2, rowspan=2, sticky="news")
        self.btnLeft = Button(self.frame, text="<-")
        self.btnLeft.grid(row=1, column=0, rowspan=2, sticky="news")
        self.btnUp = Button(self.frame, text="Up")
        self.btnUp.grid(row=0, column=1, sticky="news")
        self.btnDown = Button(self.frame, text="Down")
        self.btnDown.grid(row=3, column=1, sticky="news")

        self.btnShoot = Button(self.frame, text="Shoot", command=self.testBanditActions)
        self.btnShoot.grid(row=1, column=1, sticky="news")
        self.btnSteal = Button(self.frame, text="Steal")
        self.btnSteal.grid(row=2, column=1, sticky="news")

        self.history = Label(self.menuSpace, text = "EMPTY\nHistory")
        self.history.grid(row=7, column=0, columnspan=3, sticky="news")

        #=== FIN MENU SPACE ================================



        #création des bandits
        for i in range(NB_JOUEURS):
            name = "Bandit " + str(i + 1)
            Game.bandits.append(Bandit(self.playSpace, name, (255, 255, 0, 0)))


        #ajout du marshall
        self.wagons[0].marshall = True
        # self.printPosMarshall()

        #resize des images de self.playSpace lorsque la fenêtre est redimentionnée
        self.playSpace.bind('<Configure>', lambda e: self.resize_image())


    def testBanditActions(self):
        for bandit in Game.bandits:
            bandit.test()
        print()


    def resize_image(self):
            #oum: j'ai mis en commentaire cette ligne pk ça beug
            #self.update()

            for img in self.imgsOnPlaySpace:
                self.playSpace.delete(img)

            self.imgsOnPlaySpace.clear()

            hauteur=self.playSpace.winfo_height()
            largeur=self.playSpace.winfo_width()



            # self.pay = createImg(largeur, hauteur, "png/landscape.png")
            self.imgPaysage = createLoadedImg(largeur, hauteur, Game.imgPaysage)
            img = self.playSpace.create_image(0, 0, image=self.imgPaysage, anchor="nw")
            self.imgsOnPlaySpace.append(img)
            # return


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
        print()




class Wagon():
    imgLoco = Image.open('png/locomotive val.png')
    imgWagon = Image.open('png/wagon val.png')
    imgQueue = Image.open('png/queue val.png')

    #tetewagonqueue est un entier entre 0 et 2, 0=loco, 1=wagon, 2=queue
    # def __init__(self, game:Game, playSpace:Canvas , y:int, tetewagonqueue:int):
    def __init__(self, game:Game, y:int, type:str):
        # self.y = y
        self.marshall = False
        self.type = type

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

    def __init__(self, playSpace:Canvas, name:str, color:tuple):
        self.name = name
        self.color = color
        self.position = (0, NB_WAGONS)
        self.actions = [] #comment on décrit une action ? (ex: 0=droite, ...5 = tirer) (ex: "droite"=droite, "tire"=tire)
        self.marshall = 0 #je pense que c'est pas nécessaire (Valentin)


    def test(self):
        act = ['right', 'left', 'up', 'down', 'shoot', 'rob']
        self.actions.append(random.choice(act))
        self.executeAction()


    def executeAction(self):
        if not len(self.actions):
            print(f'{self.name} has no actions')
            return
        
        if self.actions[0] in ['right', 'left', 'up', 'down']:
            self.deplacement()
        elif self.actions[0] == 'shoot':
            self.shoot()
        elif self.actions[0] == 'rob':
            self.rob()

        #self.getHitByBandit()
        #self.gedHitByMarshall()

        self.actions.pop(0)


    def deplacement(self):
        print(f'{self.name} move to {self.actions[0]}')


    def shoot(self):
        #tire sur un Bandit, aléatoirement, à la même position (aka, appeler la fonction getHit() du Bandit touché)
        print(f'{self.name} shoot')


    def rob(self):
        #vole un butin, aléatoirement, sur sa position
        print(f'{self.name} rob')


    def getHitByBandit(self):
        #perd un butin, aléatoirement
        print(f'{self.name} get hit by a bandit')


    def getHitByMarshall(self):
        #perd un butin, aléatoirement, et monte sur le toit
        print(f'{self.name} get hit by the Marshall')









mon_jeu = Game()





mon_jeu.mainloop()


