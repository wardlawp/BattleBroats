'''
Created on Aug 24, 2016

@author: Philip Wardlaw
'''

from game_states import GameState
from server_play import ServerPlayState
from Protocol import Response, Request, StringMessage
from .. import Board

class ClientPlayState(GameState):
    'An abstract class for expressing client game behaviour'

    def handle(self, response, inputs):
        #Handle Responses
        self.__handleServerResponses(response) 
                    
        #Ask Server Questions
        return self.__generateRequests()
    

    def __handleServerResponses(self, response):
        if response and response.status == Response.STATUS_OK:
            content = response.content
            if isinstance(content, list) and isinstance(content[0], StringMessage):
                msg = content[0].msg
                if msg == ServerPlayState.VIEW:
                    boards = {'self': content[1], 'other': content[2]}
                    self.game.updateBoards(boards)


    def __generateRequests(self):
        request = Request(StringMessage(ServerPlayState.VIEW))
        return request
    

    def nextState(self):
        "Get the GameState that should be used next game loop"
        return self
    
    
