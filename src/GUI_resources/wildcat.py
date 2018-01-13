# Paria Khamsehzadeh
# HW 12
# SL: Heather Covello
# This class stores information about my wild cats
# This class will determine the behaviour and habbits of the wild cat

from Critter import *
from random import *

class WildCat(Critter):
    
    def __init__(self):
        self.hungry = True # setting the hungry variable equal to true so it will unitialy be hungry
        
    # the wild cat will eat as long as it is hungry
    #but their appetite will not be satisfied
    #untill they fight and eat a hippo so they will stay hungry
    #untill they have a hippo for lunch
    def eat(self):
        if self.hungry == True:
            return True
        return False

    def fight(self, opponent):
        for i in range(0, 10):
            if opponent == "%": # my wild cat will FORFEIT when it runs into an ant
                return ATTACK_FORFEIT
            # and it will pounce birds
            elif opponent == "V" or opponent == "<" or opponent == ">" or opponent == "^":
                return ATTACK_POUNCE
            # my while cats will scratch when they run into a hippo and then it will eat them and become full
            elif opponent == str(i):
                self.hungry = False
                return ATTACK_SCRATCH

    def get_color(self):
        if self.hungry == True: # they will be black wild cats as long as they are hungry 
            return "black"
        return "pink" # and thet will become pink when they eat a hippo

    def get_move(self):
        if self.hungry == True: # when they are hungry 
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
        else: # when they are full they will not move
            return DIRECTION_CENTER
        
    # they wild cats will stay thin when they are hungry and they will become round after they have a hippo
    def __str__(self):
        if self.hungry == True:
            return "I"
        return "O"
