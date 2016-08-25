'''
Created on Aug 16, 2016

@author: Philip Wardlaw
'''
from tile import Tile
from Protocol import Transmittable
import json

class Board(Transmittable):
    '''
    classdocs
    '''


    def __init__(self, nCols = None, nRows= None, data = None):
        '''
        Constructor
        '''
        if data is None:
            self.__data = [[Tile() for y in xrange(nCols)] for x in xrange(nRows)]
        else:
            self.__data = data
            
    @staticmethod
    def deserialize(data):
        deserialzedData = []
        for row in data:
            deserialzedRow = []
            for el in row:
                deserialzedRow.append(Tile.deserialize(el))
            deserialzedData.append(deserialzedRow)
            
            
        return Board(None, None, data)
        
    
    def serialize(self):
        serialData = []
        
        for row in self.__data:
            serialRow = []
            for el in row:
                serialRow.append(el.serialize())
            serialData.append(serialRow)
                
        return serialData
    
    def __str__(self, *args, **kwargs):
        return 'Board:' + str(self.__data)