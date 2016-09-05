'''
Created on Aug 24, 2016

@author: Philip Wardlaw
'''

from game_states import ClientState
from client_play import ClientPlayState
from server_start import ServerStartState, ServerPlayState
import BattleBroats.constants as gc


class ClientStartState(ClientState):
    """
    State class defining behaviour of client at start of game
    Ask to join, then ask has the game started
    """
    
    def __init__(self, game):
        ClientState.__init__(self, game)
        

        self.__joined = False
        self.__gameStarting = False
    

    def registerHandlers(self):
        #define methods
        def strHandler(content):
            if content == ServerStartState.JOIN:
                self.__joined = True
            elif content == ServerPlayState.START:
                self.__gameStarting = True
                self.game.addPlayers(gc.CLIENT_SELF)
                self.game.addPlayers(gc.CLIENT_OTHER)
                

        
        #register methods
        self.handlers[unicode.__name__] = strHandler
        self.handlers[str.__name__] = strHandler
              


    def questions(self):

        if not self.__joined:
            return [ServerStartState.JOIN]
        elif not self.__gameStarting:
            return [ServerPlayState.START]
        
        return []

    def handle(self, packets, inputs):

        self.handlePackets(packets)
        responseContent = self.questions()
        
        return self.packageContent(responseContent)
            

    
    
    def nextState(self):
        "Get the GameState that should be used next game loop"
        if self.__gameStarting:
            return ClientPlayState(self.game) #may cause self not to get GC?
        else:
            return self