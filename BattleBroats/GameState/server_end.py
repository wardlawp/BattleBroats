'''
Created on Aug 24, 2016

@author: Philip Wardlaw
'''
from game_states import ServerGameState
from Protocol import Request, StringMessage

class ServerGameState(ServerGameState):
    'State class defining behaviour of server at start of game'
    
    JOIN = 'JOIN'
    
    def __init__(self, game):
        ServerGameState.__init__(self, game)
        self.__complete = False
        self.__responses = {}
    
    def handle(self, packetsDict, inputs = None):
        responses = {}
        
        for id in packetsDict:
            currResonses = len(responses)
            request = packetsDict[id]
            assert isinstance(request, Request)
            
            _type = type(request.content)
            
            if _type == StringMessage:
                verb = request.content.msg
                
                if verb == self.JOIN:
                    self.addPlayers(id)
                    responses[id] = Protocol.Response(self.__boards[id], 1)
                    
        self.__responses = responses

    

    def responses(self):
        "Get Responses after handle()"
        return
    

    def nextState(self):
        "Get the GameState that should be used next game loop"
        if self.__complete:
            
    
    
