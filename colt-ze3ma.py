import random 
from tkinter import * #pour générer une fenêtre et son contenu
from PIL import Image, ImageTk #pour l'import et la modification d'images


global NB_WAGONS
global NB_ACTIONS 
global NB_JOUEURS 
global NB_BALLES
NB_WAGONS = 4
NB_JOUEURS = NB_WAGONS




class Game(Tk):
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
        # self.playSpace.rowconfigure(0, weight=1)
        # self.playSpace.rowconfigure(1, weight=1)
        # self.playSpace.rowconfigure(2, weight=1)

        #le décor derrière le train
        self.paysage = Game.createImg(100*(NB_WAGONS + 1), 100*4, "png/paysage_2.png")
        img = self.playSpace.create_image(0, 0, image=self.paysage, anchor="nw")
        self.imgsOnPlaySpace.append(img)
        
        # self.paysageLb = Label(self.playSpace, image=self.paysage, border=0)
        # self.paysageLb.grid(row=0, column=0, rowspan=3, columnspan=NB_WAGONS+1, sticky='nsew')

        # self.paysageLb.rowconfigure(0, weight=1)
        # self.paysageLb.columnconfigure(0, weight=1)

        #création du train
        # self.train = Train(self.playSpace, 500, 750)
        # self.train.grid(row = 1, column = 0, sticky =  'nsew', columnspan=NB_WAGONS+1)
        # self.train.config(bg= "green")


        #Créer les cases
        for y in range(NB_WAGONS + 1):
            #loco
            if y == 0:
                self.wagons.append(Wagon(self, self.playSpace, 2, y, 0))
                continue
            #queue
            if y == NB_WAGONS:
                self.wagons.append(Wagon(self, self.playSpace, 2, y, 2))
                continue

            #wagon
            self.wagons.append(Wagon(self, self.playSpace, 2, y, 1))


        # #oum : la condition d'arret pour la boucle est i = NB_WAGONS+1 
        # #sinon la cellule du dernier wagon ne s'adaptera pas à la taille de la fenetre
        # for i in range(NB_WAGONS+1):
        #     self.train.columnconfigure(i, weight=1)
        # #oum: On attribue un poids plus grand à la ligne qui contient le train
        # #Si toutes les lignes ont le même poids elles auront la meme taille 
        # #Et donc la ligne 2 ne pourra pas occuper plus d'espace que les autres lignes
        # #afin d'afficher les wagons
        # self.train.rowconfigure(2, weight=3)
            

        #=== FIN PLAY SPACE ================================

        
        #=== MENU SPACE ====================================
        self.menuSpace.rowconfigure(0, weight=1)
        self.menuSpace.columnconfigure(0, weight=1)
        # grille de x = 3, y = 4+1+1+?
        self.frame = Frame(self.menuSpace, width= 400, height= 100)
        self.frame.grid(row=0,column=0,sticky='nsew')

        
        self.btnAction = Button(self.frame, text="Action")
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
        self.btnSteal = Button(self.frame, text="Steal")
        self.btnSteal.grid(row=2, column=1, sticky="news")

        self.history = Label(self.menuSpace, text = "EMPTY\nHistory")
        self.history.grid(row=7, column=0, columnspan=3, sticky="news")

        #=== FIN MENU SPACE ================================

        

        # #création des bandits
        # self.bandits = []
        # for i in range(NB_JOUEURS):
        #     name = "Bandit " + str(i + 1)
        #     self.bandits.append(Bandit(name))

            
        #ajout du marshall
        self.wagons[0].marshall = True


        self.playSpace.bind('<Configure>', lambda e: self.resize_image())




    def resize_image(self):
            #oum: j'ai mis en commentaire cette ligne pk ça beug
            #self.update()
            print(self.imgsOnPlaySpace)
            for img in self.imgsOnPlaySpace:
                self.playSpace.delete(img)

            self.imgsOnPlaySpace.clear()
            
            hauteur=self.playSpace.winfo_height()
            largeur=self.playSpace.winfo_width()


            
            self.pay = Game.createImg(largeur, hauteur, "png/paysage_2.png")
            img = self.playSpace.create_image(0, 0, image=self.pay, anchor="nw")
            self.imgsOnPlaySpace.append(img)
            # return


            w = int(largeur / (NB_WAGONS+1))
            h = int(hauteur / 3)
            # print(w, h)
            
            self.loco = Game.createImg(w, h, "png/locomotive val.png")
            self.wagon = Game.createImg(w, h, "png/wagon val.png")
            self.queue = Game.createImg(w, h, "png/queue val.png")
 
            
            # self.train.wagons[0].config(image = loco)
            # self.train.wagons[0].image = loco

            img = self.playSpace.create_image(0, h+(h/3), image=self.loco, anchor="nw")
            self.imgsOnPlaySpace.append(img)
            
            for i in range(1, NB_WAGONS):
                # self.train.wagons[i].config(image = wagon)
                # self.train.wagons[i].image = wagon
                img = self.playSpace.create_image(i*w, h+(h/3), image=self.wagon, anchor="nw")
                self.imgsOnPlaySpace.append(img)
            
            # self.train.wagons[NB_WAGONS].config(image = queue)
            # self.train.wagons[NB_WAGONS].image = queue
            img = self.playSpace.create_image(NB_WAGONS*w, h+(h/3), image=self.queue, anchor="nw")
            self.imgsOnPlaySpace.append(img)


    @classmethod
    def createImg(cls, x, y, file):
        img = Image.open(file)
        img = img.resize((x, y))
        return ImageTk.PhotoImage(img)

    # @classmethod
    # def createImgWithTransBg(cls, x, y, file):
    #     img = Image.open(file)
    #     img = img.resize((x, y))
    #     bg = Image.new('RGBA', img.size, (0, 0, 0, 0))
    #     newImg = Image.alpha_composite(bg, img)
    #     return ImageTk.PhotoImage(newImg)
        
            
    # Pour le Marshall
    def deplacement(self):
        i = 0 #position du wagon où se trouve le Marshall
        for wagon in self.wagons:
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

    


#tetewagonqueue est un entier entre 0 et 2, 0=loco, 1=wagon, 2=queue
class Wagon():
    def __init__(self, game:Game, playSpace:Canvas, x:int , y:int, tetewagonqueue:int):
        self.x = x
        self.y = y
        self.marshall = False

        taille = 100

        #chargement de la bonne image
        if tetewagonqueue == 0:
            self.img = Game.createImg(taille, taille, "png/locomotive val.png")
        elif tetewagonqueue == 1:
            self.img = Game.createImg(taille, taille, "png/wagon val.png")
        elif tetewagonqueue == 2:
            self.img = Game.createImg(taille, taille, "png/queue val.png")

        #placement de l'image sur le label
        # self.config(image = self.img)
            
        img = playSpace.create_image((0+y*taille, 0+x*taille), image=self.img, anchor="nw")
        game.imgsOnPlaySpace.append(img)





mon_jeu = Game()



mon_jeu.mainloop()


