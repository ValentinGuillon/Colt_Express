import pygame
from pygame import mixer as mix
from typing import Literal
import random
import time


PATH = 'sound/'

#musics
MUSIC_MAIN = PATH + 'main-menu_valentin.wav'
MUSIC_MARIA = PATH + 'maria_s_rush.wav'

#sounds
    #shoots
SOUND_SHOOT = PATH + 'sounds/sure/shoot/Fallout 4/Fire_2D.wav'
# SOUND_SHOOTMARSHALL
# SOUND_MAGEMPTY

    #menus
SOUND_CONFIRM = PATH + 'sounds/maybe/reload/Fallout 4/Reload_Charge_01.wav' #crop
SOUND_NEWGAME = PATH + 'sounds/maybe/reload/Fallout 4/Reload_BoltOpen_01.wav'
SOUND_LOADGAME = PATH + 'sounds/maybe/reload/Fallout 4/Reload_BoltClose_01.wav'
SOUND_STARTGAME = PATH + 'sounds/maybe/reload/Fallout 4/EquipUp_01.wav'
SOUND_RETURNMAINMENU = PATH + 'sounds/maybe/bruitage/Western Outlaw Wanted Dead or Alive/THICKMETALIMPACT2.WAV' #change
SOUND_LOADING = PATH + 'sounds/maybe/bruitage/Western Outlaw Wanted Dead or Alive/HORSES_GALLOPING.WAV'

    #butin
SOUND_LOOTBUTIN = PATH + 'sounds/maybe/butin/Lucky Luke Western Fever/cashier.wav'
SOUND_LOOTMAGOT = PATH + 'sounds/maybe/butin/Lucky Luke Western Fever/collect_hat.wav'

SOUND_STEPSIDE1 = PATH + 'sounds/maybe/walk/Western Outlaw Wanted Dead or Alive/FS_WOOD1.WAV'
SOUND_STEPSIDE2 = PATH + 'sounds/maybe/walk/Western Outlaw Wanted Dead or Alive/FS_WOOD2.WAV'
SOUND_STEPSIDE3 = PATH + 'sounds/maybe/walk/Western Outlaw Wanted Dead or Alive/FS_WOOD3.WAV'
SOUND_STEPSIDE4 = PATH + 'sounds/maybe/walk/Western Outlaw Wanted Dead or Alive/FS_WOOD4.WAV'
SOUND_STEPUPDOWN1 = PATH + 'sounds/maybe/walk/Western Outlaw Wanted Dead or Alive/WLADDER1.WAV'
SOUND_STEPUPDOWN2 = PATH + 'sounds/maybe/walk/Western Outlaw Wanted Dead or Alive/WLADDER2.WAV'
SOUND_STEPUPDOWN3 = PATH + 'sounds/maybe/walk/Western Outlaw Wanted Dead or Alive/WLADDER3.WAV'


pygame.init()

musicMain = mix.music.load(MUSIC_MAIN)
musicMaria = mix.music.load(MUSIC_MARIA)


soundShoot = mix.Sound(SOUND_SHOOT)

soundConfirm = mix.Sound(SOUND_CONFIRM) #quand on appuie sur un bouton qui propose oui/non

soundNewGame = mix.Sound(SOUND_NEWGAME)
soundLoadGame = mix.Sound(SOUND_LOADGAME)
soundStartGame = mix.Sound(SOUND_STARTGAME)
soundReturnMainMenu = mix.Sound(SOUND_RETURNMAINMENU)
soundLoading = mix.Sound(SOUND_LOADING)

soundLootButin = mix.Sound(SOUND_LOOTBUTIN)
soundLootMagot = mix.Sound(SOUND_LOOTMAGOT)

soundStepSide1 = mix.Sound(SOUND_STEPSIDE1)
soundStepSide2 = mix.Sound(SOUND_STEPSIDE2)
soundStepSide3 = mix.Sound(SOUND_STEPSIDE3)
soundStepSide4 = mix.Sound(SOUND_STEPSIDE4)
soundStepUpDown1 = mix.Sound(SOUND_STEPUPDOWN1)
soundStepUpDown2 = mix.Sound(SOUND_STEPUPDOWN2)
soundStepUpDown3 = mix.Sound(SOUND_STEPUPDOWN3)


sounds:mix.Sound = []
sounds.append(soundShoot)
sounds.append(soundConfirm)
sounds.append(soundNewGame)
sounds.append(soundLoadGame)
sounds.append(soundStartGame)
sounds.append(soundReturnMainMenu)
sounds.append(soundLoading)
sounds.append(soundLootButin)
sounds.append(soundLootMagot)
sounds.append(soundStepSide1)
sounds.append(soundStepSide2)
sounds.append(soundStepSide3)
sounds.append(soundStepSide4)
sounds.append(soundStepUpDown1)
sounds.append(soundStepUpDown2)
sounds.append(soundStepUpDown3)










def playMusic(name:Literal['main', 'maria']):
    if not name in ['main', 'maria']:
        print(f'ERROR: in audios.py, in playMusic:\n    "{name}" doesn\'t exist \n    (expected: main, maria)')
        exit()

    if name == 'main':
        mix.music.load(MUSIC_MAIN)
        mix.music.play(-1)
    elif name == 'maria':
        mix.music.load(MUSIC_MARIA)
        mix.music.play(-1)


def stopMusic(fadeOut_ms):
    # mix.music.stop()
    mix.music.fadeout(fadeOut_ms)


def reduceMusicVolume(volume):
    newVolume = (volume / 100) * 30 #reduction to 30% of actual value
    mix.music.set_volume(newVolume/100)


