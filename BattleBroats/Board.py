'''
Created on Aug 16, 2016

@author: Philip Wardlaw
'''
from Tile import Tile
from Protocol import Transmittable

class Board(Transmittable):
    '''
    classdocs
    '''


    def __init__(self, nRows, nCols):
        '''
        Constructor
        '''
        self.__data = [[Tile() for y in xrange(nCols)] for x in xrange(nRows)]
        
    
    def deserialize(self, string):
        print string
        
    
    def serialize(self):
        serialData = []
        
        for row in self.__data:
            serialRow = []
            for el in row:
                serialRow.append(el.serialize())
            serialData.append(serialRow)
                
        return serialData