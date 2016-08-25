'''
Created on Aug 24, 2016

@author: Philip Wardlaw
'''

from game_states import ClientGameState

class ClientGameStart(ClientGameState):
    'An abstract class for expressing client game behaviour'
    
    
    def handle(self, packets, inputs):
        "Handle communication"
        return

    def requests(self):
        "Get Responses after handle()"
        return
    
    @abstractmethod
    def nextState(self):
        "Get the GameState that should be used next game loop"
        return
    
    
