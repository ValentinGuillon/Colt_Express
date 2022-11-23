import random 
from tkinter import *
from PIL import Image, ImageTk


global NB_WAGONS
global NB_ACTIONS 
global NB_JOUEURS 
global NB_BALLES
NB_WAGONS = 3
NB_JOUEURS = NB_WAGONS




class Game(Tk):
    def __init__(self):
        super().__init__()
        self.title("Colt Express")
        # self.geometry("720x480")
        self["bg"] = "orange"
        self.iconbitmap("./train.ico")

        
        #attention, il doit y avoir deux espaces, un pour le jeu (train, décor), et un pour le "menu"
        self.playSpace = Canvas(self, bg="blue")
        self.playSpace.pack(side="left")

        self.menuSpace = Canvas(self, bg="red")
        self.menuSpace.pack(side="left")


        
        #=== PLAY SPACE ====================================
        # self.playSpace.columnconfigure(0, weight = 3)
        # self.playSpace.columnconfigure(1, weight = 1)
        # self.playSpace.rowconfigure(0, weight=3)
        # self.playSpace.rowconfigure(1, weight=1)

        #background décor
        self.paysage = Image.open("png/paysage_2.png")
        self.paysage = self.paysage.resize((100*(NB_WAGONS + 1), 100*4))
        self.paysage = ImageTk.PhotoImage(self.paysage)

        self.paysageLb = Label(self.playSpace, image=self.paysage, border=0)

        self.paysageLb.grid(row=0, column=0, rowspan=3, columnspan=NB_WAGONS+1)


        #création du train
        self.train = Train(self.playSpace, 500, 750)
        self.train.grid(row = 1, column = 0, sticky =  'nsew')
        self.train.config(bg= "green")

        for i in range(NB_JOUEURS):
            self.train.rowconfigure(i, weight=1)
            self.train.columnconfigure(i, weight=1)

            
        #création des bandits
        self.bandits = []
        for i in range(NB_JOUEURS):
            name = "Bandit " + str(i + 1)
            self.bandits.append(Bandit(name))

            
        #ajout du marshall
        self.train.wagons[0].marshall = True

        #=== FIN PLAY SPACE ================================

        
        #=== MENU SPACE ====================================
        #grille de x = 3, y = 4+1+1+?
        self.btnAction = Button(self.menuSpace, text="Action").grid(row=5, column=1, padx=5, pady=10, sticky="news")

        self.btnRight = Button(self.menuSpace, text="->").grid(row=1, column=2, rowspan=2, sticky="news")
        self.btnLeft = Button(self.menuSpace, text="<-").grid(row=1, column=0, rowspan=2, sticky="news")
        self.btnUp = Button(self.menuSpace, text="Up").grid(row=0, column=1, sticky="news")
        self.btnDown = Button(self.menuSpace, text="Down").grid(row=3, column=1, sticky="news")

        self.btnShoot = Button(self.menuSpace, text="Shoot").grid(row=1, column=1, sticky="news")
        self.btnSteal = Button(self.menuSpace, text="Steal").grid(row=2, column=1, sticky="news")

        self.history = Label(self.menuSpace, text = "EMPTY\nHistory").grid(row=7, column=0, columnspan=3, sticky="news")

        #=== FIN MENU SPACE ================================


    # Pour le Marshall
    def deplacement(self):
        i = 0 #position du wagon où se trouve le Marshall
        for wagon in self.train:
            if wagon.marshall == True:
                break
            i += 1

        #on verifie si le Marshall est en tete ou en queue de train
        if i == 0:
            self.marshallMoveLeft()
            #return
        elif i == NB_WAGONS - 1:
            self.marshallMoveRight()
            #return


        #le marshall n'est pas en tête/queue du train, donc...
        if (random.randint(0,1)):
            self.marshallMoveLeft()
        else:
            self.marshallMoveRight()


    def marshallMoveLeft():
        pass

    def marshallMoveRight():
        pass



# class Train():
#     wagons = []
#     #Constructeur
#     def __init__(self):
#         # self.wm_attributes()

