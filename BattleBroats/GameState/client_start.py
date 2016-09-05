'''
Created on Aug 24, 2016

@author: Philip Wardlaw
'''

from game_states import GameState
from client_play import ClientPlayState
from server_start import ServerStartState, ServerPlayState
from Network import Packet


class ClientStartState(GameState):
    'An abstract class for expressing client game behaviour'
    
    def __init__(self, game):
        GameState.__init__(self, game)
        
        self.__askedToJoin = False
        self.__serverAcknowledgedJoin = False
        self.__gameStarting = False
    

    def __handleServerPackets(self, packets):
        for packet in packets:
            content = packet.content
            if self.unicodeOrString(content):
    
                if content == ServerStartState.JOIN:
                    self.__serverAcknowledgedJoin = True
                if content == ServerPlayState.START:
                    self.__gameStarting = True
                    self.game.addPlayers('self')
                    self.game.addPlayers('other')


    def __generatePackets(self):
        packets = []
        if not self.__askedToJoin:
            packets.append(Packet(ServerStartState.JOIN))
            self.__askedToJoin = True
        elif not self.__gameStarting:
            packets.append(Packet(ServerPlayState.START))
        return packets

    def handle(self, packets, inputs):

        #Handle Responses
        self.__handleServerPackets(packets) 
                    
        #Ask Server Questions
        return self.__generatePackets()
            

    
    
    def nextState(self):
        "Get the GameState that should be used next game loop"
        if self.__gameStarting:
            return ClientPlayState(self.game) #may cause self not to get GC?
        else:
            return self