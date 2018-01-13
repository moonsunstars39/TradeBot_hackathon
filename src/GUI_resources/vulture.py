# Paria Khamsehzadeh
# HW 12
# SL: Heather Covello
# This class stores information about my vulture
# This class will determine the behaviour and habbits of the vulture

from bird import * # for this one instead of using critter i'm using my bird class
# because they look almost identical

class Vulture(Bird):
    
    def __init__(self):
        self.move = 0
        self.fight_count = 0
        self.food_count = 0

    # the vutures eat differently sepending on fight method
    def eat(self):
        # so when they are first born they are hungry and get full when they eat once
        if self.food_count == 0:
            self.food_count +=1
            return True
        # they are full until they get into a fight
        # and get hungry again
        elif self.fight_count >= 1:
            return True
        return False

    # they fight differenty with ants than other animals
    # for my fight method i could have used the super method to eliminate redundency
    # but i chose not to because theres a slight difference betweenn my vunture's and my bird's
    # for my vutures to be able to eat again they would have to fight
    # and here i encrement fight by one to see if they can eat yet
    def fight(self, opponent):
        if opponent == "%": # they roar at ants
            self.fight_count += 1
            return ATTACK_ROAR
        # and pounce at others
        elif opponent != "<" or opponent != ">" or opponent != "^" or opponent != "V":
            self.fight_count += 1
            return ATTACK_POUNCE

    # the color of the vultures will be black at all times
    def get_color(self):
        return "black"
        

    # my last two methods are identical to bird's
    # so i am using the super method to eliminate redundency
    def get_move(self):
        moves =  super(Vulture, self).get_move()
        return moves

    def __str__(self):
        
        string =  super(Vulture, self).__str__()
        return string
