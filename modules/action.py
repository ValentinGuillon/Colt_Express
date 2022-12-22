from tkinter import Frame, Button
import modules.images as images


#create empty class just to be able to names variables type
class Game:
    pass




class Action(Frame):
    def __init__(self, game:Game, actionsFrame:Frame, value:str, column:int):
        super().__init__(actionsFrame, bg='orange')
        self.game:Game = game
        self.column:int = column
        self.value:str = value

        self.action = Button(self, text=value, command=self.remove)
        self.left = Button(self, text="<-", command=self.moveLeft)
        self.right = Button(self, text="->", command=self.moveRight)

        self.configButton([self.action, self.left, self.right])


        if not value == 'osef':
            self.drawImg()


        self.action.grid(row=0, column=0, columnspan=2, sticky='ew')
        self.left.grid(row=1, column=0)
        self.right.grid(row=1, column=1)


    
    def configButton(self, buttons:list[Button]):
        for btn in buttons:
            btn.config(bg=self.game.WIDGET_COLORS['train'], border=0, highlightthickness=0, activebackground=self.game.WIDGET_COLORS['road'])


    def chooseTheGoodImg(self):
        if self.value == 'right':
            return images.imgRight
        elif self.value == 'left':
            return images.imgLeft
        elif self.value == 'up':
            return images.imgUp
        elif self.value == 'down':
            return images.imgDown
        elif self.value == 'shoot':
            return images.imgShoot
        elif self.value == 'rob':
            return images.imgRob
        else:
            return images.imgWagon


    def setImgAction(self):
        self.action.destroy()
        self.imgAction = images.createLoadedImg(self.widthAction, int((self.heightAction//3)*2), self.chooseTheGoodImg())
        self.action = Button(self, text=self.value, command=self.remove, image=self.imgAction)
        self.configButton([self.action])
        self.action.grid(row=0, column=0, columnspan=2, sticky='ew')


    def remove(self):
        for action in self.game.tempActions:
            if action == self:
                self.game.removeAction(self)
                return


    #swap value between this Action and the right one
    def moveRight(self):
        if (self.column >= self.game.MAX_ACTIONS-1) or (self.column >= len(self.game.tempActions)-1):
            #can't move right
            return


        for i, action in enumerate(self.game.tempActions):
            if action == self:
                actionTo = self.game.tempActions[i+1]

                #swap values
                self.value, actionTo.value = actionTo.value, self.value

                #update Action(s)
                self.update()
                actionTo.update()



    #swap value between this Action and the left one
    def moveLeft(self):
        if self.column <= 0:
            #can't move left
            return


        for i, action in enumerate(self.game.tempActions):
            if action == self:
                actionTo = self.game.tempActions[i-1]

                #swap values
                self.value, actionTo.value = actionTo.value, self.value

                #update Action(s)
                self.update()
                actionTo.update()



    def update(self):
        self.action.config(text=self.value)
        self.setImgAction()


    def drawImg(self):
        self.widthAction = (self.game.menuSpace.winfo_width()) // self.game.MAX_ACTIONS
        self.heightAction = int(self.game.menuSpace.winfo_height()*0.15)

        if self.widthAction <= 0:
            self.widthAction = 10
        if self.heightAction <= 0:
            self.heightAction = 10

        if self.widthAction > self.heightAction:
            self.widthAction = self.heightAction

        self.setImgAction()
        self.imgLeft = images.createLoadedImg(self.widthAction//2, int(self.heightAction//3), images.imgLeft)
        self.imgRight = images.createLoadedImg(self.widthAction//2, int(self.heightAction//3), images.imgRight)

        self.action.config(image=self.imgAction)
        self.left.config(image=self.imgLeft)
        self.right.config(image=self.imgRight)

