'''
Created on Aug 24, 2016

@author: Philip Wardlaw
'''
from .. import Game
from game_states import GameState

class ClientGameState(GameState):
    'An abstract class for expressing client game behaviour'

    def handle(self, packets, inputs):
        "Handle communication"
        return
    
    @abstractmethod
    def responses(self):
        "Get Responses after handle()"
        return
    
    @abstractmethod
    def nextState(self):
        "Get the GameState that should be used next game loop"
        return
    
    
