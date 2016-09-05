'''
Created on Aug 24, 2016

@author: Philip Wardlaw
'''
from game_states import ServerState


class ServerEndState(ServerState):
    """

    """
    
    FINISHED = 'FINISHED' 
    VIEW = 'VIEW'
    
    def __init__(self, game):
        ServerState.__init__(self, game)



    def registerHandlers(self):
        #define methods
        def strHandler(content, clientId):
            if content == self.VIEW:
                return self.game.getBoardsFromPerspective(clientId) + [self.FINISHED]
            else:
                return self.FINISHED
            
        #register methods
        self.handlers[unicode.__name__] = strHandler
        self.handlers[str.__name__] = strHandler

            
    
    def handle(self, packetsDict, inputs = None):
        if len(self.game.players()) == 0:
            self.game.finished = True
        
        responseContent= self.handlePackets(packetsDict)
        return self.packageContent(responseContent)
        


    def nextState(self):
        "This is the final state"
        return self


    
    