def resetMusicVolume(volume):
    mix.music.set_volume(volume/100)




def playSound(name:Literal['shoot', 'confirm', 'newGame', 'loadGame', 'startGame', 'returnMainMenu', 'loading', 'butin', 'magot', 'stepSide', 'stepUpDown']):
    if not name in ['shoot', 'confirm', 'newGame', 'loadGame', 'startGame', 'returnMainMenu', 'loading', 'butin', 'magot', 'stepSide', 'stepUpDown']:
        print(f'ERROR: in audios.py, in playSound:\n    "{name}" doesn\'t exist \n    (expected: shoot, confirm, newGame, loadGame, startGame, returnMainMenu, loading, butin, magot, stepSide, stepUpDown)')
        exit()

    if name == 'shoot':
        soundShoot.play()
    elif name == 'confirm':
        soundConfirm.play()
    elif name == 'newGame':
        soundNewGame.play()
    elif name == 'loadGame':
        soundLoadGame.play()
    elif name == 'startGame':
        soundStartGame.play()
    elif name == 'returnMainMenu':
        soundReturnMainMenu.play()
    elif name == 'loading':
        soundLoading.play()
        soundLoading.fadeout(5500)
        
    elif name == 'butin':
        soundLootButin.play()
    elif name == 'stepSide':
        choice = random.randint(1, 4)
        if choice == 1:
            soundStepSide1.play()
        elif choice == 2:
            soundStepSide2.play()
        elif choice == 3:
            soundStepSide3.play()
        elif choice == 4:
            soundStepSide4.play()
    elif name == 'stepUpDown':
        choice = random.randint(1, 3)
        if choice == 1:
            soundStepUpDown1.play()
        elif choice == 2:
            soundStepUpDown2.play()
        elif choice == 3:
            soundStepUpDown3.play()




def stopSoundLoading():
    soundLoading.stop()


def setVolume(type:Literal['music', 'sounds'], value:int):
    if not type in ['music', 'sounds']:
        print(f'ERROR: in audios.py, in setVolume:\n    "{type}" doesn\'t exist \n    (expected: music, sounds)')
        exit()

    if type == 'music':
        mix.music.set_volume(value/100)
    elif type == 'sounds':
        for sound in sounds:
            mix.Sound.set_volume(sound, value/100)




def setAudioVolume(volume):
    setVolume('music', volume)
    setVolume('sounds', volume)








"""


def printCommands():
    print('\nCommands :')
    print('\tfade')
    print('\tvolume music, volume sounds')
    print('\tmain, main stop')
    print('\tmaria, maria stop')
    print('\tpause, play')
    print('\tnew, load, start')
    print('\tconfirm')
    print('\tshoot')
    print('\tbutin, magot')
    print('\tloading, loading stop')
    print('\tstep side, step up down')


#test
while 1:
    printCommands()
    userInput = input(">")
    if userInput == 'exit':
        break


    if userInput == 'fade':
        mix.fadeout(3000)
        print(' audio fade out ...')


    elif userInput == 'volume music':
        print("How much ? (max 100) (or 'cancel')", end='')
        while 1:
            volume = input('\n>')
            if volume == 'cancel':
                break

            volume = int(volume)
            if volume >=0 and volume <= 100:
                break

        if isinstance(volume, int):
            setVolume('music', volume)
            print(f' music volume : {volume}...')


    elif userInput == 'volume sounds':
        print("How much ? (max 100) (or 'cancel')", end='')
        while 1:
            volume = input('\n>')
            if volume == 'cancel':
                break

            volume = int(volume)
            if volume >=0 and volume <= 100:
                break

        if isinstance(volume, int):
            setVolume('sounds', volume)
            print(f' sounds volume : {volume}...')


    elif userInput == 'main':
        playMusic('main')
        print(' music main : play..')
    elif userInput == 'main stop':
        mix.music.stop()
        print(' music main : stop...')

    elif userInput == 'maria':
        playMusic('maria')
        print(' music maria : play..')
    elif userInput == 'maria stop':
        mix.music.stop()
        print(' music maria : stop...')
    
    elif userInput == 'pause':
        mix.music.pause()
        print(' music : pause...')
    elif userInput == 'play':
        mix.music.unpause()
        print(' music : unpause...')




    elif userInput == 'new':
        playSound('newGame')
        print(' audio new game...')
    elif userInput == 'load':
        playSound('loadGame')
        print(' audio load game...')
    elif userInput == 'start':
        playSound('startGame')
        print(' audio start game...')

    elif userInput == 'loading':
        playSound('loading')
        print(' audio load game...')
    elif userInput == 'loading stop':
        stopSoundLoading()
        print(' audio start game...')


    elif userInput == 'confirm':
        playSound('confirm')
        print(' audio confirm ?...')


    elif userInput == 'shoot':
        playSound('shoot')
        print(' audio shoot...')

    elif userInput == 'butin':
        playSound('butin')
        print(' audio loot butin...')
    elif userInput == 'magot':
        playSound('magot')
        print(' audio loot magot...')

    elif userInput == 'step side':
        playSound('stepSide')
        for _ in range(4):
            time.sleep(0.3)
            playSound('stepSide')
            # Label.after(ms=300, func=lambda:playSound('stepSide'))
        print(' audio step side...')
    elif userInput == 'step up down':
        playSound('stepUpDown')
        for _ in range(3):
            time.sleep(0.5)
            playSound('stepUpDown')
            # Label.after(ms=300, func=lambda:playSound('stepUpDown'))
        print(' audio step up/down...')


    else:
        print(' audio not found')

"""



