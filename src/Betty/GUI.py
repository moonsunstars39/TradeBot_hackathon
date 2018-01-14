from tkinter import *
from bot import *
import tkinter as tk

class BotGUI():
    def __init__(self):
        self.setup_backend()
        self.setup_frontend()
        self._root.mainloop()

    def setup_backend(self):
        socket = BotSocket(product=["BTC-USD", "LTC-USD", "ETH-USD", "BCH-USD"], channels=["matches"])
        self._bot = Bot("Betty", "LTC-USD", socket)

    def setup_frontend(self):
        self._root = Tk()

        self._topframe = Frame(self._root)
        self._topframe.pack(side=TOP)

        self._bottomframe = Frame(self._root)
        self._bottomframe.pack(side=BOTTOM)

        self._startButton = Button(self._topframe, text="Start Bot", bg="green", fg="black", command=self._bot.start)
        self._stopButton  = Button(self._topframe, text="Stop Bot", bg="red", fg="white", command=self._bot.stop)

        self._startButton.pack(side=LEFT)
        self._stopButton.pack(side=LEFT)


        # ---------------RadioButtons---------------------
        v = tk.StringVar()
        v.set("BTC-USD")

        myList = [
        ("BTC-USD"),
        ("BCH-USD"),
        ("LTC-USD"),
        ("ETH-USD"),
        ]
        
        tk.Radiobutton(self._root, text=myList[0], padx = 20, variable=v, value=myList[0], command= lambda: self._bot.set_currency(myList[0])).pack(anchor=tk.W)
        tk.Radiobutton(self._root, text=myList[1], padx = 20, variable=v, value=myList[1], command= lambda: self._bot.set_currency(myList[1])).pack(anchor=tk.W)
        tk.Radiobutton(self._root, text=myList[2], padx = 20, variable=v, value=myList[2], command= lambda: self._bot.set_currency(myList[2])).pack(anchor=tk.W)
        tk.Radiobutton(self._root, text=myList[3], padx = 20, variable=v, value=myList[3], command= lambda: self._bot.set_currency(myList[3])).pack(anchor=tk.W)
        # ---------------RadioButtons---------------------



        # ---------------CheckBoxes---------------------
        # the check values should be 1 if on and 0 if off.
        CheckVars = [IntVar(), IntVar(), IntVar(), IntVar(), IntVar()]
        '''
        CheckVar1 = IntVar()
        CheckVar2 = IntVar()
        CheckVar3 = IntVar()
        CheckVar4 = IntVar()
        CheckVar5 = IntVar()
        '''
        myList2 = [
        (" SMA 120"), # CheckVar[4]
        (" SMA 30"),  # CheckVar[3]
        (" SMA 10"),  # CheckVar[2]
        ("  SMA 5"),  # CheckVar[1]
        ("  SMA 1"),  # CheckVar[0]
        ]
        i=0;
        for string in myList2:
            tk.Checkbutton(text = string, variable = CheckVars[i], onvalue = 1, offvalue = 0, height=1, width = 6, command= lambda:self.update_graphics(CheckVars, myList2)).pack(side=BOTTOM)
            i+=1
        # ---------------CheckBoxes---------------------
        
    def update_graphics(self, CheckVars, Average_list):
        print("----------------")

        for i in range(len(CheckVars)):
            if CheckVars[i].get() == 1:
                print(Average_list[i])
        






def main():
    GUI = BotGUI()

main()
