'''
Created on Aug 24, 2016

@author: Philip Wardlaw
'''
from game_states import GameState
from server_play import ServerPlayState
from Network import Packet

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
        responsePackets= {}
        
        for clientId in packetsDict:
            packets = packetsDict[clientId]
            responsePackets[clientId] = self.__handlePackets(clientId, packets)
            
                
        return responsePackets

    
    def __handlePackets(self, clientId, packets):
        responsePackets= []
        for packet in packets:
            content = packet.content
            
            if self.unicodeOrString(content) and content == self.JOIN:
                if self.game.canAddPlayer(clientId):
                    self.game.addPlayers(clientId)
                
                self.__complete = self.game.full()
                
                responsePackets.append(Packet(self.JOIN))
        
        return responsePackets   
    
    

    def nextState(self):
        "Get the GameState that should be used next game loop"
        if self.__complete:
            return ServerPlayState(self.game) #may cause self not to get GC
        else:
            return self
            
    
    
