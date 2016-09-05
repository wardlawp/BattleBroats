'''
Created on Aug 24, 2016

@author: Philip Wardlaw
'''

from game_states import ClientState



class ClientEndState(ClientState):
    """
    The final ClientState, simply mark the game as complete
    """
    
    def __init__(self,game):
        ClientState.__init__(self,game)

    def registerHandlers(self):
        pass
              

    def handle(self, packets, _input):
        self.game.finished = True
            

    def nextState(self):
        "This is the final state"
        return self