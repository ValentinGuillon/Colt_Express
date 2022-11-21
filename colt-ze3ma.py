import random 
from tkinter import *
# from PIL import Image, ImageTk


global NB_WAGONS
global NB_ACTIONS 
global NB_JOUEURS 
global NB_BALLES
NB_WAGONS = 6
NB_JOUEURS = NB_WAGONS




class Game(Tk):
    def __init__(self):
        super().__init__()
        self.title("Colt Express")
        # self.geometry("720x480")
        self["bg"] = "orange"

        
        #attention, il doit y avoir deux espaces, un pour le jeu (train, décor), et un pour le "menu"
        self.playSpace = Canvas(self, bg="blue")
        self.playSpace.pack(side="left")

        self.menuSpace = Canvas(self, bg="green")
        self.menuSpace.pack(side="left")

        #le self sera donc remplacé par autre chose ici (qui sera un Canvas)
        self.playSpace.columnconfigure(0, weight = 3)
        self.playSpace.columnconfigure(1, weight = 1)
        self.playSpace.rowconfigure(0, weight=3)
        self.playSpace.rowconfigure(1, weight=1)

        #création du train
        self.train = Train(self.playSpace, 500, 750)
        self.train["bg"] = "orange"
        self.train.grid(row = 0, column = 0, sticky =  'nsew')

        # self.iconbitmap("./train.ico")


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



class Train(Canvas):
    wagons = []
    #Constructeur
    def __init__(self, fenetre:Tk, width, height):
        super().__init__(fenetre, width=width, height=height, bg='green')
        #Créer les cases
        isLoco = True
        for x in range(2):
            for y in range(NB_WAGONS):
                if isLoco:
                    self.wagons.append(Wagon(self, x, y, 0))
                    isLoco = False

                self.wagons.append(Wagon(self, x, y, 1))



#tetewagonqueue est un entier entre 0 et 2, 0=loco, 1=wagon, 2=queue
class Wagon(Canvas):
    def __init__(self, Train:Canvas, x , y, tetewagonqueue):
        super().__init__(Train, width=100, height=100, highlightbackground='red')
        self.x = x
        self.y = y
        self.marshall = False
        self.grid(row=x, column=y, sticky= 'nsew')



        #posage du png
        if tetewagonqueue == 0:
            #mette le png "locomotive"
            pass
        elif tetewagonqueue == 1:
            #mette le png "wagon"
            pass
        elif tetewagonqueue == 2:
            #mette le png "queue"
            pass









class Bandit(Canvas):
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