#         # #Créer les cases
#         # for x in range(2):
#         #     for y in range(NB_WAGONS):
#         #         #loco
#         #         if x == 0 and y == 0:
#         #             self.wagons.append(Wagon(self, x, y, 0))
#         #             isLoco = False
#         #             continue
#         #         #queue
#         #         if x == 1 and y == NB_WAGONS - 1:
#         #             self.wagons.append(Wagon(self, x, y, 2))
#         #             continue

#         #         #wagon
#         #         self.wagons.append(Wagon(self, x, y, 1))
        
#         #Créer les cases
#         for y in range(NB_WAGONS + 1):
#             #loco
#             if y == 0:
#                 self.wagons.append(Wagon(self, 2, y, 0))
#                 continue
#             #queue
#             if y == NB_WAGONS:
#                 self.wagons.append(Wagon(self, 2, y, 2))
#                 continue

#             #wagon
#             self.wagons.append


class Train(Canvas):
    wagons = []
    #Constructeur
    def __init__(self, fenetre:Tk, width, height):
        super().__init__(fenetre, width=width, height=height, bg='green', border=0)



        # self.wm_attributes()

        # #Créer les cases
        # for x in range(2):
        #     for y in range(NB_WAGONS):
        #         #loco
        #         if x == 0 and y == 0:
        #             self.wagons.append(Wagon(self, x, y, 0))
        #             isLoco = False
        #             continue
        #         #queue
        #         if x == 1 and y == NB_WAGONS - 1:
        #             self.wagons.append(Wagon(self, x, y, 2))
        #             continue

        #         #wagon
        #         self.wagons.append(Wagon(self, x, y, 1))
        
        #Créer les cases
        for y in range(NB_WAGONS + 1):
            #loco
            if y == 0:
                self.wagons.append(Wagon(self, 2, y, 0))
                continue
            #queue
            if y == NB_WAGONS:
                self.wagons.append(Wagon(self, 2, y, 2))
                continue

            #wagon
            self.wagons.append(Wagon(self, 2, y, 1))



#tetewagonqueue est un entier entre 0 et 2, 0=loco, 1=wagon, 2=queue
class Wagon(Label):
    def __init__(self, Train:Canvas, x , y, tetewagonqueue):
        super().__init__(Train, width=100, height=100, border=0)
        self.x = x
        self.y = y
        self.marshall = False
        self.grid(row=x, column=y, sticky= 'nsew')

        self["bg"] = "brown"



        #posage du png
        if tetewagonqueue == 0:
            self.img = self.drawImage("png/locomotive val.png")
        elif tetewagonqueue == 1:
            self.img = self.drawImage("png/wagon val.png")
        elif tetewagonqueue == 2:
            self.img = self.drawImage("png/queue val.png")

        # imgLb = Label(self, image=self.img)
        # imgLb.pack()
        self["image"] = self.img



    def drawImage(self, file):
        #train
        img = Image.open(file).convert('RGBA')
        img = img.resize((100, 100))
        
        #background
        background = Image.new('RGBA', img.size, (0, 0, 0, 0))

        #addition des deux
        newImg = Image.alpha_composite(background, img)


        return ImageTk.PhotoImage(newImg)






class Bandit(Label):
    def __init__(self, name):
        self.name = name
        self.position = (0, NB_WAGONS)
        self.actions = [] #comment on décrit une action ? (ex: 0=droite, ...5 = tirer) (ex: "droite"=droite, "tire"=tire)
        self.marshall = 0 #je pense que c'est pas nécessaire (Valentin)



    def deplacement(self):
        pass





mon_jeu = Game()


#Teste pour voir la position du Marshall
# print("position du Marshall")
# for wagon in mon_jeu.train.wagons:
#     print(int(wagon.marshall), end="")
# print()

#Test pour afficher le nom de chaque Bandit
# print("nom de chaque Bandit")
# for bandit in mon_jeu.bandits:
#     print(bandit.name)


mon_jeu.mainloop()
