from tkinter import *
from NavBar import *
from Settings import *
from LampView import *
from Calculate import *


class MyTkWindow:
    def __init__(self):
        self.root = Tk()  # Makes the window
        self.root.wm_title("POL")  # Makes the title that will appear in the top left
        self.root.config(background="#FFFFFF")
        self.settings_obj = Settings()

        self.leftFrame = Frame(self.root, width=200, height=600)
        self.leftFrame.grid(row=0, column=0, padx=(10,5), pady=2)
        #self.leftFrame.grid_propagate(False)


        self.rightFrame = Frame(self.root, width=300, height=300)
       # self.rightFrame.grid_propagate(False)
        self.rightFrame.grid(row=0, column=1, padx=(5,10), pady=2)

        self.bottomFrame = Frame(self.root,width=500,height=200)
       # self.bottomFrame.grid_propagate(False)
        self.bottomFrame.grid(row=1,column=0,columnspan=2,padx=10,pady=2)

        self.navbar = NavBar(self.root, self.settings_obj)
        self.calculate = Calculate(self.rightFrame,self.root)
        self.lampview = LampView(self.leftFrame,self.bottomFrame,self.settings_obj,self.calculate)

    def start(self):
        self.root.mainloop()  # start monitoring and updating the GUI


myWindow = MyTkWindow()
myWindow.start()
