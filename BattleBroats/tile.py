'''
Created on Aug 16, 2016

@author: Philip Wardlaw
'''


from Protocol import Transmittable

class Tile(Transmittable):

    WATER = 0
    BROAT = 1
    
    VALID_TYPES = [WATER, BROAT]


    def __init__(self, _type = WATER ):
        assert _type in Tile.VALID_TYPES
        self._type = _type
    
    def __str__(self):
        return self._type
    
    def serialize(self):
        return self._type
    
    @staticmethod
    def deserialize(string):
        return Tile(string)