# Paria Khamsehzadeh
# HW 12
# SL: Heather Covello
# This class stores information about my ants
# This class will determine the behaviour and habbits of the ants

from Critter import *

class Ant(Critter):
    # constructs weather walk_south is true or false
    def __init__(self, walk_south):
        self.walk_south = walk_south
        self.move = 0 # setting move vaiable to 0
        
    # always returns true for eat method so my ants will always eat when they run into food
    def eat(self):
        return True
    
    # if the opponent they run into is not an ant they will always scratch
    def fight(self, opponent):
        if opponent != "%":
            return ATTACK_SCRATCH

    # return red because the ants are always red 
    def get_color(self):
        return "red"

    # this method determinds which direction the ants will be moving
    def get_move(self):
        self.move += 1 # encriments move by one
        if self.walk_south != True: # as spec says if walk_south is true, the ants will move east and south in a zigzag movement
            if self.move % 2 == 1: # if not divisible by 2 moves east
                return DIRECTION_EAST
            elif self.move % 2 == 0: # and when divisible by 2 moves south
                return DIRECTION_SOUTH
        # they go the other durection when walk_south == False
        else:
            if self.move % 2 == 1:
                return DIRECTION_NORTH
            elif self.move % 2 == 0:
                return DIRECTION_EAST
                
    # the ants are displayed as % on the display grid
    def __str__(self):
        return "%"
    
