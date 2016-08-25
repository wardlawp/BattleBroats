'''
Created on Aug 24, 2016

@author: Philip Wardlaw
'''
from .. import Game
from abc import ABCMeta, abstractmethod

class GameState(object):
    'An abstract class for expressing game behaviour'
    __metaclass__ = ABCMeta

    def __init__(self, game):
        assert isinstance(game, Game)
        self.game = game

    @abstractmethod
    def handle(self, packetsDict, inputs):
        "Handle communication"
        return
    
    @abstractmethod
    def responses(self):
        "Get Responses after handle()"
        return
    
    @abstractmethod
    def requests(self):
        "Get Requests after handle()"
        return
    
    @abstractmethod
    def nextState(self):
        "Get the GameState that should be used next game loop"
        return
    

class ServerGameState(GameState):
    def requests(self):
        "Server only responds, never makes requests"
        return None

class ClientGameState(GameState):
    def responses(self):
        "Client only requests, never makes responses"
        return None
