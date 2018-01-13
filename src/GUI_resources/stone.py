# This class represents a Rock type of Critter
# It stays still, doesn't eat and roars for an attack
# it is represented by a gray S

from Critter import *

class Stone (Critter): 
    def fight(self, opponent):
        return ATTACK_ROAR 
    
    def get_color(self):
        return "gray"
    
    def __str__(self): 
        return "S" 
