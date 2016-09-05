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
    
    CLIENT_SELF = 'self'
    CLIENT_OTHER = 'other'
    
    BOARD_SIZE = (8,10)
    BROATS = (4,4,3,3,2,2)
    
    
    EVENT_BOARD_CHANGED = 20


    def __init__(self, mode):
        
        self.__mode = mode
        
        if mode == self.MODE_SERVER:
            self.state = ServerStartState(self)
        else:
            self.state = ClientStartState(self)

        self.__players = []
        self.boards = {}
        self.__observers = []
        
    
    def getBoardsFromPerspective(self, playerId):
        otherID = [x for x in self.__players if x != playerId][0]
        return [self.boards[playerId], self.boards[otherID].getEnemyView()]

    def player(self, idx):
        return self.__players[idx]
    
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
        self.boards[player] = Board(*self.BOARD_SIZE)
        if self.__mode == self.MODE_SERVER:
            self.boards[player].addBroats(self.BROATS)

            
 
    def update(self, packetDict, inputs = None):
        packets = self.state.handle(packetDict, inputs)
        self.state = self.state.nextState()
        return packets
