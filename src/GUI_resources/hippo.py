# Paria Khamsehzadeh
# HW 12
# SL: Heather Covello
# This class stores information about my hippos
# This class will determine the behaviour and habbits of the hippo

from Critter import *
from random import *

class Hippo(Critter):
    
    # constructs weather hunger is true or false
    def __init__(self, hunger):
        self.hunger = hunger
        self.count = 0

    # hippos eat the number of times they are hungry
    def eat(self):
        if self.hunger > 0: # so as long as the value if hunger is not 0 they will eat
            self.hunger -= 1
            return True
        
        return False

    # the hippos fight differently depending on wether they are hungry or not
    def fight(self, opponent):
        # so if they are hungry they scratch
        if self.hunger > 0 and opponent != "0" or opponent != "1" or opponent != "2" or opponent != "3" or opponent != "4" or opponent != "5":
            return ATTACK_SCRATCH
        # and if they are not hungry, they pounce
        elif opponent != "0" or opponent != "1" or opponent != "2" or opponent != "3" or opponent != "4" or opponent != "5":  
            return ATTACK_POUNCE

    # their color also depends on on wether they are hungry or not
    def get_color(self):
        if self.hunger > 0: # so if they are hungry they are gray otherwise they are white
            return "gray"
        return "white"

    # the hipos do not move in a pattern like others
    # the move randomly, so im using the randint method
    def get_move(self):
        rand_num = randint(1, 4) # choosing a random number between 1-4
        # and moving a certain direction depending on the number, then repeat
        if rand_num == 1:
            rand_num = randint(1, 4)
            return DIRECTION_NORTH
        elif rand_num == 2:
            rand_num = randint(1, 4)
            return DIRECTION_EAST
        elif rand_num == 3:
            rand_num = randint(1, 4)
            return DIRECTION_SOUTH
        else:
            rand_num = randint(1, 4)
            return DIRECTION_WEST
        
                
    # the hippos will look differenetly depending on how hungry they are
    # this methis will return the string value of hunger
    # which represents how much more food they can eat
    def __str__(self):
        
        if self.hunger == 0:
            return "0"
        elif self.hunger == 1:
            return "1"
        elif self.hunger == 2:
            return "2"
        elif self.hunger == 3:
            return "3"
        elif self.hunger == 4:
            return "4"
        elif self.hunger == 5:
            return "5"
        elif self.hunger == 6:
            return "6"
        elif self.hunger == 7:
            return "7"
        elif self.hunger == 8:
            return "8"
        else:
            return "9"






