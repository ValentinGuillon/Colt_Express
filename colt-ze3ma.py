import random
from tkinter import *
from PIL import Image, ImageTk #pour l'import et la modification d'images
import modules.saveGestion as saveGestion


global NB_JOUEURS 
global NB_WAGONS
global NB_TOURS
global MAX_ACTIONS
global MAX_BULLETS
global LOAD_SAVE
global COLORS
global WIDGET_COLORS


NB_JOUEURS = 4
NB_WAGONS = NB_JOUEURS
NB_TOURS = 3
MAX_ACTIONS = NB_JOUEURS * 2
MAX_BULLETS = (NB_JOUEURS // 2) + 1

LOAD_SAVE = FALSE

COLORS = {"red":(255, 0, 0),
          "orange":(255, 128, 0),
          "yellow":(255, 255, 0),
          "green":(0, 255, 0),
          "blue":(0, 0, 255)}

WIDGET_COLORS = {"red":"#b13001",
                 "redLight":"#ca3904",
                 "sand":"#c1880b",
                 "train":"#723f02"}




























class Game(Tk):
    wagons = [] # liste de classe Wagon
    bandits = [] # liste de classe Bandit
    butins = [] # liste de classe Butin

    #lists used during preparation phase
    tempName = "nameOeuf"
    tempColor = []
    tempActions = [] #liste de classe Action (qui permet de reconfigurer l'ordre des actions d'un bandit)

    #fill tempColor
    for color in COLORS:
        tempColor.append(color)


    
    #listes "stockant" ce qui est dessiné sur un Canvas (afin de les pouvoir les supprimer par la suite)
    imgsOnCanvasPlaySpace = []
    imgsOnCanvasMenuSpace = []


    #chargement de toutes les images
    #certaines images ont un % en commentaire, % par rapport à un wagon
    imgPaysage = Image.open("png/landscape.png")

    imgRight = Image.open('png/menuSpace_button_arrow_right.png')
    imgLeft = Image.open('png/menuSpace_button_arrow_left.png')
    imgUp = Image.open('png/menuSpace_button_arrow_up.png')
    imgDown = Image.open('png/menuSpace_button_arrow_down.png')
    imgShoot = Image.open('png/menuSpace_button_shoot.png')
    imgRob = Image.open('png/menuSpace_button_rob.png')

    imgLoco = Image.open('png/loco_v2.png') #width = 200%
    imgWagon = Image.open('png/wagon_v2.png')
    imgQueue = Image.open('png/queue_v2.png')

    imgBourse = Image.open("png/bourse_v2.png") #width = 13%, height = 11%
    imgBijoux = Image.open("png/bijoux_v1.png") #width = 7%, height = 6%
    imgMagot = Image.open("png/magot_v1.png") #width = 35%, height = 20%

    imgMarshall = Image.open('png/marshall_v1.png') #width = 26%, height = 42%

    imgBody = Image.open("png/bandit_body_v1.png") #width = 26%, height = 42%
    imgDetails = Image.open("png/bandit_details_v1.png") #width = 26%, height = 42%

    imgIconMinution = Image.open("png/icone_munition_v1.png")
    imgIconBourse = Image.open("png/icone_bourse_v1.png")
    imgIconBanditBody = Image.open("png/icone_bandit_body_v1.png")
    imgIconBanditDetails = Image.open("png/icone_bandit_details_v1.png")



    def __init__(self):
        super().__init__()

        #window parameters
        self.title("Colt Zeʁma")
        self.geometry("900x415")
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight=1)

        #icon d'application
        img = ImageTk.PhotoImage(Image.open('train.ico'))
        self.call('wm', 'iconphoto', self._w, img)


        #var de choix des actions
        self.currentTurn = 1
        self.action = 1 #only used to insert in Log while Actions phase
        self.banditQuiChoisi = 0


        # createMainMenuCanvas
        self.createMainMenuCanvas()




    def resizeMenusBackground(self, canvas):
        self.img = Game.createLoadedImg(canvas.winfo_width(), canvas.winfo_height(), Game.imgPaysage)
        canvas.create_image(0, 0, image=self.img, anchor='nw')


    #MENU CANVAS CREATION ================================================

    def createMainMenuCanvas(self):
        self.canvasMainMenu = Canvas(self, bg='red')
        self.canvasMainMenu.grid(columnspan=2, sticky='nsew')

        for i in [0, 2]:
            self.canvasMainMenu.columnconfigure(i, weight = 1)
        for i in [0, 5]:
            self.canvasMainMenu.rowconfigure(i, weight = 1)

        #mainMenu buttons
        self.btnNew = Button(self.canvasMainMenu, text='New', command=self.createNewGameMenuCanvas)
        self.btnLoad = Button(self.canvasMainMenu, text='Load', command=lambda:self.startGame(loadSave=True))
        self.btncredits = Button(self.canvasMainMenu, text='Credits', command=self.createCreditsMenuCanvas)
        self.btnExit = Button(self.canvasMainMenu, text='Exit', command=self.destroy)

        self.btnNew.grid(column=1, row=1, sticky='nsew')
        self.btnLoad.grid(column=1, row=2, sticky='nsew')
        self.btncredits.grid(column=1, row=3, sticky='nsew')
        self.btnExit.grid(column=1, row=4, sticky='nsew')

        self.canvasMainMenu.bind('<Configure>', lambda e: self.resizeMenusBackground(self.canvasMainMenu))


    def createCreditsMenuCanvas(self):
        self.canvasMainMenu.destroy()
        self.creditsCanvas = Canvas(self, bg='green')
        self.creditsCanvas.grid(columnspan=2, sticky='nsew')

        for i in [0, 2]:
            self.creditsCanvas.columnconfigure(i, weight = 1)
        for i in [0, 3]:
            self.creditsCanvas.rowconfigure(i, weight = 1)

        txt = 'Created by\n\nMaria MESSAOUD-NACER\nValentin GUILLON\n\n\nBased on the game\n"Colt Express"'
        self.labelCredits = Label(self.creditsCanvas, text=txt, justify='center')
        self.creditsBtnExit = Button(self.creditsCanvas, text='Return to Main Menu', command=self.exitCreditsMenu)

        self.labelCredits.grid(row=1, column=1, pady=15)
        self.creditsBtnExit.grid(row=2, column=1, pady=15)

        self.creditsCanvas.bind('<Configure>', lambda e: self.resizeMenusBackground(self.creditsCanvas))


    def createLoadGameCanvas(self):
        pass
        #afficher un aperçu de se que contient la sauvegarde


    def createNewGameMenuCanvas(self):
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



    def createEndGameMenuCanvas(self, text):
        self.playSpace.destroy()
        self.menuSpace.destroy()

        self.endGameMenu = Canvas(self, bg='red')
        self.endGameMenu.grid(columnspan=2, sticky='nsew')

        for i in [0, 2]:
            self.endGameMenu.columnconfigure(i, weight = 1)
        for i in [0, 4]:
            self.endGameMenu.rowconfigure(i, weight = 1)

        #mainMenu buttons
        self.label = Label(self.endGameMenu, text=text, justify=CENTER)
        self.btnExitToMainMenu = Button(self.endGameMenu, text='Return to Main Menu', command=self.exitEndGameMenu)
        self.btnExit = Button(self.endGameMenu, text='Exit', command=self.destroy)

        self.label.grid(column=1, row=1, sticky='nsew')
        self.btnExitToMainMenu.grid(column=1, row=2, sticky='nsew')
        self.btnExit.grid(column=1, row=3, sticky='nsew')

        self.endGameMenu.bind('<Configure>', lambda e: self.resizeMenusBackground(self.endGameMenu))

    #FIN === MENU CANVAS CREATION =====================================



    #CHANGE MENU ======================================================

    def exitCreditsMenu(self):
        self.creditsCanvas.destroy()
        self.createMainMenuCanvas()


    def exitNewGameMenu(self):
        self.loadGameCanvas.destroy()
        self.createMainMenuCanvas()

    def exitEndGameMenu(self):
        self.endGameMenu.destroy()
        self.createMainMenuCanvas()

    #CHANGE MENU ======================================================


    #mise à jour des variables globales (avant de continuer à process)
    def startGame(self, nbPlayers=4, nbTurns=3, nbActions=6, loadSave=False):
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
            MAX_BULLETS = (nbPlayers // 2) + 1
        
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

        for i in range(6):
            self.menuSpace.rowconfigure(i, weight=1)

        for i in range(3):
            self.menuSpace.columnconfigure(i, weight=1)


        self.btns = []

        #boutons
        self.btnAction = Button(self.menuSpace, text="Action", command=self.executeTurnStep1on4, bg=WIDGET_COLORS['red'], border=0, highlightthickness=0, activebackground=WIDGET_COLORS['red'], disabledforeground='black')
        self.btnRight = Button(self.menuSpace, text="->", command=lambda:self.addActionToTempActions('right'))
        self.btnLeft = Button(self.menuSpace, text="<-", command=lambda:self.addActionToTempActions('left'))
        self.btnUp = Button(self.menuSpace, text="Up", command=lambda:self.addActionToTempActions('up'))
        self.btnDown = Button(self.menuSpace, text="Down", command=lambda:self.addActionToTempActions('down'))
        self.btnShoot = Button(self.menuSpace, text="Shoot", command=lambda:self.addActionToTempActions('shoot'))
        self.btnSteal = Button(self.menuSpace, text="Rob", command=lambda:self.addActionToTempActions('rob'))
        
        self.btns.append(self.btnRight)
        self.btns.append(self.btnLeft)
        self.btns.append(self.btnUp)
        self.btns.append(self.btnDown)
        self.btns.append(self.btnShoot)
        self.btns.append(self.btnSteal)

        #set all buttons's attributes (except "btnAction")
        for btn in self.btns:
            btn.config(bg=WIDGET_COLORS['redLight'], border=0, highlightthickness=0, activebackground=WIDGET_COLORS['red'])


        #placement des buttons
        self.btnAction.grid(row=5, column=1, padx=5, pady=10)
        self.btnRight.grid(row=1, column=2, rowspan=2)
        self.btnLeft.grid(row=1, column=0, rowspan=2)
        self.btnUp.grid(row=0, column=1)
        self.btnDown.grid(row=3, column=1)
        self.btnShoot.grid(row=1, column=1)
        self.btnSteal.grid(row=2, column=1)


        #actions history
        self.createCanvasLog()

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
                    self.wagons.append(Wagon(self, y, 'queue'))
                    continue
                #wagon
                self.wagons.append(Wagon(self, y, 'wagon'))


            #ajout du marshall
            self.wagons[0].marshall = True

            self.btnAction.config(state='disabled', text='Choose your actions...', bg=WIDGET_COLORS['red'])
            self.createValidationCanvas()


        #create from loaded game
        else:
            #import save
            NB_JOUEURS, tempWagons, tempBandits, tempButins = saveGestion.loadSave()

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

                Butin(self, type, None, value=value, position=(xPos, yPos), bracable=bracable)
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
            
            for btn in self.btns:
                btn.config(state='disabled')




        #resize des images de l'interface lorsque la fenêtre est redimensionnée
        self.playSpace.bind('<Configure>', lambda e: self.updateCanvasImgs())




    def saveGame(self):
        saveGestion.save(NB_JOUEURS, self.wagons, self.bandits, self.butins)



    def addActionToTempActions(self, action):
        actionbtn = Action(self, self.actionsFrame, action, len(Game.tempActions))
        Game.tempActions.append(actionbtn)

        if len(Game.tempActions) < MAX_ACTIONS : #il manque des actions
            #on désactive btn "Valide" et on active les btn actions
            self.btnValidate.config(state='disabled')
            for btn in self.btns:
                btn.config(state="normal")

        else:
            self.btnValidate.config(state='normal')
            for btn in self.btns:
                btn.config(state="disabled")

        self.updateActionsBar()



    def removeAction(self, actionToRemove):
        founded = False
        for action in Game.tempActions:
            if founded:
                action.column -= 1
                continue
            if action == actionToRemove:
                founded = True

        if not founded:
            print("ERROR: action not removed")
            return

        Game.tempActions.remove(actionToRemove)
        self.updateActionsBar()



    def updateActionsBar(self):
        #clear actions bar
        for widget in self.actionsFrame.grid_slaves(row=0):
            widget.grid_remove()
        
        #fill it
        for action in Game.tempActions:
            action.grid(row=0, column=action.column)

        #update buttons state
        if len(Game.tempActions) == MAX_ACTIONS: #nombre d'actions atteint
            self.btnValidate.config(state='normal')
            for btn in self.btns:
                btn.configure(state='disabled')
        else: #il n'y a pas assez d'actiions
            self.btnValidate.config(state='disabled')
            for btn in self.btns:
                btn.configure(state='normal')



    def clearActionsBar(self):
        for widget in self.actionsFrame.grid_slaves(row=0):
            widget.grid_remove()
        
        Game.tempActions.clear()
        self.updateActionsBar()



    def appendActionsToBandit(self):
        if self.currentTurn == 1:
            #do nothing if name or color are missing
            if self.entryName.get() in ["", "<Enter your name>"]:
                print("Name are missing")
                return
            if not self.selected_color.get() in Game.tempColor:
                print("Color are missing")
                return

        tempActions = []
        for actionBtn in Game.tempActions:
            tempActions.append(actionBtn.value)

        if self.currentTurn == 1: #on créé un nouveau Bandit
            bandit = Bandit(self, self.entryName.get(), self.selected_color.get(), actions=tempActions)
            self.bandits.append(bandit)

            #reset Name and Color values of Validation Canvas
            self.tempColor.remove(self.selected_color.get())
            self.entryName.delete(0,END)
            
            #suppression et recréation du Validation Canvas
            self.validationSpace.grid_forget()
            self.createValidationCanvas()

        else: #append les actions dans un bandit
            self.bandits[self.banditQuiChoisi].actions = tempActions

            #reset Name and Color values of Validation Canvas
            #self.tempColor.remove(self.selected_color.get())
            #self.entryName.delete(0,END)
            
            #suppression et recréation du Validation Canvas
            self.validationSpace.grid_forget()
            self.createValidationCanvas()

        self.banditQuiChoisi += 1

        Game.tempActions.clear()


        if self.banditQuiChoisi == NB_JOUEURS: #tous les joueurs ont selectionnés leurs actions
            self.btnAction.config(state='normal', text='Action !', bg=WIDGET_COLORS['sand'])
            for btn in self.btns:
                btn.config(state="disabled")

            self.banditQuiChoisi = 0
            self.validationSpace.grid_forget()
            self.logSpace.grid(row=7, column=0, columnspan=3)
            

        else: #d'autres joueurs doivent encore choisir leur actions
            self.btnValidate.config(state='disabled')
            for btn in self.btns:
                btn.config(state="normal")

    

    def clearEntry(self):
        self.entryName.delete(0, END)

 
    #VALIDATION/LOG CANVAS CREATION ================================================

    def createValidationCanvas(self):
        self.validationSpace = Canvas(self.menuSpace, border=0)
        for i in range(6):
            self.validationSpace.rowconfigure(i, weight=1)


        self.nbTurnForLabel = StringVar()
        self.nbTurnForLabel.set(f"Turn {self.currentTurn}/{NB_TOURS}")



        if self.currentTurn == 1: #c'est le premier tout, il faut créer les bandits
            #create widgets (actions bar, label for bandit name)
            self.labelTurn = Label(self.validationSpace, textvariable=self.nbTurnForLabel, justify=CENTER)
            self.entryName = Entry(self.validationSpace, justify=CENTER, borderwidth=2)
            self.entryName.insert(0, "<Enter your name>")
            self.colorFrame = Frame(self.validationSpace, bg='red')
            self.actionsFrame = Frame(self.validationSpace, bg=WIDGET_COLORS['sand'])
            self.btnValidate = Button(self.validationSpace, text='Validate', command=self.appendActionsToBandit, state='disabled')

            self.labelTurn.grid(row=0, sticky="nsew", column = 0)
            self.entryName.grid(row=1, column = 0)
            
            self.entryName.bind("<FocusIn>", lambda e:self.clearEntry())

            self.colorFrame.rowconfigure(0,weight=1)
            for i in range(len(self.tempColor)):
                self.colorFrame.columnconfigure(i,weight = 1)
            self.colorFrame.grid(row=2, column=0, sticky="nsew")
            self.actionsFrame.rowconfigure(0, weight=1)
            for i in range(MAX_ACTIONS):
                self.actionsFrame.columnconfigure(i, weight=1)

            self.actionsFrame.grid(row=3, column=0, sticky='nsew')
            
            
            self.btnValidate.grid(row=4, sticky="nsew", column = 0)


            #-----------Couleurs----------------
            self.selected_color = StringVar()
            for i, color in enumerate(self.tempColor):
                rb = Radiobutton(self.colorFrame, text = color, value = color , variable = self.selected_color, fg=color,bg='cadet blue',selectcolor='cadet blue')
                self.selected_color.set(False)	 
                rb.grid(row=0, column= i,sticky="nsew")


            #-------------Fin Couleurs -----------


        elif self.currentTurn > 1: #on n'a pas besoin de redonner un nom et choisir un couleur
            #create widgets (actions bar, entry for name, colors)

            self.banditNameForLabel = StringVar()
            self.banditNameForLabel.set(f"{self.bandits[self.banditQuiChoisi].name}")
            self.labelTurn = Label(self.validationSpace, textvariable=self.nbTurnForLabel, justify=CENTER)
            self.labelName = Label(self.validationSpace, textvariable=self.banditNameForLabel, justify=CENTER)
            self.actionsFrame = Frame(self.validationSpace, bg=WIDGET_COLORS['sand'])
            self.btnValidate = Button(self.validationSpace, text='Validate', command=self.appendActionsToBandit, state='disabled')

            self.labelTurn.grid(row=0, sticky="nsew")
            self.labelName.grid(row=1, sticky="nsew")
            self.actionsFrame.grid(row=3, column=0,sticky='nsew')
            self.btnValidate.grid(row=4, sticky="nsew")

            self.actionsFrame.rowconfigure(0, weight=1)
            for i in range(MAX_ACTIONS):
                self.actionsFrame.columnconfigure(i, weight=1)
            


        self.logSpace.grid_forget()
        self.validationSpace.grid(row=7, column=0, columnspan=3)


        #place and remove an Action (so that actionsFrame expand in height)
        self.addActionToTempActions('osef')
        self.after(ms=200, func=self.clearActionsBar)
    


    def createCanvasLog(self):
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
        self.logSpace.grid(row=7, column=0, columnspan=3)
        self.lbLog.grid(row=1, column=1, columnspan=2, sticky="nsew")
        self.log.grid(row=2, column=1, sticky="nsew")
        vbar.grid(row=2, column=2, sticky='NS')
    
    #FIN === VALIDATION/LOG CANVAS CREATION ========================================



    def insertTextInLog(self, text, color="black"):
        colorize = "color-" + color
        self.log.config(state="normal")
        self.log.tag_configure(colorize, foreground=color)
        self.log.insert(END, text,colorize)
        self.log.see(END)
        self.log.config(state="disabled")



    def executeTurnStep1on4(self):
        self.btnAction.config(state='disabled', text='Wait...', bg=WIDGET_COLORS['red'])

        self.insertTextInLog(f"\nTurn {self.currentTurn} :\n")
        self.insertTextInLog(f"Action {self.action} :\n")
        self.action += 1

        #execute l'action de chaque bandit
        for bandit in Game.bandits:
            bandit.testRandomAction()


        self.updateCanvasImgs()

        self.after(ms=100, func=self.executeTurnStep2on4)


    def executeTurnStep2on4(self):
        #verifie pour chaque bandit s'il le Marshall est au même endroit (déplace le bandit si oui)
        for bandit in Game.bandits:
            bandit.checkMarshallPresence()

        #update du Canvas
        self.updateCanvasImgs()

        self.after(ms=500, func=self.executeTurnStep3on4)


    def executeTurnStep3on4(self):
        #déplace le marshall
        self.moveMarshall()

        #update du Canvas
        self.updateCanvasImgs()

        self.after(ms=100, func=self.executeTurnStep4on4)



    def executeTurnStep4on4(self):
        #verifie pour chaque bandit s'il le Marshall est au même endroit (déplace le bandit si oui)
        for bandit in Game.bandits:
            bandit.checkMarshallPresence()

        #update du Canvas
        self.updateCanvasImgs()
        self.btnAction.config(state='normal', text='Action !', bg=WIDGET_COLORS['sand'])
        
        if not len(self.bandits[0].actions):
            if self.currentTurn == NB_TOURS:
                self.determineWinner()
                return

            self.currentTurn += 1
            self.createValidationCanvas()

            self.btnAction.config(state='disabled', text='Choose your actions', bg=WIDGET_COLORS['red'])
            for btn in self.btns:
                btn.config(state="normal")




    def determineWinner(self):
        indexWinners = []
        moneyAmount = 0

        endGameMessage = "Results:\n"
        for i, bandit in enumerate(self.bandits):
            endGameMessage += bandit.formatedStr() + '\n'
            tempMoneyAmount = 0
            for butin in bandit.butins:
                tempMoneyAmount += butin.value

            if tempMoneyAmount == moneyAmount:
                indexWinners.append(i)
            elif tempMoneyAmount > moneyAmount:
                indexWinners.clear()
                indexWinners.append(i)
        


        if len(indexWinners) < 1:
            endGameMessage += "Winner are \n"
            for banditIndex in indexWinners:
                endGameMessage += self.bandits[banditIndex].formatedStr() + '\n'
        elif len(indexWinners) == 1:
            endGameMessage += "Winner is \n"
            endGameMessage += self.bandits[0].formatedStr() + '\n'
        

        self.createEndGameMenuCanvas(endGameMessage)











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
        bandit.imgHead = Game.createBanditPng(widthIcon, heightIcon, COLORS[bandit.color], justHead=True)
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
                        yOffsetButin -= (heightWagon*0.005) * (i%3) #réhaussement de 0.005% * 0 ou 1 ou 2

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

        # FIN === ON DESSINE LES BUTINS DANS LES WAGONS ======================


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
        widthCharacter = int(widthCharacter*1.2)
        heightCharacter = int(heightCharacter*1.2)
        self.imgMarshal = Game.createLoadedImg(widthCharacter,heightCharacter, Game.imgMarshall)

        for wagon in self.wagons :
            if wagon.marshall == True:
                xOffsetMarshall = widthWagon + (widthWagon//2) - (widthCharacter//2)
                yOffsetMarshall = ((heightWagon-heightCharacter) - (heightWagon * 0.3)) * 0.9 #réhaussement de 20%

                xMarshallPosition = (wagon.xPosition * widthWagon) + xOffsetMarshall
                yMarshallPosition = heightWagon + yOffsetMarshall


                img = self.playSpace.create_image(xMarshallPosition, yMarshallPosition, image=self.imgMarshal, anchor="nw")
                self.imgsOnCanvasPlaySpace.append(img)
                break
    
        # FIN === ON DESSINE LE MARSHALL ======================



        #ON DESSINE LES INVENTAIRES DES BANDITS ==============================

        for i, bandit in enumerate(self.bandits):
            self.createInventoryCanvas(bandit, widthCanvas, heightCanvas, i)

        #FIN === ON DESSINE LES INVENTAIRES DES BANDITS ======================
    

    @staticmethod
    def createLoadedImg(width, height, loadedImg):
        loadedImg = loadedImg.resize((width, height))
        return ImageTk.PhotoImage(loadedImg)


    @staticmethod
    def createBanditPng(width, height, color, justHead=False):
        body = Game.imgBody
        details = Game.imgDetails

        if justHead:
            body = Game.imgIconBanditBody
            details = Game.imgIconBanditDetails
            body = body.resize((width, height))
            details = details.resize((width, height))
        else:
            body = Game.imgBody
            details = Game.imgDetails
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


    def formatedStr(self):
        somme = 0
        for butin in self.butins:
            somme += butin.value

        return f'{self.name} ({somme}$ in {len(self.butins)} butins)\n'


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

        
        self.game.insertTextInLog(f"{self.name} moves {action}\n",self.color)

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









class Action(Frame):
    def __init__(self, game:Game, actionsFrame:Frame, value:str, column:int):
        super().__init__(actionsFrame, bg='orange')
        self.game:Game = game
        self.column:int = column
        self.value:str = value

        self.action = Button(self, text=value, command=self.remove, bg=WIDGET_COLORS['sand'], border=0, highlightthickness=0, activebackground=WIDGET_COLORS['redLight'])
        self.left = Button(self, text="<-", command=self.moveLeft, bg=WIDGET_COLORS['sand'], border=0, highlightthickness=0, activebackground=WIDGET_COLORS['redLight'])
        self.right = Button(self, text="->", command=self.moveRight, bg=WIDGET_COLORS['sand'], border=0, highlightthickness=0, activebackground=WIDGET_COLORS['redLight'])


        if not value == 'osef':
            self.widthAction = (game.playSpace.winfo_width()//4) // MAX_ACTIONS
            self.heightAction = int(game.playSpace.winfo_height()*0.15)
            self.setImgAction()
            self.imgLeft = Game.createLoadedImg(self.widthAction//2, int(self.heightAction//3), self.game.imgLeft)
            self.imgRight = Game.createLoadedImg(self.widthAction//2, int(self.heightAction//3), self.game.imgRight)

            self.action.config(image=self.imgAction)
            self.left.config(image=self.imgLeft)
            self.right.config(image=self.imgRight)


        self.action.grid(columnspan=2, sticky='ew')
        self.left.grid(row=1)
        self.right.grid(row=1, column=1)





    def chooseTheGoodImg(self):
        if self.value == 'right':
            return self.game.imgRight
        elif self.value == 'left':
            return self.game.imgLeft
        elif self.value == 'up':
            return self.game.imgUp
        elif self.value == 'down':
            return self.game.imgDown
        elif self.value == 'shoot':
            return self.game.imgShoot
        elif self.value == 'rob':
            return self.game.imgRob


    def setImgAction(self):
        self.action.destroy()
        self.imgAction = Game.createLoadedImg(self.widthAction, int((self.heightAction//3)*2), self.chooseTheGoodImg())
        self.action = Button(self, text=self.value, command=self.remove, image=self.imgAction, bg=WIDGET_COLORS['sand'], border=0, highlightthickness=0, activebackground=WIDGET_COLORS['redLight'])
        self.action.grid(row=0, columnspan=2, sticky='ew')


    def remove(self):
        for action in self.game.tempActions:
            if action == self:
                self.game.removeAction(self)
                return


    #swap value between this Action and the right one
    def moveRight(self):
        if (self.column >= MAX_ACTIONS-1) or (self.column >= len(self.game.tempActions)-1):
            print("Can't move right")
            return


        for i, action in enumerate(self.game.tempActions):
            if action == self:
                actionTo = self.game.tempActions[i+1]

                #swap values
                self.value, actionTo.value = actionTo.value, self.value
                # self.action, actionTo.action = actionTo.action, self.action

                #update Action(s)
                self.update()
                actionTo.update()
                self.setImgAction()
                actionTo.setImgAction()



    #swap value between this Action and the left one
    def moveLeft(self):
        if self.column <= 0:
            print("Can't move left")
            return


        for i, action in enumerate(self.game.tempActions):
            if action == self:
                actionTo = self.game.tempActions[i-1]

                 #swap values
                self.value, actionTo.value = actionTo.value, self.value

                #update Action(s)
                self.update()
                actionTo.update()
                self.setImgAction()
                actionTo.setImgAction()



    def update(self):
        self.action.config(text=self.value)

















mon_jeu = Game()

mon_jeu.mainloop()
