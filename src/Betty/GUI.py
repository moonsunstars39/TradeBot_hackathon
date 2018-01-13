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


        # ---------------RasioButtons---------------------
        v = tk.IntVar()
        v.set(1)

        myList = [
        ("BTC-USD"),
        ("BCH-USD"),
        ("LTC-USD"),
        ("ETH-USD"),
        ]

        for val, language in enumerate(myList):
                  tk.Radiobutton(self._root, text=language, padx = 20, variable=v, value=val, command=self._bot.currency).pack(anchor=tk.W)
        # ---------------RasioButtons---------------------



        # ---------------CheckBoxes---------------------
        # the check values should be 1 if on and 0 if off.
        CheckVar1 = IntVar()
        CheckVar2 = IntVar()
        CheckVar3 = IntVar()
        CheckVar4 = IntVar()
        CheckVar5 = IntVar()

        myList2 = [
        (" SMA 120"), # CheckVar4
        (" SMA 30"),  # CheckVar3
        (" SMA 10"),  # CheckVar2
        ("  SMA 5"),  # CheckVar1
        ]
        i=0;
        for string in myList2:
            i+=1
            tk.Checkbutton(text = string, variable = ("CheckVar" + str(i)), onvalue = 1, offvalue = 0, height=1, width = 6).pack(side=BOTTOM)
        # ---------------CheckBoxes---------------------






def main():
    GUI = BotGUI()

main()
