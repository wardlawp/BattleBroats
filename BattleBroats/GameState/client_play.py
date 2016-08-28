'''
Created on Aug 24, 2016

@author: Philip Wardlaw
'''

from game_states import GameState
from server_play import ServerPlayState
from Protocol import Response, Request, StringMessage

class ClientPlayState(GameState):
    'An abstract class for expressing client game behaviour'

    def __init__(self,game):
        GameState.__init__(self,game)
        self.__attackOrder = None

    def handle(self, response, inputs):
        #Handle Responses
        self.__handleServerResponses(response) 
        
        #Handle user input
        self.__handleUserInput(inputs)
        
        #Ask Server Questions
        return self.__generateRequests()
    
    def __handleUserInput(self, inputs):
        self.__attackOrder = None
        if isinstance(inputs, list):
            self.__attackOrder = inputs

    def __handleServerResponses(self, response):
        
        if not response:
            return
        
        if response.status == Response.STATUS_OK:
            content = response.content
            
            if isinstance(content, list) and isinstance(content[0], StringMessage):
                msg = content[0].msg
                if msg == ServerPlayState.VIEW:
                    boards = {'self': content[1], 'other': content[2]}
                    self.game.updateBoards(boards)
                    
            if isinstance(content, StringMessage) and content.msg == ServerPlayState.GO:
                self.game.setTurn('self')
        
        if response.status == Response.STATUS_NO:
            if isinstance(content, StringMessage) and content.msg == ServerPlayState.GO:
                self.game.setTurn('other')


    def __generateRequests(self):
        request = Request(StringMessage(ServerPlayState.VIEW))
        return request
    

    def nextState(self):
        "Get the GameState that should be used next game loop"
        return self
    
    
