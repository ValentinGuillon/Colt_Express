from tkinter import *
import random
import modules.saveGestion as saveGestion
import modules.images as images
import modules.widgets as widgets
import modules.tools as tools





def returnToMainMenu(window, canvas:list[Canvas]):
    for cnv in canvas:
        cnv.destroy()
    createMainMenu(window)




#resizes the background of Menus when the window is resized
def resizeMenusBackground(window, canvas:Canvas):
    window.img = images.createLoadedImg(canvas.winfo_width(), canvas.winfo_height(), images.imgPaysage)
    canvas.create_image(0, 0, image=window.img, anchor='nw')


def loadingBarProgess(loadingScreen, label, step=6):
    if step == 6:
        label.config(text='                                           ')
        loadingScreen.after(ms=random.randint(300, 400), func=lambda:loadingBarProgess(loadingScreen, label, step=step-1))
    elif step == 5:
        label.config(text='=======                                    ')
        loadingScreen.after(ms=random.randint(300, 600), func=lambda:loadingBarProgess(loadingScreen, label, step=step-1))
    elif step == 4:
        label.config(text='=============                              ')
        loadingScreen.after(ms=random.randint(500, 550), func=lambda:loadingBarProgess(loadingScreen, label, step=step-1))
    elif step == 3:
        label.config(text='=======================                    ')
        loadingScreen.after(ms=random.randint(100, 150), func=lambda:loadingBarProgess(loadingScreen, label, step=step-1))
    elif step == 2:
        label.config(text='================================           ')
        loadingScreen.after(ms=random.randint(200, 300), func=lambda:loadingBarProgess(loadingScreen, label, step=step-1))
    elif step == 1:
        label.config(text='===========================================')
        loadingScreen.after(ms=500, func=lambda:loadingBarProgess(loadingScreen, label, step=step-1))
    else:
        loadingScreen.destroy()


def createLoadingScreen(window):

    #menu Canvas
    window.loadingCanvas = Canvas(window, bg=window.WIDGET_COLORS['sand'])
    window.loadingCanvas.grid(row=0, column=0, columnspan=2, sticky='nsew')

    #weight of empty rows/columns
    for i in [0, 4]:
        window.loadingCanvas.columnconfigure(i, weight=1)
    for i in [1, 3]:
        window.loadingCanvas.columnconfigure(i, weight=4)
    for i in [0, 4]:
        window.loadingCanvas.rowconfigure(i, weight=3)
    window.loadingCanvas.rowconfigure(2, weight=1)

    #widgets creation
    loadingProgessText = '3'
    window.title = Label(window.loadingCanvas, text='FAKE LOADING', font=60)
    window.loadingProgress = Label(window.loadingCanvas, text=loadingProgessText, justify='center', font=("Consolas", 10))

    #widgets default configuration
    widgets.configWidgets(window, 'Label', [window.title, window.loadingProgress])
    window.title.config(bg=window.WIDGET_COLORS['sand'])
    window.loadingProgress.config(bg=window.WIDGET_COLORS['train'], fg=window.WIDGET_COLORS['sand'])

    #widgets placement
    window.title.grid(row=1, column=2)
    window.loadingProgress.grid(row=3, column=1, columnspan=3)

    loadingBarProgess(window.loadingCanvas, window.loadingProgress)



