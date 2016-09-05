'''
Created on Aug 16, 2016

@author: Philip Wardlaw
'''
from tile import Tile
from Network import Transmittable
from attack_order import AttackOrder
from random import randint, shuffle

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
    
    def nCols(self):
        return len(self.__data[0])
    
    def nRows(self):
        return len(self.__data)

    def element(self, rowIdx, colIdx):
        return  self.__data[rowIdx][colIdx]
    
    
    def addBroats(self, broats):
        for broat in broats:
            notPlaced = True
            while notPlaced: #Potential for inf loop if we actually cant place 
                x, y = randint(0, self.nRows()-1), randint(0, self.nCols()-1)
                notPlaced = not self.__tryPlace(x,y,broat)
            
    def __tryPlace(self, x,y, broat):
        vectors = ((1,0), (-1,0), (0,1), (0,-1))
        order = range(4)
        shuffle(order)

        for o in order:
            broatOccupancy = []
            for i in range(broat):
                cell = [x + vectors[o][0]*i, y +  vectors[o][1]*i]
                broatOccupancy.append(cell)
                
            canPlace = True
          
            for cell in broatOccupancy:
                if cell[0] >= (self.nRows() -1) or cell[1] >= (self.nCols() -1):
                    canPlace = False
                    break
                
                if  self.__data[cell[0]][cell[1]] != Tile.WATER:
                    canPlace = False
                    break
                
            if canPlace:
                for cell in broatOccupancy:
                    self.__data[cell[0]][cell[1]] = Tile(Tile.BROAT)
                return True
        
        return False
            
    def shoot(self, attackOrder):
        assert isinstance(attackOrder, AttackOrder)
        
        if self.__data[attackOrder.x][attackOrder.y] == Tile.WATER:
            self.__data[attackOrder.x][attackOrder.y] = Tile(Tile.SHOT)
        else:
            self.__data[attackOrder.x][attackOrder.y] = Tile(Tile.DEAD_BROAT)
        
    def getEnemyView(self):
        enemyViewData = []
        for row in self .__data:
            enemyViewRow = []
            for el in row:
                if el.type in (Tile.SHOT, Tile.DEAD_BROAT):
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
            
            
        return Board(None, None, deserialzedData)
        
    
    def serialize(self):
        serialData = []
        
        for row in self.__data:
            serialRow = []
            for el in row:
                serialRow.append(el.serialize())
            serialData.append(serialRow)
                
        return serialData
    
    
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
    
    def __str__(self, *args, **kwargs):
        return 'Board:' + str(self.__data)