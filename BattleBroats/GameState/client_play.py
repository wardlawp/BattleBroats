'''
Created on Aug 24, 2016

@author: Philip Wardlaw
'''

from game_states import GameState
from server_play import ServerPlayState
from Network import Packet
from BattleBroats.attack_order import AttackOrder

class ClientPlayState(GameState):
    'An abstract class for expressing client game behaviour'

    def __init__(self,game):
        GameState.__init__(self,game)
        self.__attackOrder = None
        self.ourGo = False

    def handle(self, packets, inputs):
        #Handle Responses
        self.__handleIncomingPackets(packets) 
        
        #Handle user input
        self.__handleUserInput(inputs)
        
        #Ask Server Questions
        return self.__outgoingPacket()
    
    def __handleUserInput(self, inputs):
        self.__attackOrder = None
        if isinstance(inputs, list):
            self.__attackOrder = AttackOrder(inputs[0], inputs[1])

    def __handleIncomingPackets(self, packets):
        
        for packet in packets:
    
            content = packet.content
            
            if isinstance(content, list) and len(content) == 2:
                boards = {'self': content[0], 'other': content[1]}
                self.game.updateBoards(boards)
                    
            if self.unicodeOrString(content) and content == ServerPlayState.GO:
                print "My go"
                self.ourGo = True
            
            if self.unicodeOrString(content) and content == ServerPlayState.NGO:
                self.ourGo = False


    def __outgoingPacket(self):
        return [Packet(ServerPlayState.VIEW)]

    

    def nextState(self):
        "Get the GameState that should be used next game loop"
        return self
    
    
