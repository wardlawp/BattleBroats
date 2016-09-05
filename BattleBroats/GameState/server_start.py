'''
Created on Aug 24, 2016

@author: Philip Wardlaw
'''
from game_states import ServerState
from server_play import ServerPlayState


class ServerStartState(ServerState):
    """
    State class defining behaviour of server at start of game
    Wait for players to join, when enough have joined progress state
    """
    
    JOIN = 'JOIN'
    
    def __init__(self, game):
        ServerState.__init__(self, game)
        self.__complete = False


    def registerHandlers(self):
        #define methods
        def strHandler(content, clientId):
            if content == self.JOIN:
                if self.game.canAddPlayer(clientId):
                    self.game.addPlayers(clientId)
                
                self.__complete = self.game.full()
                
                return [self.JOIN]
            
            return []
        #register methods
        self.handlers[unicode.__name__] = strHandler
        self.handlers[str.__name__] = strHandler
            
    
    def handle(self, packetsDict, inputs = None):
        responseContent= self.handlePackets(packetsDict)
        
        return self.packageContent(responseContent)
        


    def nextState(self):
        "Get the GameState that should be used next game loop"
        if self.__complete:
            return ServerPlayState(self.game) #may cause self not to get GC
        else:
            return self
            
    
    
