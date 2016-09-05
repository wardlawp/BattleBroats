'''
Created on Aug 16, 2016

@author: Philip Wardlaw
'''


from Network import Transmittable

class Tile(Transmittable):

    WATER = 0
    BROAT = 1
    DEAD_BROAT = 2
    SHOT = 3
    
    VALID_TYPES = [WATER, BROAT]


    def __init__(self, _type = WATER ):
        assert _type in Tile.VALID_TYPES
        self.type = _type
    
    def __str__(self):
        return self.type
    
    def __ne__(self, other):
        return not self.__eq__(other)
    def __eq__(self, other):
        if isinstance(other, int):
            return self.type == other
        
        return self.type == other.type
    
    def serialize(self):
        return self.type
    
    @staticmethod
    def deserialize(string):
        return Tile(string)