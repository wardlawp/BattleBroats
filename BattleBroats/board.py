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
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __eq__(self, other):
        
        if len(self.__data) != len(other.__data):
            return False
        
        for x in range(len(self.__data)):
            
            if len(self.__data[x]) != len(other.__data[x]):
                return False
            
            for y in range(len(self.__data[x])):
                if self.__data[x][y] !=  other.__data[x][y]:
                    return False
                
        return True
    
    def getEnemyView(self):
        enemyViewData = []
        for row in self .__data:
            enemyViewRow = []
            for el in row:
                if el._type in (Tile.SHOT, Tile.DEAD_BROAT):
                    enemyViewRow.append(el)
                else:
                    enemyViewRow.append(Tile())
            
            enemyViewData.append(enemyViewRow)
        
        return Board(None, None, enemyViewData) 
                    
    
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