def createMainMenu(window):
    #menu Canvas
    window.canvasMainMenu = Canvas(window)
    window.canvasMainMenu.grid(columnspan=2, sticky='nsew')
    window.canvasMainMenu.bind('<Configure>', lambda e: resizeMenusBackground(window, window.canvasMainMenu))


    #weight empty rows/columns
    for i in [0, 4]:
        window.canvasMainMenu.columnconfigure(i, weight = 1)
    for i in [1, 3]:
        window.canvasMainMenu.columnconfigure(i, weight = 1)
    for i in [0, 9]:
        window.canvasMainMenu.rowconfigure(i, weight = 3)

    window.canvasMainMenu.rowconfigure(2, weight = 2)
    window.canvasMainMenu.rowconfigure(5, weight = 1)
    window.canvasMainMenu.rowconfigure(7, weight = 1)

    #widgets creations
    window.title = Label(window.canvasMainMenu, text='COLT ZEʁMA', font=60)
    window.btnNew = Button(window.canvasMainMenu, text='New', command=lambda:createNewGameMenu(window))
    window.btnLoad = Button(window.canvasMainMenu, text='Load', command=lambda:createLoadGameMenu(window))
    window.btncredits = Button(window.canvasMainMenu, text='Credits', command=lambda:createCreditsMenu(window))
    window.btnExit = Button(window.canvasMainMenu, text='Exit', command=window.destroy)


    #widgets configuration
    widgets.configWidgets(window, 'Label', [window.title])
    widgets.configWidgets(window, 'Button', [window.btnNew, window.btnLoad, window.btncredits, window.btnExit])

    if saveGestion.saveIsEmpty():
        window.btnLoad.config(state='disabled')
    else:
        window.btnLoad.config(state='normal')

    #widgets placement
    window.title.grid(column=1, row=1, columnspan=3, sticky='nsew', ipady=10)
    window.btnNew.grid(column=2, row=3, sticky='nsew')
    window.btnLoad.grid(column=2, row=4, sticky='nsew')
    window.btncredits.grid(column=2, row=6, sticky='nsew')
    window.btnExit.grid(column=2, row=8, sticky='nsew')





def createCreditsMenu(window):
    window.canvasMainMenu.destroy()

    #menu Canvas
    window.creditsCanvas = Canvas(window)
    window.creditsCanvas.grid(columnspan=2, sticky='nsew')
    window.creditsCanvas.bind('<Configure>', lambda e: resizeMenusBackground(window, window.creditsCanvas))

    #weight of empty rows/columns
    for i in [0, 2]:
        window.creditsCanvas.columnconfigure(i, weight=1)
    for i in [0, 6]:
        window.creditsCanvas.rowconfigure(i, weight=3)
    window.creditsCanvas.rowconfigure(2, weight=2)
    window.creditsCanvas.rowconfigure(4, weight=1)

    #widgets creation
    creditText = 'Created by\n\nMaria MESSAOUD-NACER\nValentin GUILLON\n\n\nBased on the Game\n"Colt Express"'
    window.title = Label(window.creditsCanvas, text='CREDITS', font=60)
    window.labelCredits = Label(window.creditsCanvas, text=creditText, justify='center')
    window.creditsBtnExit = Button(window.creditsCanvas, text='Main Menu', command=lambda:returnToMainMenu(window, [window.creditsCanvas]))

    #widgets default configuration
    widgets.configWidgets(window, 'Label', [window.title, window.labelCredits])
    widgets.configWidgets(window, 'Button', [window.creditsBtnExit])

    #widgets placement
    window.title.grid(column=1, row=1, sticky='nsew', ipady=10)
    window.labelCredits.grid(row=3, column=1, pady=15, ipadx=15, ipady=10)
    window.creditsBtnExit.grid(row=5, column=1, pady=15)







