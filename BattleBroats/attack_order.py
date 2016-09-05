'''
Created on Aug 16, 2016

@author: Philip Wardlaw
'''


from Network import Transmittable

class AttackOrder(Transmittable):


    def __init__(self, x, y):
        assert isinstance(x, int) and isinstance(y, int)
        self.x = x
        self.y = y
    
    
    def __ne__(self, other):
        return not self.__eq__(other)
    def __eq__(self, other):
      
        return self.x == other.x and self.y == other.y
    
    def serialize(self):
        return [self.x, self.y]
    
    @staticmethod
    def deserialize(data):
        return AttackOrder(data[0], data[1])