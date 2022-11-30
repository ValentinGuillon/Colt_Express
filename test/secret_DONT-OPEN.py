from tkinter import *
from PIL import Image, ImageTk

# from goto import with_goto

global time
time = 0




class Root(Tk):
    imgs = []
    def __init__(self):
        super().__init__()
        self.geometry("900x650")

        self.config(bg="blue")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)

        self.btn = Button(self, text="Start")
        self.btn.config(command=self.parallax)
        self.btn.grid(column=1)

        self.exit = Button(self, text="Move Btn")
        self.exit.config(command=self.moveBtn)
        self.exit.grid()
        
        self.cnv = Canvas(self, width=800, height=600, bg="orange")
        self.cnv.grid(row=1, column=1)

        



        self.img_1 = Root.createImg("1_sky")
        self.img_2 = Root.createImg("2_mountains-over-horizon")
        self.img_3 = Root.createImg("3_sand")
        self.img_4 = Root.createImg("5_mountains_1")
        self.img_5 = Root.createImg("5_mountains_2")
        self.img_6 = Root.createImg("6_cactus_1")
        self.img_7 = Root.createImg("6_cactus_2")
        self.img_8 = Root.createImg("7_rails_1")
        self.img_9 = Root.createImg("7_rails_2")
        self.img_10 = Root.createImg("7_rails_3")
        self.img_11 = Root.createImg("8_rocks-ahead_1")
        self.img_12 = Root.createImg("8_rocks-ahead_2")
        self.img_13 = Root.createImg("8_rocks-ahead_3")

        self.loco = Image.open("../png/locomotive val.png")
        self.loco = self.loco.resize((200, 200))
        self.loco = ImageTk.PhotoImage(self.loco)

        img1 = self.cnv.create_image(0, 0, anchor="nw", image=self.img_1)
        img2 = self.cnv.create_image(0, 0, anchor="nw", image=self.img_2)
        img3 = self.cnv.create_image(0, 0, anchor="nw", image=self.img_3)
        img4 = self.cnv.create_image(0, 0, anchor="nw", image=self.img_4)
        img5 = self.cnv.create_image(0, 0, anchor="nw", image=self.img_5)
        img6 = self.cnv.create_image(0, 0, anchor="nw", image=self.img_6)
        img7 = self.cnv.create_image(0, 0, anchor="nw", image=self.img_7)
        img8 = self.cnv.create_image(0, 0, anchor="nw", image=self.img_8)
        # img9 = self.cnv.create_image(0, 0, anchor="nw", image=self.img_9)
        # img10 = self.cnv.create_image(0, 0, anchor="nw", image=self.img_10)
        img11 = self.cnv.create_image(0, 0, anchor="nw", image=self.img_11)
        img12 = self.cnv.create_image(0, 0, anchor="nw", image=self.img_12)
        img13 = self.cnv.create_image(0, 0, anchor="nw", image=self.img_13)
        imgloco = self.cnv.create_image(200, 0, anchor="nw", image=self.loco)

        self.imgs.append(img1)
        self.imgs.append(img2)
        self.imgs.append(img3)
        self.imgs.append(img4)
        self.imgs.append(img5)
        self.imgs.append(img6)
        self.imgs.append(img7)
        self.imgs.append(img8)
        # self.imgs.append(img9)
        # self.imgs.append(img10)
        self.imgs.append(img11)
        self.imgs.append(img12)
        self.imgs.append(img13)
        self.imgs.append(imgloco)


        # while(1):
        #     self.after(ms=1, func=self.parallax)
        #     # self.parallax()


        
    @classmethod
    def createImg(cls, file):
        file = "../png/wip/secret_DONT-OPEN/" + file + ".png"
        img = Image.open(file)
        img = img.resize((800, 600))
        return ImageTk.PhotoImage(img)

    
    def moveBtn(self):
        print("=========================")



    def parallax(self):
        global time
        for img in self.imgs:
            self.cnv.delete(img)

        if time == 90:
            time = 0


        #1
        img1 = self.cnv.create_image(0, 0, anchor="nw", image=self.img_1)
        self.imgs.append(img1)

        #2
        img2 = self.cnv.create_image(0, 0, anchor="nw", image=self.img_2)
        self.imgs.append(img2)

        #3
        img3 = self.cnv.create_image(0, 0, anchor="nw", image=self.img_3)
        self.imgs.append(img3)

        #4
        img4 = self.cnv.create_image(0, 0, anchor="nw", image=self.img_4)
        self.imgs.append(img4)

        #5
        img5 = self.cnv.create_image(0, 0, anchor="nw", image=self.img_5)
        self.imgs.append(img5)

        #6
        img6 = self.cnv.create_image(0, 0, anchor="nw", image=self.img_6)
        self.imgs.append(img6)

        #7
        img7 = self.cnv.create_image(0, 0, anchor="nw", image=self.img_7)
        self.imgs.append(img7)

        #rails
        if time < 30:
            img8 = self.cnv.create_image(0, 0, anchor="nw", image=self.img_8)
            self.imgs.append(img8)

        elif time < 60:
            img9 = self.cnv.create_image(0, 0, anchor="nw", image=self.img_9)
            self.imgs.append(img9)

        else:
            img10 = self.cnv.create_image(0, 0, anchor="nw", image=self.img_10)
            self.imgs.append(img10)

        #11
        img11 = self.cnv.create_image(0, 0, anchor="nw", image=self.img_11)
        self.imgs.append(img11)

        #12
        img12 = self.cnv.create_image(0, 0, anchor="nw", image=self.img_12)
        self.imgs.append(img12)

        #13
        img13 = self.cnv.create_image(0, 0, anchor="nw", image=self.img_13)
        self.imgs.append(img13)

        #loco
        imgloco = self.cnv.create_image(200, 200, anchor="nw", image=self.loco)
        self.imgs.append(imgloco)

        

            

        
        time += 1
        print(time)

        self.after(ms=1, func=self.parallax)

        






root = Root()
# root.after(1, root.parallax())
# while(1):
#     root.after(ms=1, func=root.parallax)

root.mainloop()

