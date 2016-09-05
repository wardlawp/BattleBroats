'''
Created on Aug 24, 2016

@author: Philip Wardlaw
'''
from game_states import ServerState
from BattleBroats.attack_order import AttackOrder
import BattleBroats.constants as gc


class ServerPlayState(ServerState):
    """
    State class defining behaviour of server at start of game
    Wait for players to join, when enough have joined progress state
    """
    
    START = 'START'
    VIEW = 'VIEW'
    GO = 'GO'
    NGO = 'NGO'
    
    def __init__(self, game):
        ServerState.__init__(self, game)
        self.__complete = False
        self.__currPlayerIdx = 0
        self.__clientUpToDate = {}
        
        for pId in game.players():
            self.__clientUpToDate[pId] = False

    def incrementPlayerIdx(self, idx):
        return (idx+1)%gc.MAX_PLAYERS

    def registerHandlers(self):
        #define methods
        def strHandler(content, clientId):
            if content == self.START:
                return [self.START]

            elif content == self.VIEW:
                
                if not self.__clientUpToDate[clientId]:
                
                    responseContent = self.game.getBoardsFromPerspective(clientId)
                   
                    if self.game.player(self.__currPlayerIdx) == clientId:
                        responseContent.append(self.GO)
                    else:
                        responseContent.append(self.NGO)
                    
                    self.__clientUpToDate[clientId] = True
                    return responseContent
            

        
        def attackHandler(content, clientId):
            if self.game.player(self.__currPlayerIdx) == clientId:
                #preemptively change currently player idx
                self.__currPlayerIdx = self.incrementPlayerIdx(self.__currPlayerIdx)
                
                otherPlayerId = self.game.player(self.__currPlayerIdx)
                otherBoard = self.game.boards[otherPlayerId]
                otherBoard.shoot(content)
                
                #Flag both players out of date
                for pId in self.__clientUpToDate:
                    self.__clientUpToDate[pId] = False
                    

                

            
        #register methods
        self.handlers[unicode.__name__] = strHandler
        self.handlers[str.__name__] = strHandler
        self.handlers[AttackOrder.__name__] = attackHandler
            
    
    def handle(self, packetsDict, inputs = None):
        responseContent= self.handlePackets(packetsDict)
        
        return self.packageContent(responseContent)
        


    def nextState(self):
        "Get the GameState that should be used next game loop"
        return self


    
    
