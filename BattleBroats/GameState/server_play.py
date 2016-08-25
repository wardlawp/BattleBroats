'''
Created on Aug 24, 2016

@author: Philip Wardlaw
'''
from game_states import ServerGameState
from Protocol import Request, StringMessage

class ServerGamePlay(ServerGameState):
    """
    State class defining behaviour of server during a game
    
    Process Turns
        player asks for VIEW
            respond with game board
        player has turn and attacks
            update board
            
            new player joins?
                send OK and game boards
                
            all players joined?
                move to next state
    
    """
    
    VIEW = 'VIEW'
    
    def __init__(self, game):
        ServerGameState.__init__(self, game)
        self.__complete = False
        self.__responses = {}
    
    def handle(self, packetsDict, inputs = None):

    

    def responses(self):
        "Get Responses after handle()"
        return
    

    def nextState(self):
        "Get the GameState that should be used next game loop"
        return
            
    
    
