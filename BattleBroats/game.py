'''
Created on Aug 16, 2016

@author: Philip Wardlaw
'''

from GameState import ServerStartState, ClientStartState
from board import Board
from observer import Observer
from subject import Subject

class Game(Subject):
    
    MODE_SERVER = 0
    MODE_CLIENT = 1
    MAX_PLAYERS = 2
    
    
    EVENT_BOARD_CHANGED = 20


    def __init__(self, mode):
        
        if mode == self.MODE_SERVER:
            self.__state = ServerStartState(self)
        else:
            self.__state = ClientStartState(self)

        self.__players = []
        self.boards = {}
        self.__observers = []
        
    
    def getBoardsFromPerspective(self, playerId):
        otherID = [x for x in self.__players if x != playerId][0]
        return [self.boards[playerId], self.boards[otherID].getEnemyView()]


    def updateBoards(self, boardDict):
        changed = False
        
        for pId in boardDict:
            if self.boards[pId] != boardDict[pId]:
                changed = True
                self.boards[pId] = boardDict[pId]
        
        if changed:    
            self.emmit(self.EVENT_BOARD_CHANGED)
        
    #region Observer
    def registerObserver(self, observer):
        assert isinstance(observer, Observer)
        self.__observers.append(observer)
        
    def unregisterObserver(self, observer):
        assert isinstance(observer, Observer)
        self.__observers.remove(observer)
        
    def emmit(self, event):
        for o in self.__observers:
            o.recieveEvent(event)
    
    def inProgress(self):
        return True
    
    def full(self):
        return self.MAX_PLAYERS <= len(self.__players)
    
    def canAddPlayer(self, clinetId):
        room = not self.full()
        playerNotJoined = self.__players.count(clinetId) == 0
        
        return room and playerNotJoined
        
    def addPlayers(self, player):
        self.__players.append(player)
        self.boards[player] = Board(5,5)
 
    def update(self, packetDict, inputs = None):
        packets = self.__state.handle(packetDict, inputs)
        self.__state = self.__state.nextState()
        return packets