def createLoadGameMenu(window):
    #afficher un aperçu de ce que contient la sauvegarde
    window.canvasMainMenu.destroy()

    #menuCanvas
    window.loadGameCanvas = Canvas(window)
    window.loadGameCanvas.grid(columnspan=2, sticky='nsew')
    window.loadGameCanvas.bind('<Configure>', lambda e: resizeMenusBackground(window, window.loadGameCanvas))

    #weight empty rows/columns
    for i in [0, 6]:
        window.loadGameCanvas.columnconfigure(i, weight = 4)
    for i in [1, 5]:
        window.loadGameCanvas.columnconfigure(i, weight = 3)
    for i in [2, 4]:
        window.loadGameCanvas.columnconfigure(i, weight = 1)
    window.loadGameCanvas.columnconfigure(3, weight = 1)

    for i in [0, 8]:
        window.loadGameCanvas.rowconfigure(i, weight = 4)
    window.loadGameCanvas.rowconfigure(2, weight = 3)
    window.loadGameCanvas.rowconfigure(4, weight = 1)
    window.loadGameCanvas.rowconfigure(6, weight = 2)


    #Canvas for Label(s) and Entry(s)
    window.gameInfosSpace = Frame(window.loadGameCanvas, bg=window.WIDGET_COLORS['road'])
    window.gameInfosSpace.grid(row=3, column=1, columnspan=2, sticky='news', ipady=10)
    window.playersInfosSpace = Frame(window.loadGameCanvas, bg=window.WIDGET_COLORS['road'])
    window.playersInfosSpace.grid(row=3, column=4, columnspan=2, sticky='news', ipady=10)


    #load saved game's data
    _, nbTurns, currentTurn, nbWagons, maxActions, _, preparation, _, tempBandits, tempButins = saveGestion.loadSave()

    #on compte les butins de chaque bandits
    nbButinsOfBandits = []
    for banditElements in tempBandits:
        name = banditElements[0]
        ammount = 0
        for butinElements in tempButins:
            if butinElements[3] == name:
                ammount += 1
        nbButinsOfBandits.append(ammount)

    #weight empty rows/columns
        #game's datas Space
    for i in [0, 4]:
        window.gameInfosSpace.columnconfigure(i, weight = 1)
    window.gameInfosSpace.columnconfigure(2, weight = 3)
    for i in [0, 2, 7]:
        window.gameInfosSpace.rowconfigure(i, weight = 1)

        #players' infos Space
    for i in [0, 4]:
        window.playersInfosSpace.columnconfigure(i, weight = 1)
    window.playersInfosSpace.columnconfigure(2, weight = 3)
    for i in [0, 2, 2+len(tempBandits)+1]:
        window.playersInfosSpace.rowconfigure(i, weight = 1)


    #widgets creation
    window.title = Label(window.loadGameCanvas, text='LOAD GAME', font=60)
    window.launchLoadedGame = Button(window.loadGameCanvas, text='Load', command=lambda:window.startGame(window.loadGameCanvas, loadSave=True))
    window.btnExitNewGameMenu = Button(window.loadGameCanvas, text='Main Menu', command=lambda:returnToMainMenu(window, [window.loadGameCanvas]))

        #game's datas Space
    window.titleGameDatas = Label(window.gameInfosSpace, text="GAME'S INFOS")
    window.labelNbTurns = Label(window.gameInfosSpace, text=f'Turn {currentTurn}/{nbTurns}')
    window.labelPhase = Label(window.gameInfosSpace)
    window.labelNbWagons = Label(window.gameInfosSpace, text=f'{nbWagons} wagons')
    window.labelNbActions = Label(window.gameInfosSpace, text=f'{maxActions} actions by turns')

        #players' infos Space
    window.titlePlayersInfos = Label(window.playersInfosSpace, text='PLAYERS')

    window.loadGamePlayersLabels:list[Label] = []
    for i, banditElements in enumerate(tempBandits):
        #banditElement = [<name>, <color>, <x>, <y>, <action>..., <bullets>]
        name = banditElements[0]
        nbButins = nbButinsOfBandits[i]
        nbBullets = banditElements[-1]
        text = f'{name}: {nbButins} butins, {nbBullets} bullets'

        labelPlayer = Label(window.playersInfosSpace, text=text)
        widgets.configWidgets(window, 'Label', [labelPlayer])
        color = tools.convertToHtml(window.COLORS[banditElements[1]])
        labelPlayer.config(fg=color, bg=window.WIDGET_COLORS['sand'])


        window.loadGamePlayersLabels.append(labelPlayer)


    #widgets default configurations
    if preparation:
        window.labelPhase.config(text='Phase: Preparation')
    else:
        window.labelPhase.config(text='Phase: Action')

    widgets.configWidgets(window, 'Label', [window.title, window.titleGameDatas, window.labelNbTurns, window.labelPhase, window.labelNbWagons, window.labelNbActions, window.titlePlayersInfos])
    widgets.configWidgets(window, 'Button', [window.launchLoadedGame, window.btnExitNewGameMenu])


    #widgets placement
    window.title.grid(row=1, column=1, columnspan=5, sticky='nsew', ipady=10)
    window.launchLoadedGame.grid(row=5, column=2, columnspan=3, sticky='ew')
    window.btnExitNewGameMenu.grid(row=7, column=2, columnspan=3, sticky='ew')

        #game's datas Space
    window.titleGameDatas.grid(row=1, column=1, columnspan=3, sticky='news')
    window.labelNbTurns.grid(row=3, column=2, sticky='news')
    window.labelPhase.grid(row=4, column=2, sticky='news')
    window.labelNbWagons.grid(row=5, column=2, sticky='news')
    window.labelNbActions.grid(row=6, column=2, sticky='news')

        #players' infos Space
    window.titlePlayersInfos.grid(row=1, column=1, columnspan=3, sticky='news')

    add = 2
    for i, label in enumerate(window.loadGamePlayersLabels, start=1):
        label.grid(row=add+i, column=2, sticky='news')










