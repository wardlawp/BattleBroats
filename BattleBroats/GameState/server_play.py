'''
Created on Aug 24, 2016

@author: Philip Wardlaw
'''
from game_states import GameState
from Protocol import Response, StringMessage

class ServerPlayState(GameState):
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
    START = 'START'
    VIEW = 'VIEW'
    GO = 'GO'
    
    def __init__(self, game):
        GameState.__init__(self, game)
        self.__complete = False

    
    def handle(self, packetsDict, inputs = None):
        responses = {}
        
        for clientId in packetsDict:

            request = packetsDict[clientId]
            responses[clientId] = self.__handleRequests(clientId, request.content)
            
                
        return responses

    
    def __handleRequests(self, clientId, content):
        
        if isinstance(content, StringMessage):
            
            msg = content.msg
            if msg == self.START:
                return Response(StringMessage(self.START), Response.STATUS_OK)
            elif msg == self.VIEW:
                boards = self.game.getBoardsFromPerspective(clientId)
                payload = [StringMessage(self.VIEW)] + boards
                return Response(payload, Response.STATUS_OK)
                
           

     

    

    def nextState(self):
        "Get the GameState that should be used next game loop"
        if self.__complete:
            return ServerPlayState(self.game) #may cause self not to get GC
        else:
            return self
            
    
    

    
    
