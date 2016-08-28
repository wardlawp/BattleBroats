'''
Created on Aug 24, 2016

@author: Philip Wardlaw
'''

from game_states import GameState
from client_play import ClientPlayState
from server_start import ServerStartState, ServerPlayState
from Protocol import Response, Request, StringMessage

class ClientStartState(GameState):
    'An abstract class for expressing client game behaviour'
    
    def __init__(self, game):
        GameState.__init__(self, game)
        
        self.__askedToJoin = False
        self.__serverAcknowledgedJoin = False
        self.__gameStarting = False
    

    def __handleServerResponses(self, response):
        if response and response.status == Response.STATUS_OK:
            content = response.content
            if isinstance(content, StringMessage):
                msg = content.msg
                if msg == ServerStartState.JOIN:
                    self.__serverAcknowledgedJoin = True
                if msg == ServerPlayState.START:
                    self.__gameStarting = True
                    self.game.addPlayers('self')
                    self.game.addPlayers('other')


    def __generateRequests(self):
        request = None
        if not self.__askedToJoin:
            request = Request(StringMessage(ServerStartState.JOIN))
            self.__askedToJoin = True
        elif not self.__gameStarting:
            request = Request(StringMessage(ServerPlayState.START))
        return request

    def handle(self, response, inputs):

        #Handle Responses
        self.__handleServerResponses(response) 
                    
        #Ask Server Questions
        return self.__generateRequests()
            

    
    
    def nextState(self):
        "Get the GameState that should be used next game loop"
        if self.__gameStarting:
            return ClientPlayState(self.game) #may cause self not to get GC?
        else:
            return self