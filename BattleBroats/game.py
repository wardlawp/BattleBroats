'''
Created on Aug 16, 2016

@author: Philip Wardlaw
'''

from GameState import ServerStartState, ClientStartState
from board import Board
from board_update import BoardUpdate
from observer import Observer
from subject import Subject
from constants import *

class Game(Subject):
    
    


    def __init__(self, mode):
        
        self.__mode = mode
        
        if mode == MODE_SERVER:
            self.state = ServerStartState(self)
        else:
            self.state = ClientStartState(self)

        self.__players = []
        self.boards = {}
        self.__observers = []
        
    
    def getBoardsFromPerspective(self, playerId):
        otherID = [x for x in self.__players if x != playerId][0]
        return [BoardUpdate(self.boards[playerId], CLIENT_SELF), 
                BoardUpdate(self.boards[otherID].getEnemyView(), CLIENT_OTHER)]

    def player(self, idx):
        return self.__players[idx]
    
    def players(self):
        return self.__players
    
    def updateBoards(self, boardDict):
        changed = False
        
        for pId in boardDict:
            if self.boards[pId] != boardDict[pId]:
                changed = True
                self.boards[pId] = boardDict[pId]
        
        if changed:    
            self.emmit(EVENT_BOARD_CHANGED)
        
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
        return MAX_PLAYERS <= len(self.__players)
    
    def canAddPlayer(self, clinetId):
        room = not self.full()
        playerNotJoined = self.__players.count(clinetId) == 0
        
        return room and playerNotJoined
        
    def addPlayers(self, player):
        self.__players.append(player)
        self.boards[player] = Board(*BOARD_SIZE)
        if self.__mode == MODE_SERVER:
            self.boards[player].addBroats(BROATS)

            
 
    def update(self, packetDict, inputs = None):
        packets = self.state.handle(packetDict, inputs)
        self.state = self.state.nextState()
        return packets
