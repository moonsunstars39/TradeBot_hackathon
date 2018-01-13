# Preliminary version of the Critters class
# We will give you a different version for the homework. 

#
# Author: Daniel Dicken
# Converting CSc 110 "Critters" program from java to python.
#

WIDTH = 50
HEIGHT = 50
NUM_CRITTERS = 50

# Global variable, once a critter class is implemented, put its name in here
CLASS_NAMES = ["Stone", "Ant", "Bird", "Hippo", "Vulture", "WildCat"]

SELECTED_CLASSES = []

STATS = []

# Imports
import atexit
import sys
import time
import subprocess
import os
import imp
import inspect 
import random
from time import sleep
from random import *
from Critter import *
from tkinter import *
from threading import Thread

# ---------- start main ----------

def main():
    control = Control()
    gui = GUI(control)
    #model = Model(3, 3)

# ---------- end main ----------

# ---------- start Model ----------

# Model represents the board and critter tournament
class Model:

    def __init__(self, xSize, ySize, numCritters, control):

        self.xSize = xSize
        self.ySize = ySize

        self.control = control
        self.classes = []
        self.numCritters = numCritters
        self.critters = []

        self.critterMap = [[0 for x in range(ySize)] for y in range(xSize)]
        self.foodMap = [[0 for x in range(ySize)] for y in range(xSize)]

        # Represent our critter map with a 2d array of the given size
        for x in range(xSize):
            for y in range(ySize):
                self.critterMap[x][y] = Critter()
                self.critterMap[x][y].setX(-1)
                self.critterMap[x][y].setY(-1)

        # Represent our food map with a 2d array of the given size
        for x in range(xSize):
            for y in range(ySize):
                self.foodMap[x][y] = 0

        # Generate initial food on map
        i = 0
        while i < randint(0, int((xSize * ySize)/4)):

            self.randX = randint(0, xSize-1)
            self.randY = randint(0, ySize-1)

            if (self.foodMap[self.randX][self.randY] == 0):
                self.foodMap[self.randX][self.randY] = 1
                i += 1                

        self.i = 0
        for value in CLASS_NAMES:
           #value = value.lower()
           #print(value)
           if (SELECTED_CLASSES[self.i].get()):
                print("Importing " + CLASS_NAMES[self.i]) # fix for file lowercase
                self.classes.append(getattr(__import__(CLASS_NAMES[self.i].lower()), CLASS_NAMES[self.i]))
           self.i += 1

        for className in self.classes:
            for i in range(self.numCritters):
                self.critter = ""
                #print(className)
                if "ant" in str(className).lower():
                    self.critter = className(randint(0, 1) == 0)
                elif "hippo" in str(className).lower():
                    self.critter = className(randint(1, 9))
                
                else:
                    self.critter = className()
                self.critters.append(self.critter)
               
                while True:
                    self.randX = randint(0, xSize-1)
                    self.randY = randint(0, ySize-1)
                    if (self.critterMap[self.randX][self.randY].getX() == -1 
                            and self.critterMap[self.randX][self.randY].getY() == -1): 
                        self.critter.setX(self.randX)
                        self.critter.setY(self.randY)
                        self.critterMap[self.randX][self.randY] = self.critter
                        break
                  


    def turn(self):

         # Shuffle list of critters for randomized "fair" movement
        shuffle(self.critters)
        self.moveCritters()

    def moveCritters(self):

        for critter in self.critters:
            if critter.is_mating():
                self.tempC = critter.get_mate()
                #                print("is awake " + str(critter.isAwake()))
                if critter.is_awake() and self.tempC != None and not critter.get_mating():
                    while self.tempC.get_mating():
                        self.tempC.is_mating()
                    (self.tempX,self.tempY) = self.findOpen()
                    if "ant" in str(type(critter)).lower():
                        self.critterMap[self.tempX][self.tempY] = type(critter)(randint(0, 1) == 0)
                    elif "hippo" in str(type(critter)).lower():
                        self.critterMap[self.tempX][self.tempY] = type(critter)(randint(1, 9))
                    else:
                        self.critterMap[self.tempX][self.tempY] = type(critter)()
                    self.critters.append(self.critterMap[self.tempX][self.tempY])
                    self.critterMap[self.tempX][self.tempY].setX(self.tempX)
                    self.critterMap[self.tempX][self.tempY].setY(self.tempY)

                continue

            if not critter.is_awake():
                continue

            self.move = critter.get_move()
            
            self.x = critter.getX()
            self.y = critter.getY()
            self.newX = self.x
            self.newY = self.y

            if self.foodMap[self.x][self.y] == 1:
                if critter.eat():
                    critter.increment_food()
                    self.foodMap[self.x][self.y] = 0
                if critter.get_food() >= 5:
                    critter.sleep()
                    critter.set_food()
                    critter.set_awake(False)
                    continue

            if self.move == DIRECTION_NORTH:
                self.newY += 1
                if self.newY > self.ySize - 1:
                    self.newY = 0

            elif self.move == DIRECTION_SOUTH:
                self.newY -= 1
                if self.newY < 0:
                    self.newY = self.ySize - 1

            elif self.move == DIRECTION_EAST:
                self.newX += 1
                if self.newX > self.xSize - 1:
                    self.newX = 0

            elif self.move == DIRECTION_WEST:
                self.newX -= 1
                if self.newX < 0:
                    self.newX = self.xSize - 1
                       

            if ((self.critterMap[self.newX][self.newY].getX() == -1 
                    and self.critterMap[self.newX][self.newY].getY() == -1) and (critter.is_awake())):
                critter.setX(self.newX)
                critter.setY(self.newY)
                self.critterMap[self.newX][self.newY] = critter
                self.critterMap[self.x][self.y] = Critter()
                self.critterMap[self.x][self.y].setX(-1)
                self.critterMap[self.x][self.y].setY(-1)
            elif not (str(self.critterMap[self.newX][self.newY]) == str(self.critterMap[self.x][self.y])):

                self.a1 = self.critterMap[self.newX][self.newY].fight(self.critterMap[self.x][self.y]) 
                self.a2 = self.critterMap[self.x][self.y].fight(self.critterMap[self.newX][self.newY])
                self.winner = self.fight(self.a1,self.a2)

                if (self.a1 == ATTACK_FORFEIT or self.winner == 1):
                    critter.win()
                    if (self.critterMap[self.newX][self.newY] in self.critters): 
                        self.critters.remove(self.critterMap[self.newX][self.newY])
                    self.critterMap[self.newX][self.newY].set_alive(False)
                    self.critterMap[self.newX][self.newY] = critter
                    critter.setX(self.newX)
                    critter.setY(self.newY)
                    self.critterMap[self.x][self.y] = Critter()
                    self.critterMap[self.x][self.y].setX(-1)
                    self.critterMap[self.x][self.y].setY(-1)                  
                elif (self.a2 == ATTACK_FORFEIT or self.winner == 2):
                    critter.lose()
                    self.critterMap[self.x][self.y].set_alive(False)
                    self.critterMap[self.x][self.y] = Critter()
                    self.critterMap[self.x][self.y].setX(-1)
                    self.critterMap[self.x][self.y].setY(-1)                  
                    self.critters.remove(critter)

            elif (str(self.critterMap[self.newX][self.newY]) == str(self.critterMap[self.x][self.y]) and not self.critterMap[self.newX][self.newY].has_mated() and not self.critterMap[self.x][self.y].has_mated()):
                    critter.mate()
                    self.critterMap[self.newX][self.newY].set_mated(True)
                    self.critterMap[self.x][self.y].set_mated(True)
                    self.critterMap[self.newX][self.newY].is_mating()
                    self.critterMap[self.x][self.y].is_mating()
                    self.critterMap[self.newX][self.newY].set_mate(self.critterMap[self.x][self.y])
                    self.critterMap[self.x][self.y].set_mate(self.critterMap[self.newX][self.newY])

        i = 0
        while i < randint(0, 5):

            self.randX = randint(0, self.xSize-1)
            self.randY = randint(0, self.ySize-1)

            if (self.foodMap[self.randX][self.randY] == 0):
                self.foodMap[self.randX][self.randY] = 1
            i += 1                

    def fight(self, a1,a2):
        if a1 == a2:
            return 0

        if ((a1 == ATTACK_ROAR and a2 == ATTACK_SCRATCH) or (a1 == ATTACK_SCRATCH and a2 == ATTACK_POUNCE) or (a1 == ATTACK_POUNCE and a2 == ATTACK_ROAR)):
            return 1
        elif ((a2 == ATTACK_ROAR and a1 == ATTACK_SCRATCH) or (a2 == ATTACK_SCRATCH and a1 == ATTACK_POUNCE) or (a2 == ATTACK_POUNCE and a1 == ATTACK_ROAR)):
            return 2
   
    def findOpen(self):
        x = 0
        y = 0
        while (self.critterMap[x][y].getX() != -1 and self.critterMap[x][y].getY() != -1):
            x = randint(0,self.xSize) -1
            y = randint(0,self.ySize) -1
        return (x,y)

    def getCritterMap(self):
        return self.critterMap

    def getFoodMap(self):
        return self.foodMap

