import random
from tkinter import * #pour générer une fenêtre et son contenu
from PIL import Image, ImageTk #pour l'import et la modification d'images
from modules.saveGestion import * #for loadSave(win)


global NB_WAGONS
global NB_ACTIONS
global NB_JOUEURS 
global NB_TOURS
global MAX_ACTIONS
global MAX_BULLETS
global COLORS
global LOAD_SAVE
global WIDGET_COLORS


NB_JOUEURS = 2
NB_WAGONS = NB_JOUEURS
NB_TOURS = 3
MAX_ACTIONS = NB_JOUEURS * 2
MAX_BULLETS = (NB_JOUEURS // 2) + 1

COLORS = {"red":(255, 0, 0),
          "orange":(255, 128, 0),
          "yellow":(255, 255, 0),
          "green":(0, 255, 0),
          "blue":(0, 0, 255)}

WIDGET_COLORS = {"red":"#b13001",
                 "redLight":"#ca3904",
                 "sand":"#c1880b",
                 "train":"#723f02"}

LOAD_SAVE = FALSE



























class Game(Tk):
    wagons = [] # liste de classe Wagon
    bandits = [] # liste de classe Bandit
    butins = [] # liste de classe Bandit

    tempActions = []
    tempColor = "green"
    tempName = "nameOeuf"
    

    imgsOnCanvasPlaySpace = [] # liste "stockant" ce qui est dessiné sur un Canvas (afin de les pouvoir les supprimer par la suite)
    imgsOnCanvasMenuSpace = []

    #chargement de toutes les images
    #certaines images ont un % en commentaire, % par rapport à un wagon
    imgMenuSpace = Image.open('png/menuSpaceBackground.png')
    imgMenuButton = Image.open('png/menuSpaceButton.png')

    imgRight = Image.open('png/menuSpace_button_arrow_right.png')
    imgLeft = Image.open('png/menuSpace_button_arrow_left.png')
    imgUp = Image.open('png/menuSpace_button_arrow_up.png')
    imgDown = Image.open('png/menuSpace_button_arrow_down.png')
    imgShoot = Image.open('png/menuSpace_button_shoot.png')
    imgRob = Image.open('png/menuSpace_button_rob.png')

    imgPaysage = Image.open("png/landscape.png")
    imgMarshall = Image.open('png/marshall_v0.png') #width = 26%, height = 42%

    imgLoco = Image.open('png/loco_v2.png') #width = 200%
    imgWagon = Image.open('png/wagon_v2.png')
    imgQueue = Image.open('png/queue_v2.png')

    imgBourse = Image.open("png/bourse_v2.png") #width = 13%, height = 11%
    imgBijoux = Image.open("png/bijoux_v0.png") #width = 7%, height = 6%
    imgMagot = Image.open("png/magot_v1.png") #width = 35%, height = 20%

    imgBody = Image.open("png/bandit_body_v1.png") #width = 26%, height = 42%
    imgDetails = Image.open("png/bandit_details_v1.png") #width = 26%, height = 42%

    imgIconMinution = Image.open("png/icone_munition_v1.png")
    imgIconBourse = Image.open("png/icone_bourse_v1.png")
    #iconBanditHead => crop imgBody/Details to (28-1, 16-1) (58, 46)


    def __init__(self):
        super().__init__()
        self.turn = 1
        self.action = 1
        self.banditQuiChoisi = 0

        #window parameters
        self.title("Colt Zeʁma")
        self.geometry("900x415")

        img = Image.open('train.ico')
        img = ImageTk.PhotoImage(img)
        self.call('wm', 'iconphoto', self._w, img)

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight=1)


        # createMainMenu
        self.canvasMainMenu = Canvas(self, bg='red')
        self.canvasMainMenu.grid(columnspan=2, sticky='nsew')

        for i in [0, 2]:
            self.canvasMainMenu.columnconfigure(i, weight = 1)
        for i in [0, 5]:
            self.canvasMainMenu.rowconfigure(i, weight = 1)

        #mainMenu buttons
        self.btnNew = Button(self.canvasMainMenu, text='New', command=self.createNewGameMenu)
        self.btnLoad = Button(self.canvasMainMenu, text='Load', command=lambda:self.startGame(loadSave=True))
        self.btncredits = Button(self.canvasMainMenu, text='Credits', command=self.createCredits)
        self.btnExit = Button(self.canvasMainMenu, text='Exit', command=self.destroy)

        self.btnNew.grid(column=1, row=1, sticky='nsew')
        self.btnLoad.grid(column=1, row=2, sticky='nsew')
        self.btncredits.grid(column=1, row=3, sticky='nsew')
        self.btnExit.grid(column=1, row=4, sticky='nsew')

        self.canvasMainMenu.bind('<Configure>', lambda e: self.resizeMenusBackground(self.canvasMainMenu))


    def resizeMenusBackground(self, canvas):
        self.img = Game.createLoadedImg(canvas.winfo_width(), canvas.winfo_height(), Game.imgPaysage)
        canvas.create_image(0, 0, image=self.img, anchor='nw')


    def createMainMenu(self):
        # createMainMenu
        self.canvasMainMenu = Canvas(self, bg='red')
        self.canvasMainMenu.grid(columnspan=2, sticky='nsew')

        for i in [0, 2]:
            self.canvasMainMenu.columnconfigure(i, weight = 1)
        for i in [0, 5]:
            self.canvasMainMenu.rowconfigure(i, weight = 1)

        #mainMenu buttons
        self.btnNew = Button(self.canvasMainMenu, text='New', command=self.createNewGameMenu)
        self.btnLoad = Button(self.canvasMainMenu, text='Load', command=lambda:self.startGame(loadSave=True))
        self.btncredits = Button(self.canvasMainMenu, text='Credits', command=self.createCredits)
        self.btnExit = Button(self.canvasMainMenu, text='Exit', command=self.destroy)

        self.btnNew.grid(column=1, row=1, sticky='nsew')
        self.btnLoad.grid(column=1, row=2, sticky='nsew')
        self.btncredits.grid(column=1, row=3, sticky='nsew')
        self.btnExit.grid(column=1, row=4, sticky='nsew')

        self.canvasMainMenu.bind('<Configure>', lambda e: self.resizeMenusBackground(self.canvasMainMenu))


    def createCredits(self):
        self.canvasMainMenu.destroy()
        self.creditsCanvas = Canvas(self, bg='green')
        self.creditsCanvas.grid(columnspan=2, sticky='nsew')

        for i in [0, 2]:
            self.creditsCanvas.columnconfigure(i, weight = 1)
        for i in [0, 3]:
            self.creditsCanvas.rowconfigure(i, weight = 1)

        txt = 'Created by\n\nMaria MESSAOUD-NACER\nValentin GUILLON\n\n\nBased on the game\n"Colt Express"'
        self.labelCredits = Label(self.creditsCanvas, text=txt, justify='center')
        self.creditsBtnExit = Button(self.creditsCanvas, text='Return to Main Menu', command=self.exitCredits)

        self.labelCredits.grid(row=1, column=1, pady=15)
        self.creditsBtnExit.grid(row=2, column=1, pady=15)

        self.creditsCanvas.bind('<Configure>', lambda e: self.resizeMenusBackground(self.creditsCanvas))


    def exitCredits(self):
        self.creditsCanvas.destroy()
        self.createMainMenu()


    def createNewGameMenu(self):
        self.canvasMainMenu.destroy()
        self.loadGameCanvas = Canvas(self, bg='green')
        self.loadGameCanvas.grid(columnspan=2, sticky='nsew')

        for i in [0, 3]:
            self.loadGameCanvas.columnconfigure(i, weight = 1)
        for i in [0, 6]:
            self.loadGameCanvas.rowconfigure(i, weight = 1)
        

        nbPlayers = IntVar()
        nbTurns =  IntVar()
        nbActions =  IntVar()

        nbPlayers.set(2)
        nbTurns.set(3)
        nbActions.set(3)


        self.labelNbPlayers = Label(self.loadGameCanvas, text='Nombre de joueurs')
        self.labelNbTurns = Label(self.loadGameCanvas, text='Nombre de tours')
        self.labelNbActions = Label(self.loadGameCanvas, text="Nombre d'actions par tour")
        self.entryNbPlayers = Entry(self.loadGameCanvas, textvariable=nbPlayers)
        self.entryNbTurns = Entry(self.loadGameCanvas, textvariable=nbTurns)
        self.entryNbActions = Entry(self.loadGameCanvas, textvariable=nbActions)
        self.launchNewGame = Button(self.loadGameCanvas, text='Start', command=lambda:self.startGame(nbPlayers.get(), nbTurns.get(), nbActions.get()))
        self.btnExitNewGameMenu = Button(self.loadGameCanvas, text='Return to Main Menu', command=self.exitNewGameMenu)


        self.labelNbPlayers.grid(row=1, column=1, sticky='e')
        self.labelNbTurns.grid(row=2, column=1, sticky='e')
        self.labelNbActions.grid(row=3, column=1, sticky='e')
        self.entryNbPlayers.grid(row=1, column=2, sticky='w')
        self.entryNbTurns.grid(row=2, column=2, sticky='w')
        self.entryNbActions.grid(row=3, column=2, sticky='w')
        self.launchNewGame.grid(row=4, column=1, columnspan=2, sticky='ew')
        self.btnExitNewGameMenu.grid(row=5, column=1, columnspan=2, sticky='ew')

        self.loadGameCanvas.bind('<Configure>', lambda e: self.resizeMenusBackground(self.loadGameCanvas))


    def exitNewGameMenu(self):
        self.loadGameCanvas.destroy()
        self.createMainMenu()


    def startGame(self, nbPlayers=6, nbTurns=3, nbActions=6, loadSave=False):
        if loadSave:
            global LOAD_SAVE

            LOAD_SAVE = True

        else:
            global NB_JOUEURS
            global NB_WAGONS
            global NB_TOURS
            global MAX_ACTIONS
            global MAX_BULLETS

            NB_JOUEURS = nbPlayers
            NB_WAGONS = NB_JOUEURS
            NB_TOURS = nbTurns
            MAX_ACTIONS = nbActions
            MAX_BULLETS = (NB_JOUEURS // 2) + 1
        
        self.continueInit()
        



    def loadSave(self):
        global LOAD_SAVE
        LOAD_SAVE = True
        self.continueInit()


    def continueInit(self):
        self.canvasMainMenu.destroy()

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
        #oum: menuspace contient 6 lignes (la 6e contient le log/validation space)
        for i in range(5):
            self.menuSpace.rowconfigure(i, weight=1)
        #oum: la dernière ligne doit occuper plus d'espace 
        self.menuSpace.rowconfigure(5, weight=4)

        for j in range(3):
            self.menuSpace.columnconfigure(j, weight=1)

        self.btns = []


        # for i in range(9):
        #     self.menuSpace.rowconfigure(i, weight=1)
        # self.menuSpace.columnconfigure(0, weight=1)
        # self.menuSpace.columnconfigure(5, weight=1)

        # self.btns = []

        #boutons
        self.btnAction = Button(self.menuSpace, text="Action", command=self.testActionsStep1on4, bg=WIDGET_COLORS['redLight'], border=0, highlightthickness=0, activebackground=WIDGET_COLORS['red'], disabledforeground='black')
        # self.btnAction = Button(self.menuSpace, text="Action", command=self.testActionsStep1on4, bg=WIDGET_COLORS['redLight'], border=0, highlightthickness=0, activebackground=WIDGET_COLORS['red'], disabledforeground='black')
        self.btnRight = Button(self.menuSpace, text="->", bg=WIDGET_COLORS['redLight'], border=0, highlightthickness=0, activebackground=WIDGET_COLORS['red'], command=lambda:self.addActions('right'))
        self.btnLeft = Button(self.menuSpace, text="<-", bg=WIDGET_COLORS['redLight'], border=0, highlightthickness=0, activebackground=WIDGET_COLORS['red'], command=lambda:self.addActions('left'))
        self.btnUp = Button(self.menuSpace, text="Up", bg=WIDGET_COLORS['redLight'], border=0, highlightthickness=0, activebackground=WIDGET_COLORS['red'], command=lambda:self.addActions('up'))
        self.btnDown = Button(self.menuSpace, text="Down", bg=WIDGET_COLORS['redLight'], border=0, highlightthickness=0, activebackground=WIDGET_COLORS['red'], command=lambda:self.addActions('down'))
        self.btnShoot = Button(self.menuSpace, text="Shoot", bg=WIDGET_COLORS['redLight'], border=0, highlightthickness=0, activebackground=WIDGET_COLORS['red'], command=lambda:self.addActions('shoot'))
        self.btnSteal = Button(self.menuSpace, text="Rob", bg=WIDGET_COLORS['redLight'], border=0, highlightthickness=0, activebackground=WIDGET_COLORS['red'], command=lambda:self.addActions('rob'))
        
        
        self.btns.append(self.btnRight)
        self.btns.append(self.btnLeft)
        self.btns.append(self.btnUp)
        self.btns.append(self.btnDown)
        self.btns.append(self.btnShoot)
        self.btns.append(self.btnSteal)
        
        

        #placement des buttons
        self.btnAction.grid(row=5, column=2, padx=5, pady=10)
        self.btnRight.grid(row=1, column=3, rowspan=2)
        self.btnLeft.grid(row=1, column=1, rowspan=2)
        self.btnUp.grid(row=0, column=2)
        self.btnDown.grid(row=3, column=2)
        self.btnShoot.grid(row=1, column=2)
        self.btnSteal.grid(row=2, column=2)


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

        self.log.insert(END,"Be fairplay,\nDon't look others' actions\n")
        self.log.config(state=DISABLED)

        #placement du log
        self.logSpace.grid(row=9, column=1, columnspan=3)
        self.lbLog.grid(row=1, column=1, columnspan=2, sticky="nsew")
        self.log.grid(row=2, column=1, sticky="nsew")
        vbar.grid(row=2, column=2, sticky='NS')

        #=== FIN MENU SPACE ================================
        
        self.createValidationCanvas()
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
                    self.wagons.append(Wagon(self, y, 'queue'))
                    continue
                #wagon
                self.wagons.append(Wagon(self, y, 'wagon'))


            #création des bandits
            # for i in range(NB_JOUEURS):
            #     name = "Bandit" + str(i + 1)
            #     color = random.choice(list(COLORS.keys()))
            #     Game.bandits.append(Bandit(self, name, color))


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
        self.test = 1


    def printBandit(self):
        for bandit in self.bandits:
            print(bandit.name, bandit.color, bandit.actions, bandit.position)


    def saveGame(self):
        save(NB_JOUEURS, self.wagons, self.bandits, self.butins)



    def addActions(self, action):
        Game.tempActions.append(action)

        if len(Game.tempActions) < MAX_ACTIONS :
            if self.btnValidate["state"] == 'normal':
                self.btnValidate.config(state='disabled') #ce SERA BTN VALIDATE
                for btn in self.btns:
                    btn.config(state="normal")

        else:
            self.btnValidate.config(state='normal')
            for btn in self.btns:
                btn.config(state="disabled")

        print(Game.tempActions)


    def validateActions(self):
        if self.turn == 1:
            
            #print(f"regarde, elle est pas vide {Game.tempActions}")
            bandito = Bandit(self, self.entryName.get(),self.selected_color.get(), actions=Game.tempActions)
            self.bandits.append(bandito)
            #print(aled.name, aled.color, aled.actions)
            
            test = self.bandits[self.banditQuiChoisi]
            print(test.name, test.color, test.actions)
            self.entryName.delete(0,END)
            #self.updateCanvasImgs()
            print("hi")

        else:
            self.bandits[self.banditQuiChoisi].actions = self.tempActions


        self.banditQuiChoisi += 1

        self.tempActions.clear()
        if self.banditQuiChoisi == NB_JOUEURS:
            #self.btnAction.config(command=self.testActionsStep1on4)
            self.btnAction.config(state='normal')
            #self.btnRight.config(command=self.printBandit)
            self.btnRight.config(state='normal')
            self.banditQuiChoisi = 0
            self.validationSpace.grid_forget()
            self.logSpace.grid(row=9, column=1, columnspan=3)
            

        else:
            #self.validationSpace.grid_forget()
            #self.createValidationCanvas()
            self.btnAction.config(state='disabled') #ce SERA BTN VALIDATE
            for btn in self.btns:
                btn.config(state="normal")

        #self.validationSpace.grid_forget()
        #self.logSpace.grid(row=9, column=0, columnspan=3)

    
    
    def temp_text(self,e):
        self.entryName.delete(0,"end")
    def createValidationCanvas(self):
        self.validationSpace = Canvas(self.menuSpace, border=0)
        self.turn_num = StringVar()
        self.turn_num.set(f"Turn {self.turn}")
        for i in range(6):
            
            self.validationSpace.rowconfigure(i, weight=1)

        if self.turn > 1:
            self.labelTurn = Label(self.validationSpace, textvariable=self.turn_num, justify=CENTER)
            self.labelName = Label(self.validationSpace)
            self.canvasActions = Canvas(self.validationSpace, bg="blue")
            self.canvasActions.config(height=70, width = 225)
            self.btnValidate = Button(self.validationSpace, text='Validate')
            self.labelTurn.grid(row=0, sticky="nsew")
            self.labelName.grid(row=1, sticky="nsew")
            self.canvasActions.grid(row=3, sticky="ew")
            self.btnValidate.grid(row=4, sticky="nsew")

            #create widgets (actions bar, entry for name, colors)



        else:
            #create widgets (actions bar, label for bandit name)
            self.labelTurn = Label(self.validationSpace,textvariable= self.turn_num, justify=CENTER)
            self.entryName = Entry(self.validationSpace,justify=CENTER,borderwidth=2)
            self.entryName.insert(0,"Enter your Name")
            self.canvasColor = Canvas(self.validationSpace, bg="red")
            self.canvasColor.config(height=70, width = 225)
            self.canvasActions = Canvas(self.validationSpace, bg="blue")
            self.canvasActions.config(height=70, width = 225)
            self.btnValidate = Button(self.validationSpace, text='Validate', command=self.validateActions)

            self.labelTurn.grid(row=0, sticky="nsew", column = 0)
            self.entryName.grid(row=1, column = 0)
            
            self.entryName.bind("<FocusIn>",self.temp_text)
            self.canvasColor.grid(row=2, sticky="nsew", column = 0)
            self.canvasActions.grid(row=3, sticky="nsew", column = 0)
            self.btnValidate.grid(row=4, sticky="nsew", column = 0)
            
            #-----------Couleurs----------------
            i = 0
            self.selected_color = StringVar()
            for color in COLORS:
                rb =Radiobutton(self.canvasColor, text = color, value = color , variable = self.selected_color, fg=color,bg='cadet blue')
                rb.config(selectcolor='cadet blue')
                self.selected_color.set(False)	 
                rb.grid(row=0, column= i)
                i+=1 
                
            self.tempColor = self.selected_color
            #-------------Fin Couleurs -----------
        self.logSpace.grid_forget()
        self.validationSpace.grid(row=9, column=1, columnspan=3)
        
    



    def insertTextInLog(self, text,color="black"):
        colorize = "color-" + color
        self.log.config(state="normal")
        self.log.tag_configure(colorize, foreground=color)
        self.log.insert(END, text,colorize)
        self.log.see(END)
        self.log.config(state="disabled")



    def testActionsStep1on4(self):
        self.btnAction.config(state='disabled')
        self.btnAction.config(text='Wait...')
        #execute l'action de chaque bandit (donnée aléatoirement)

        self.insertTextInLog(f"\nTurn {self.turn} :\n")
        self.insertTextInLog(f"Action {self.action} :\n")
        self.action += 1

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
        self.btnAction.config(text='Action')
        
        if not len(self.bandits[0].actions):
            self.turn += 1
            self.createValidationCanvas()

            self.btnAction.config(state='disabled') #ce SERA BTN VALIDATE
            for btn in self.btns:
                btn.config(state="normal")









    def createInventoryCanvas(self, bandit, widthplaySpace, heightplaySpace, index:int):
        #taille de l'inventaire
        widthInventorySize = widthplaySpace//8
        heightInventorySize = heightplaySpace//4

        #position de l'inventaire
        xPlacementPosition = ((widthplaySpace//NB_JOUEURS)*index) + (((widthplaySpace//NB_JOUEURS)//2) - widthInventorySize//2)
        yPlacementPosition = int(heightplaySpace*0.71)

        #taille des icones (de la tête du bandit en réalité, les autres sont 2* plus petit)
        widthIcon = widthInventorySize
        heightIcon = heightInventorySize//2


        #création des images
        bandit.imgHead = Game.createBanditPng(widthIcon, heightIcon, COLORS[bandit.color], crop=True)
        bandit.imgMunition = Game.createLoadedImg(widthIcon//2, heightIcon//2, Game.imgIconMinution)
        bandit.imgBourse = Game.createLoadedImg(widthIcon//2, heightIcon//2, Game.imgIconBourse)
        nbMunitions = bandit.bullets
        nbBourses = len(bandit.butins)

        #placement des images
        img1 = self.playSpace.create_image(xPlacementPosition, yPlacementPosition, image=bandit.imgHead, anchor="nw")
        img2 = self.playSpace.create_image(xPlacementPosition, yPlacementPosition + heightIcon, image=bandit.imgMunition, anchor="nw")
        img3 = self.playSpace.create_image(xPlacementPosition + (widthIcon//2), yPlacementPosition + heightIcon, image=bandit.imgBourse, anchor="nw")

        #placement du texte
        xTextOffset = widthIcon//4
        yTextOffset = heightIcon//4

        x = xPlacementPosition + ((xTextOffset) - (xTextOffset*0.2))
        y = yPlacementPosition + (((heightIcon//2)*3) + (yTextOffset*0.2))
        img4 = self.playSpace.create_text(x, y, text=str(nbMunitions), anchor='nw')

        x = xPlacementPosition + (((widthIcon//2) + xTextOffset) - (xTextOffset*0.2))
        y = yPlacementPosition + (((heightIcon//2)*3) + (yTextOffset*0.2))
        img5 = self.playSpace.create_text(x, y, text=str(nbBourses), anchor='nw')

        #mise des dessins dans la liste globale
        self.imgsOnCanvasPlaySpace.append(img1)
        self.imgsOnCanvasPlaySpace.append(img2)
        self.imgsOnCanvasPlaySpace.append(img3)
        self.imgsOnCanvasPlaySpace.append(img4)
        self.imgsOnCanvasPlaySpace.append(img5)




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
        widthBourse = int(widthWagon * 0.13)
        heightBourse = int(heightWagon *  0.11)
        widthBijoux = int(widthWagon * 0.07)
        heightBijoux = int(heightWagon *  0.06)
        widthMagot = int(widthWagon * 0.35)
        heightMagot = int(heightWagon *  0.20)

        #taille des images de boutons
        sizeButton = ((heightCanvas//3) * 2) // 7



        #MENU SPACE =========================================
        #resize du log
        self.log.config(width=widthCanvas//20, height=int((heightCanvas//3)*0.08))

        #images des boutons
        self.imgTest = Game.createLoadedImg(sizeButton, sizeButton, Game.imgWagon)
        self.imgBtnRight = Game.createLoadedImg(sizeButton, sizeButton, Game.imgRight)
        self.imgBtnLeft = Game.createLoadedImg(sizeButton, sizeButton, Game.imgLeft)
        self.imgBtnUp = Game.createLoadedImg(sizeButton, sizeButton, Game.imgUp)
        self.imgBtnDown = Game.createLoadedImg(sizeButton, sizeButton, Game.imgDown)
        self.imgBtnShoot = Game.createLoadedImg(sizeButton, sizeButton, Game.imgShoot)
        self.imgBtnRob = Game.createLoadedImg(sizeButton, sizeButton, Game.imgRob)

        self.btnRight.config(image=self.imgBtnRight)
        self.btnLeft.config(image=self.imgBtnLeft)
        self.btnUp.config(image=self.imgBtnUp)
        self.btnDown.config(image=self.imgBtnDown)
        self.btnShoot.config(image=self.imgBtnShoot)
        self.btnSteal.config(image=self.imgBtnRob)


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
        for wagon in Game.wagons:
            nbButins = len(wagon.butins)

            if nbButins == 0:
                continue

            #une boucle juste pour le magot
            for butin in wagon.butins:
                if not butin.type == 'magot':
                    continue

                xButinPosition = butin.position['x']
                yButinPosition:str = butin.position['y']

                #les Offset permet de placer le butin au centre du wagon (sont ajustés par la suite)
                xOffsetButin = widthWagon + (widthWagon//2) - (widthMagot//2)
                yOffsetButin = (heightWagon-heightMagot) - (heightWagon * 0.35) #hauteaur à l'intérieur du wagon

                xImgPosition = (xButinPosition * widthWagon) + xOffsetButin

                if yButinPosition == 'in':
                    yImgPosition = heightWagon + yOffsetButin
                elif yButinPosition == 'out':
                    yImgPosition = yOffsetButin + (heightWagon * 0.40)
                else:
                    print("ERROR: the butin is in a wagon's list, but is own by a bandit")
                    continue


                butin.img = Game.createLoadedImg(widthMagot, heightMagot, self.imgMagot)
                img = self.playSpace.create_image(xImgPosition, yImgPosition, image=butin.img, anchor="nw")
                self.imgsOnCanvasPlaySpace.append(img)

                break


            #une boucle pour les autres type de butins (sauf 'magot')
            for i in range(nbButins):
                butin = wagon.butins[i]

                xButinPosition = butin.position['x']
                yButinPosition:str = butin.position['y']


                if butin.type == 'magot':
                    continue
                    

                elif butin.type == 'bijoux':
                    #les Offset permet de placer le butin au centre du wagon (sont ajustés par la suite)
                    xOffsetButin = widthWagon + (widthWagon//2) - (widthBijoux//2)
                    yOffsetButin = (heightWagon-heightBijoux) - (heightWagon * 0.32) #hauteaur à l'intérieur du wagon

                    if butin.bracable == False:
                        #décalage selon le nombre de butins dans le même wagon
                        if (i % 2) == 1:
                            xOffsetButin += (((widthWagon*0.6) // nbButins) + ((i * ((widthWagon*0.6) // nbButins)))) //2

                        else:
                            xOffsetButin -= (((widthWagon*0.6) // nbButins) + ((i * ((widthWagon*0.6) // nbButins)))) //2

                        #décalage y
                        yOffsetButin -= (heightWagon*0.005) * (i%3) #réhaussement de 1% * 0 ou 1 ou 2

                    else: #bracable == True
                        #décalage selon le nombre de butins dans le même wagon
                        if (i % 2) == 1:
                            xOffsetButin += (((widthWagon*0.2) // nbButins) + ((i * ((widthWagon*0.2) // nbButins)))) //2

                        else:
                            xOffsetButin -= (((widthWagon*0.2) // nbButins) + ((i * ((widthWagon*0.2) // nbButins)))) //2

                        #décalage y
                        yOffsetButin -= heightWagon*0.2 #réhaussement pour le placer sur la table
                        yOffsetButin -= (heightWagon*0.005) * (i%3) #réhaussement de 1% * 0 ou 1 ou 2


                    xImgPosition = (xButinPosition * widthWagon) + xOffsetButin

                    if yButinPosition == 'in':
                        yImgPosition = heightWagon + yOffsetButin
                    elif yButinPosition == 'out':
                        yImgPosition = yOffsetButin + (heightWagon * 0.38)
                    else:
                        print("ERROR: the butin is in a wagon's list, but is own by a bandit")
                        continue

                    


                elif butin.type == 'bourse':
                    #les Offset permet de placer le butin au centre du wagon (sont ajustés par la suite)
                    xOffsetButin = widthWagon + (widthWagon//2) - (widthBourse//2)
                    yOffsetButin = (heightWagon-heightBourse) - (heightWagon * 0.32) #hauteaur à l'intérieur du wagon

                    if butin.bracable == False:
                        #décalage x selon le nombre de butins dans le même wagon
                        if (i % 2) == 1:
                            xOffsetButin += (((widthWagon*0.6) // nbButins) + ((i * ((widthWagon*0.6) // nbButins)))) // 2

                        else:
                            xOffsetButin -= (((widthWagon*0.6) // nbButins) + ((i * ((widthWagon*0.6) // nbButins)))) // 2

                        #décalage y
                        yOffsetButin -= (heightWagon*0.005) * (i%3) #réhaussement de 1% * 0 ou 1 ou 2


                    else: #bracable == True
                        #décalage x selon le nombre de butins dans le même wagon
                        if (i % 2) == 1:
                            xOffsetButin += (((widthWagon*0.2) // nbButins) + ((i * ((widthWagon*0.2) // nbButins)))) // 2

                        else:
                            xOffsetButin -= (((widthWagon*0.2) // nbButins) + ((i * ((widthWagon*0.2) // nbButins)))) // 2

                        #décalage
                        yOffsetButin -= heightWagon*0.2 #réhaussement pour le placer sur la table
                        yOffsetButin -= (heightWagon*0.005) * (i%3) #réhaussement de 1% * 0 ou 1 ou 2


                    xImgPosition = (xButinPosition * widthWagon) + xOffsetButin

                    if yButinPosition == 'in':
                        yImgPosition = heightWagon + yOffsetButin
                    elif yButinPosition == 'out':
                        yImgPosition = yOffsetButin + (heightWagon * 0.38)
                    else:
                        print("ERROR: the butin is in a wagon's list, but is own by a bandit")
                        continue
                



                if butin.type == 'bijoux':
                    butin.img = Game.createLoadedImg(widthBijoux, heightBijoux, self.imgBijoux)
                elif butin.type == 'bourse':
                    butin.img = Game.createLoadedImg(widthBourse, heightBourse, self.imgBourse)

                img = self.playSpace.create_image(xImgPosition, yImgPosition, image=butin.img, anchor="nw")
                self.imgsOnCanvasPlaySpace.append(img)


        # for wagon in self.wagons:
        #     nbButins = len(wagon.butins)

        #     for i,butin in enumerate(wagon.butins) :
        #         xOffsetButin = 0
        #         yOffsetButin = heightWagon
 
        #         if butin.type == 'magot':
        #             butin.img=  Game.createLoadedImg(widthMagot,heightMagot, self.imgMagot)
        #             xOffsetButin = xOffsetCharacter + widthMagot
                    
        #             if butin.position['y'] == 'toit':
        #                 yOffsetButin =  heightMagot


        #         elif butin.type == 'bijoux' : 
        #             butin.img=  Game.createLoadedImg(widthBijoux,heightBijoux, self.imgBijoux)
        #             xOffsetButin = xOffsetCharacter + widthBijoux
                    
        #             if butin.position['y'] == 'toit':
        #                 yOffsetButin =  heightBijoux 


        #         elif butin.type == 'bourse':
        #             butin.img=  Game.createLoadedImg(widthBourse,heightBourse, self.imgBourse)
        #             xOffsetButin = xOffsetCharacter + widthBourse
                    
        #             if butin.position['y'] == 'toit':
        #                 yOffsetButin =  heightBourse  

                
        #         if (i % 2) == 1: #permet de décaler les bandit les uns des autres
        #             xOffsetButin += ((widthWagon //nbButins) + ((i * (widthWagon // nbButins)))) // 8

        #         else:
        #             xOffsetButin -= ((widthWagon // nbButins) + ((i * (widthWagon // nbButins)))) // 8
        #         img = self.playSpace.create_image((wagon.xPosition * widthWagon) + xOffsetButin , heightCharacter+yOffsetButin, image = butin.img, anchor="nw")
        #         self.imgsOnCanvasPlaySpace.append(img)

        # FIN === ON DESSINE LES BUTINS DANS LES WAGONS ======================


        #ON DESSINE LES INVENTAIRES DES BANDITS ==============================

        for i, bandit in enumerate(self.bandits):
            self.createInventoryCanvas(bandit, widthCanvas, heightCanvas, i)

        #FIN === ON DESSINE LES INVENTAIRES DES BANDITS ======================
    

    @staticmethod
    def createLoadedImg(width, height, loadedImg):
        loadedImg = loadedImg.resize((width, height))
        return ImageTk.PhotoImage(loadedImg)


    @staticmethod
    def createBanditPng(width, height, color, crop=False):
        body = Game.imgBody
        details = Game.imgDetails

        if crop:
            #head box from bandit body/details pngs : (28-1, 16-1) (58, 46)
            body = body.crop((28-1, 16-1, 58, 46))
            details = details.crop((28-1, 16-1, 58, 46))
        
        body = body.resize((width, height))
        details = details.resize((width, height))

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

            elif self.type == 'wagon':
                for i in range(random.randint(1, 4)):
                    self.butins.append(Butin(game, random.choice(Wagon.butinTypes), self.xPosition))























class Bandit():
    def __init__(self, game:Game, name:str, color:str, position:tuple=None, actions:list=None, bullets:int=None):
        self.name = name
        self.color = color
        self.position = {'x':NB_WAGONS, 'y':1} #x => index du wagon dans Game.wagons, y => position dans le wagon(0=toit, 1=intérieur)
        self.actions = actions.copy() #action = 'right', 'left', 'up', 'down', 'shoot' or 'rob'
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
            self.game.insertTextInLog(f"{self.name} has no actions\n",self.color)
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
                self.game.insertTextInLog(f"{banditName} can't move {action}\n",self.color)
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
                self.game.insertTextInLog(f"{banditName} can't move {action}\n",self.color)
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
                self.game.insertTextInLog(f"{banditName} can't move {action}\n",self.color)
                return
            self.position['y'] = 0

        if action == 'down':
            if yBanditPosition == 1:
                self.game.insertTextInLog(f"{banditName} can't move {action}\n",self.color)
                return
            self.position['y'] = 1

        
        self.game.insertTextInLog(f"{self.name} has moved {action}\n",self.color)

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
        self.game.insertTextInLog(f"{self.name} prepare to shoot\n",self.color)

        if self.bullets == 0:
            self.game.insertTextInLog(f"{self.name} has no more bullets\n",self.color)
            return


        nb_targets = 0

        #on compte le nombre de cible possible (nombre de bandit dans le même wagon ET au même étage)
        for bandit in self.game.wagons[self.position['x']].bandits:
            if bandit.name == self.name:
                continue

            if bandit.position['y'] == self.position['y']:
                nb_targets += 1

        if nb_targets == 0:
            self.game.insertTextInLog(f"{self.name} has no targets to shoot\n",self.color)
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
        self.game.insertTextInLog(f"{self.name} rob\n",self.color)

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
        self.game.insertTextInLog(f"{self.name} robbed {robbedButin.type}({robbedButin.value})\n",self.color)



    #perd un butin, aléatoirement
    def getHitByBandit(self, ennemyName:str):
        self.game.insertTextInLog(f"{self.name} get hit by {ennemyName}\n",self.color)#couleure de l'ennemy a ajouter 


        if len(self.butins) == 0: #le bandit n'a pas de butins{self.name}
            return

        #on retire un butin du bandit, aléatoirement
        lostButin = self.butins.pop(random.randint(0, len(self.butins) - 1))
        if self.position['y'] == 0:
            lostButin.position['y'] = 'out'
        elif self.position['y'] == 1:
            lostButin.position['y'] = 'int'
        #qu'on rajoute dans la liste butins du wagon du bandit
        self.game.wagons[self.position['x']].butins.append(lostButin)
        self.game.insertTextInLog(f"{self.name} lost {lostButin.type}({lostButin.value})\n",self.color)



    #perd un butin, aléatoirement, et monte sur le toit
    def getHitByMarshall(self):
        self.game.insertTextInLog(f"{self.name} get hit by the Marshall\n",self.color)


        if len(self.butins):
            #on retire un butin du bandit
            lostButin = self.butins.pop(random.randint(0, len(self.butins) - 1))

            if self.position['y'] == 0:
                lostButin.position['y'] = 'out'
            elif self.position['y'] == 1:
                lostButin.position['y'] = 'int'

            #qu'on rajoute dans le wagon
            self.game.wagons[self.position['x']].butins.append(lostButin)
            self.game.insertTextInLog(f"{self.name} lost {lostButin.type}({lostButin.value})\n",self.color)

        #le bandit monte sur le toit
        self.position['y'] = 0
        self.game.insertTextInLog(f"{self.name} move on the roof\n",self.color)


    def checkForButin(self):
        wagon = self.game.wagons[self.position['x']]

        for i, butin in enumerate(wagon.butins):
            if butin.bracable == False:
                if self.position['x'] == wagon.xPosition: 
                    robbedButin = wagon.butins.pop(i)
                    self.butins.append(robbedButin)
                    self.game.insertTextInLog(f"{self.name} got {robbedButin.type}({robbedButin.value})\n",self.color)




    def butinAtSamePosition(self, butin):
        pos:str = butin.position['y']

        if pos == 'out' and self.position['y'] == 0:
            return True
        if pos == 'int' and self.position['y'] == 1:
            return True

        return False


























class Butin():
    lootValues = {'bourse':[100,200], 'bijoux' : [500], 'magot' : [1000]}

    def __init__(self, game:Game, type:str, x:int, value:int=None, position:tuple=None, bracable:bool=None):
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
