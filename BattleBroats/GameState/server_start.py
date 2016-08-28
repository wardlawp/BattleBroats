'''
Created on Aug 24, 2016

@author: Philip Wardlaw
'''
from game_states import GameState
from server_play import ServerPlayState
from Protocol import Response, StringMessage

class ServerStartState(GameState):
    """
    State class defining behaviour of server at start of game
    
    Wait for players to join
        new player JOINs?
            send OK and game board
            
        all players joined?
            move to next state
    
    """
    
    JOIN = 'JOIN'
    
    def __init__(self, game):
        GameState.__init__(self, game)
        self.__complete = False

    
    def handle(self, packetsDict, inputs = None):
        responses = {}
        
        for clientId in packetsDict:

            request = packetsDict[clientId]
            responses[clientId] = self.__handleRequests(clientId, request.content)
            
                
        return  responses

    
    def __handleRequests(self, clientId, content):
        
        if isinstance(content, StringMessage) and content.msg == self.JOIN:
            if self.game.canAddPlayer(clientId):
                self.game.addPlayers(clientId)
            
            self.__complete = self.game.full()
            
            return Response(StringMessage(self.JOIN), Response.STATUS_OK)
        
        return Response(None, Response.STATUS_NO)      
     

    

    def nextState(self):
        "Get the GameState that should be used next game loop"
        if self.__complete:
            return ServerPlayState(self.game) #may cause self not to get GC
        else:
            return self
            
    
    
