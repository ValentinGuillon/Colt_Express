import random 

from tkinter import *

global NB_WAGONS
global NB_ACTIONS 
global NB_JOUEURS 
global NB_BALLES
NB_WAGONS = 6
NB_JOUEURS = NB_WAGONS
class Game(Tk):
    def __init__(self):
        super().__init__()
        self.train = Train(self, 500, 750)
        self.train.grid(row = 0, column = 0, sticky =  'nsew')
        self.columnconfigure(0, weight = 3) 
        self.columnconfigure(1, weight = 1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=1) 
        self.title("Colt Express ")
        self.geometry("720x480")
        self.iconbitmap("./train.ico")
        for i in range(NB_JOUEURS):
            self.train.rowconfigure(i, weight=1)
            self.train.columnconfigure(i, weight=1)
        self.bandits = []
    # Pour le Marshall     
    def deplecement(self):
        
        #! Cette fonction retourna une position aleatoire qui sera passé dans Train/ Wagon , pour verifié si le marshall y est ( Marshall = 1/True )
        
        #on verifie si le Marshall est en tete ou s*queue de train 
        #si pos == 0
            #Deplacer a droite
            #return
        #si pos == train[wagons-1]
            #Deplacer a gauche 
            #return
         
        if (random.randint(0,1)):
            
            #deplacement a gauche
            pass
        else:
            #deplacement a droite
            pass
class Train(Canvas):
    train = []
    #Constructeur 
    def __init__(self,fenetre : Tk, width, height):
        super().__init__(fenetre, width= width, height =height, bg='ivory')
        #Créer les cases
        for x in range(0, 2 ):
            for y in range(0, NB_JOUEURS):
                self.train.append(Wagon(self, x, y))
    pass


""" class Marshall():
    def __init__(self, position):
        self.position = position
        
    
    
    def deplecement(self):
        
        #on verifie si le Marshall est en tete ou s*queue de train 
        #si pos == 0
            #Deplacer a droite
            #return
        #si pos == train[wagons-1]
            #Deplacer a gauche 
            #return
         
        if (random.randint(0,1)):
            
            #deplacement a gauche
            pass
        else:
            #deplacement a droite
            pass
        """
        
        

class Bandit(Canvas):
    def __init__(self, name):
        self.name = name
        self.position = ()
        self.actions = []
        self.marshall = 0
        
    
    
    def deplecement(self):
        
        pass
        
        
        
class Wagon(Canvas):
    def __init__(self,Train:Canvas, x , y):
        super().__init__(Train, width=100, height=100, highlightbackground='ivory')
        self.x = x
        self.y = y
        self.marshall = False
        self.grid(row=x, column=y, sticky= 'nsew')       
        
mon_jeu = Game()


mon_jeu.mainloop()