def createNewGameMenu(window):
    window.canvasMainMenu.destroy()

    #menuCanvas
    window.newGameCanvas = Canvas(window)
    window.newGameCanvas.grid(columnspan=2, sticky='nsew')
    window.newGameCanvas.bind('<Configure>', lambda e: resizeMenusBackground(window, window.newGameCanvas))

    #weight empty rows/columns
    for i in [0, 4]:
        window.newGameCanvas.columnconfigure(i, weight = 4)
    for i in [1, 3]:
        window.newGameCanvas.columnconfigure(i, weight = 1)
    for i in [0, 8]:
        window.newGameCanvas.rowconfigure(i, weight = 4)
    window.newGameCanvas.rowconfigure(2, weight = 3)
    window.newGameCanvas.rowconfigure(4, weight = 1)
    window.newGameCanvas.rowconfigure(6, weight = 2)


    #Canvas for Label(s) and Entry(s)
    window.labEntrySpace = Frame(window.newGameCanvas, bg=window.WIDGET_COLORS['road'])
    window.labEntrySpace.grid(row=3, column=1, columnspan=3, sticky='news', ipady=10)

    #weight empty rows/columns
    for i in [0, 6]:
        window.labEntrySpace.columnconfigure(i, weight = 1)
    for i in [0, 8]:
        window.labEntrySpace.rowconfigure(i, weight = 1)

    #variable for game's datas
    nbPlayers = IntVar()
    nbWagons = IntVar()
    nbTurns = IntVar()
    nbActions = IntVar()
    minButins = IntVar()
    maxButins = IntVar()
    nbBullets = IntVar()
    nbPlayers.set(4)
    nbWagons.set(4)
    nbTurns.set(6)
    nbActions.set(6)
    minButins.set(1)
    maxButins.set(4)
    nbBullets.set(12)

    #widgets creation
    window.title = Label(window.newGameCanvas, text='NEW GAME', font=60)

    window.labelNbPlayers = Label(window.labEntrySpace, text=' joueurs')
    window.labelNbWagons = Label(window.labEntrySpace, text=' wagons')
    window.labelNbTurns = Label(window.labEntrySpace, text=' tours')
    window.labelNbActions = Label(window.labEntrySpace, text=' actions par tour')
    window.labelMinButins = Label(window.labEntrySpace, text=' butins par wagon (min)')
    window.labelMaxButins = Label(window.labEntrySpace, text=' butins par wagon (max)')
    window.labelNbBullets = Label(window.labEntrySpace, text=' bullets')

    window.entryNbPlayers = Entry(window.labEntrySpace, textvariable=nbPlayers)
    window.entryNbWagons = Entry(window.labEntrySpace, textvariable=nbWagons)
    window.entryNbTurns = Entry(window.labEntrySpace, textvariable=nbTurns)
    window.entryNbActions = Entry(window.labEntrySpace, textvariable=nbActions)
    window.entryMinButins = Entry(window.labEntrySpace, textvariable=minButins)
    window.entryMaxButins = Entry(window.labEntrySpace, textvariable=maxButins)
    window.entryNbBullets = Entry(window.labEntrySpace, textvariable=nbBullets)

    window.launchNewGame = Button(window.newGameCanvas, text='Start', command=lambda:window.startGame(window.newGameCanvas, nbPlayers.get(), nbWagons.get(), nbTurns.get(), nbActions.get(), minButins.get(), maxButins.get(), nbBullets.get()))
    window.btnExitNewGameMenu = Button(window.newGameCanvas, text='Return to Main Menu', command=lambda:returnToMainMenu(window, [window.newGameCanvas]))

    #widgets default configurations
    widgets.configWidgets(window, 'Label', [window.title, window.labelNbPlayers, window.labelNbWagons, window.labelNbTurns, window.labelNbActions, window.labelMinButins, window.labelMaxButins, window.labelNbBullets])
    widgets.configWidgets(window, 'Entry', [window.entryNbPlayers, window.entryNbWagons, window.entryNbTurns, window.entryNbActions, window.entryMinButins, window.entryMaxButins, window.entryNbBullets])
    widgets.configWidgets(window, 'Button', [window.launchNewGame, window.btnExitNewGameMenu])


    #widgets placement
    window.title.grid(row=1, column=1, columnspan=3, sticky='nsew', ipady=10)

    window.labelNbPlayers.grid(row=1, column=3, columnspan=2, sticky='w', pady=2)
    window.labelNbWagons.grid(row=2, column=3, columnspan=2, sticky='w', pady=2)
    window.labelNbTurns.grid(row=3, column=3, columnspan=2, sticky='w', pady=2)
    window.labelNbActions.grid(row=4, column=3, columnspan=2, sticky='w', pady=2)
    window.labelMinButins.grid(row=5, column=3, columnspan=2, sticky='w', pady=2)
    window.labelMaxButins.grid(row=6, column=3, columnspan=2, sticky='w', pady=2)
    window.labelNbBullets.grid(row=7, column=3, columnspan=2, sticky='w', pady=2)

    window.entryNbPlayers.grid(row=1, column=1, columnspan=2, sticky='e', pady=2)
    window.entryNbWagons.grid(row=2, column=1, columnspan=2, sticky='e', pady=2)
    window.entryNbTurns.grid(row=3, column=1, columnspan=2, sticky='e', pady=2)
    window.entryNbActions.grid(row=4, column=1, columnspan=2, sticky='e', pady=2)
    window.entryMinButins.grid(row=5, column=1, columnspan=2, sticky='e', pady=2)
    window.entryMaxButins.grid(row=6, column=1, columnspan=2, sticky='e', pady=2)
    window.entryNbBullets.grid(row=7, column=1, columnspan=2, sticky='e', pady=2)

    window.launchNewGame.grid(row=5, column=2, sticky='ew')
    window.btnExitNewGameMenu.grid(row=7, column=2, sticky='ew')









