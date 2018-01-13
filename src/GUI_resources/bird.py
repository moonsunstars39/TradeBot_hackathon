# Paria Khamsehzadeh
# HW 12
# SL: Heather Covello
# This class stores information about my birds
# This class will determine the behaviour and habbits of the birds

from Critter import *

class Bird(Critter):
    
    def __init__(self):
        self.move = 0 # initializing move variable
        
    # always returns False for eat method so my ants will never eat when they run into food
    def eat(self):
        return False
    
    # the birds will only roar when they run into an ant, otherwise they will pounce
    def fight(self, opponent):
        if opponent == "%": # so if opponent is an ant , they roar
            return ATTACK_ROAR
        # else: as long as it's not another bird, they will pounce
        elif opponent != "<" or opponent != ">" or opponent != "^" or opponent != "V":
            return ATTACK_POUNCE
        
    # the color of the birds will be blue at all times
    def get_color(self):
        return "blue"

    # the birds are suppossed to have a clockwise circle movement , moving 3 blocks in each direction
    def get_move(self):
        self.move += 1 # so i encrement 3 by 1
        
        if self.move <= 3: # and they will go sounth when the move variable is less than or equal to 3
            # and so on for each direction
            return DIRECTION_SOUTH
        elif self.move <= 6:
            return DIRECTION_EAST
        elif self.move <= 9:
            return DIRECTION_NORTH
        elif self.move <= 12:
            return DIRECTION_WEST
        elif self.move == 13:
            self.move = 1
            return DIRECTION_SOUTH

    # the birds have a different symbol depending on which direction they are moving in
    def __str__(self):
        # mt str method looks similar to my get move method
        if self.move <= 3: #  they will go sounth with a ^ symbol when the move variable is less than or equal to 3
            return "^"
        # and so on for each direction
        elif self.move <= 6:
            return ">"
        elif self.move <= 9:
            return "V"
        elif self.move <= 12:
            return "<"
        
    
