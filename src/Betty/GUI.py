from tkinter import *
from bot import *

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

def main():
    GUI = BotGUI()
    
main()