def createEndGameMenu(window, indexWinners:list[int], playersNameAndResult:list[list[str]]):
    window.playSpace.destroy()
    window.menuSpace.destroy()

    #menu Canvas
    window.endGameMenuCanvas = Canvas(window, bg='red')
    window.endGameMenuCanvas.grid(columnspan=2, sticky='nsew')
    window.endGameMenuCanvas.bind('<Configure>', lambda e: resizeMenusBackground(window, window.endGameMenuCanvas))

    #weight empty rows/columns
    for i in [0, 4]:
        window.endGameMenuCanvas.columnconfigure(i, weight=4)
    for i in [1, 3]:
        window.endGameMenuCanvas.columnconfigure(i, weight=1)
    for i in [0, 6]:
        window.endGameMenuCanvas.rowconfigure(i, weight=4)
    window.endGameMenuCanvas.rowconfigure(2, weight=2)
    window.endGameMenuCanvas.rowconfigure(4, weight=1)

    #Canvas for Label(s) and Entry(s)
    window.resultSpace = Frame(window.endGameMenuCanvas, bg=window.WIDGET_COLORS['road'])
    window.resultSpace.grid(row=1, column=1, columnspan=3, sticky='news', ipady=10)
    nbRows = 1 + 1 + len(indexWinners) + 1 + 1 + window.NB_JOUEURS + 1 #empty + winnerLabel + Xlabels + empty + resultsLabel + empty

    #weight empty rows/columns
    for i in [0, 5]:
        window.resultSpace.columnconfigure(i, weight = 1)
    for i in [0, nbRows]:
        window.resultSpace.rowconfigure(i, weight = 2)
    window.resultSpace.rowconfigure((2 + len(indexWinners)) - 1, weight=2)


    #widgets creations
    nameLabels:list[Label] = []
    resultLabels:list[Label] = []

    window.winnerLabel = Label(window.resultSpace, justify=CENTER)
    window.ResultLabel = Label(window.resultSpace, text='Results', justify=CENTER)

    for iWinner in indexWinners:
        nameLabel = Label(window.resultSpace, text=playersNameAndResult[0][iWinner], justify='right')
        resultLabel = Label(window.resultSpace, text=playersNameAndResult[1][iWinner], justify='left')
        nameLabels.append(nameLabel)
        resultLabels.append(resultLabel)
    
    for iPlayer in range(window.NB_JOUEURS):
        nameLabel = Label(window.resultSpace, text=playersNameAndResult[0][iPlayer], justify='right')
        resultLabel = Label(window.resultSpace, text=playersNameAndResult[1][iPlayer], justify='left')
        nameLabels.append(nameLabel)
        resultLabels.append(resultLabel)


    window.btnExitToMainMenu = Button(window.endGameMenuCanvas, text='Return to Main Menu', command=lambda:returnToMainMenu(window, [window.endGameMenuCanvas]))
    window.btnExit = Button(window.endGameMenuCanvas, text='Exit', command=window.destroy)


    #widgets configuration
    if len(indexWinners) > 1:
        window.winnerLabel.config(text='Winners are')
    else:
        window.winnerLabel.config(text='Winner is')

    widgets.configWidgets(window, 'Label', [window.winnerLabel, window.ResultLabel, *nameLabels, *resultLabels])
    widgets.configWidgets(window, 'Button', [window.btnExitToMainMenu, window.btnExit])

    window.winnerLabel.config(bg=window.WIDGET_COLORS['train'], fg=window.WIDGET_COLORS['road'])
    window.ResultLabel.config(bg=window.WIDGET_COLORS['train'], fg=window.WIDGET_COLORS['road'])


    #widgets placement
    window.winnerLabel.grid(row=1, column=1, columnspan=2, sticky='news')
    window.ResultLabel.grid(row=2+len(indexWinners), column=1, columnspan=2, sticky='news')

    add = 2
    for indexLabel in range(0, len(indexWinners)):
        nameLabels[indexLabel].grid(row=add+indexLabel, column=1, sticky='e')
        resultLabels[indexLabel].grid(row=add+indexLabel, column=2, sticky='w')

    add += window.NB_JOUEURS + 2
    for indexLabel in range(0, window.NB_JOUEURS):
        nameLabels[indexLabel + len(indexWinners)].grid(row=add+indexLabel, column=1, sticky='e')
        resultLabels[indexLabel + len(indexWinners)].grid(row=add+indexLabel, column=2, sticky='w')
    

    window.btnExitToMainMenu.grid(column=2, row=3, sticky='nsew')
    window.btnExit.grid(column=2, row=5, sticky='nsew')