# ---------- end Model ----------

# ---------- start Control ----------
class Control:

    def __init__(self):
        self.width = 0
        self.height = 0
        self.isRunning = False
        self.oneTick = False

    def setGUI(self, gui):
        self.gui = gui
        self.width = int(gui.width)
        self.height = int(gui.height)
        self.critters = int(gui.critters)
        self.speed = 1
        self.model = Model(self.width, self.height, self.critters, self)

    def run(self):

        while True:

            if self.isRunning:
                self.model.turn()
                self.gui.updateMoves()
                self.gui.drawMap(self.getCritterMap(), self.getFoodMap())

                if self.oneTick == True:
                    self.isRunning = False
                    self.oneTick = False
                    continue

                sleep(self.getSpeed()/100)

    def getSpeed(self):
        return self.gui.getSpeed()

    def start(self):
        self.isRunning = True

    def tick(self):       
        if not self.isRunning:
            self.oneTick = True
            self.isRunning = True

    def stop(self):
        self.isRunning = False

    def reset(self):
        self.isRunnig = False

    def getCritterMap(self):
        return self.model.getCritterMap()

    def getFoodMap(self):
        return self.model.getFoodMap()

# ---------- end Control ----------

# ---------- start GUI ----------
# Tkinter GUI for program
class GUI(Tk):

    # Define variables
    width = 0
    height = 0
    critters = 0

    def __init__(self, control):
        Tk.__init__(self)

        self.thread = None

        self.frame = Frame(self)
        self.frame.pack()

        self.control = control

        self.title("Critters Settings")

        self.widthLabel = Label(self.frame, text="width")
        self.widthEntry = Text(self.frame, height=1, width=10)
        self.widthEntry.insert(END, str(WIDTH))
        self.widthLabel.pack()
        self.widthEntry.pack()

        self.heightLabel = Label(self.frame, text="height")
        self.heightEntry = Text(self.frame, height=1, width=10)
        self.heightEntry.insert(END, str(HEIGHT))
        self.heightLabel.pack()     
        self.heightEntry.pack()

        self.critterLabel = Label(self.frame, text="Number of Critters")
        self.critterEntry = Text(self.frame, height=1, width=10)
        self.critterEntry.insert(END, str(NUM_CRITTERS))
        self.critterLabel.pack()        
        self.critterEntry.pack()

        # Put tick boxes for each critter class in the directory to select if we want them in the tournament
        i = 0
        for fileName in CLASS_NAMES:
            SELECTED_CLASSES.append(BooleanVar())
            c = Checkbutton(self.frame, text=fileName, variable=SELECTED_CLASSES[i], onvalue=1, offvalue=0)
            i += 1
            c.pack()

        self.enterButton = Button(self.frame, text="Enter", fg="black", command=self.switchView)
        self.enterButton.pack()

        self.mainloop()

    # Switch view from starting prompt to critters tournament
    def switchView(self):

        self.width = self.retrieve_input(self.widthEntry)
        self.height = self.retrieve_input(self.heightEntry)
        self.critters = self.retrieve_input(self.critterEntry)

        if isValid(self.width) and isValid(self.height) and isValid(self.critters):
            self.width = int(self.width)
            self.height = int(self.height)
            self.control.setGUI(self)
            self.setMapGUI()
        else:
            self.errorWindow("Given inputs were not numbers")

    # Draw the map and other aspects of GUI
    def setMapGUI(self):

        self.frame.destroy()

        self.guiMap = Canvas(self, width=(self.width*12)+1,height=(self.height*12)+1, bg="lightgreen")
        self.guiMap.grid(row=0, column=0)

        self.multiple = 0
        for j in range(self.height + 2):
            self.guiMap.create_line(0, self.multiple + 1, self.width*12, self.multiple + 1)
            self.multiple = self.multiple + 12

        self.multiple = 0
        for i in range(self.width + 2):
            self.guiMap.create_line(self.multiple + 1, 0, self.multiple + 1, self.height*12)
            self.multiple = self.multiple + 12

        self.drawMap(self.control.getCritterMap(), self.control.getFoodMap())

        self.points = []

        self.frame = Frame(self)

        self.scale = Scale(self.frame, from_=2, to=61, orient=HORIZONTAL)
        self.scale.grid(row=1, column=0)

        # GUI elements that keep track of number of moces
        self.moveFrame = Frame(self.frame)
        self.moveLabel = Label(self.moveFrame, text="Moves")
        self.moveLabel.grid(row=0, column=0)
        self.moveCountLabel = Label(self.moveFrame, text="0")
        self.moveCountLabel.grid(row=1, column=0)
        self.moveFrame.grid(row=1, column=1)

        # Thread to run the control loop on
        self.thread = Thread(target=self.control.run)
        self.thread.daemon = True
        self.thread.start()

        # Buttons to control tournament
        self.goButton = Button(self.frame, text=" Go ", command=self.control.start)
        self.stopButton = Button(self.frame, text="Stop", command=self.control.stop)
        self.tickButton = Button(self.frame, text="Tick", command=self.control.tick)
        self.resetButton = Button(self.frame, text="Reset", command=self.control.reset)
        self.goButton.grid(row=1, column=2)
        self.stopButton.grid(row=1, column=3)
        self.tickButton.grid(row=1, column=4)
        self.resetButton.grid(row=1, column=5)

        self.frame.grid(row=1, column = 0)

    def drawMap(self, critterMap, foodMap):

        self.guiMap.delete("critter")
        self.guiMap.delete("food")
        for critterList in critterMap:
            for critter in critterList:
                if (critter.getX() != -1 and critter.getY() != -1): 
                    self.guiMap.create_text(critter.getX() * 12 + 5, critter.getY() * 12, anchor=NW, text=str(critter), fill=critter.get_color(), tags=("critter"))
                    if (critter.get_mating()):
                        self.guiMap.create_text(critter.getX() * 12 + 2, critter.getY() * 12, anchor=NW, text="M",font=("Helvetica", 4), tags=("critter"))


        x = 0
        y = 0
        for j in foodMap:
            for item in j:
                if (item == 1): 
                    self.guiMap.create_text(x * 12 + 5, y * 12 - 3, anchor=NW, text=".", tags=("food"))
                y += 1
            x += 1
            y = 0

    def updateMoves(self):
            self.moveCountLabel['text'] = int(self.moveCountLabel['text']) + 1

    def getSpeed(self):
        return self.scale.get()

    # Give error message popup windows
    def errorWindow(self, msg):

        self.top = Toplevel()
        self.top.title("Error")

        self.msgWindow = Message(self.top, text=msg)
        self.msgWindow.pack()

        self.button = Button(self.top, text="Dismiss", command=self.top.destroy)
        self.button.pack()

    def retrieve_input(self, textBox):
        return textBox.get("1.0",'end-1c')

# ---------- end GUI ----------

# ---------- start Helper Functions ----------

# check if input is valid
def isValid(s):

    try: 

        num = int(s)

        if (num > 0):
            return  True
        else:
            return False

    except ValueError:
        return False

# ---------- end Helper Functions ----------

main()

