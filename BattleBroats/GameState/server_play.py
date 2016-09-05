'''
Created on Aug 24, 2016

@author: Philip Wardlaw
'''
from game_states import GameState
from Network import Packet
from BattleBroats.attack_order import AttackOrder


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
    NGO = 'NGO'
    
    def __init__(self, game):
        GameState.__init__(self, game)
        self.__currPlayerIdx = 0
        self.__complete = False
        self.__firstIter = True

    
    def handle(self, packetsDict, inputs = None):
        self.__responsPackets= {}
        
        for clientId in packetsDict:
            self.__responsPackets[clientId] = []
            packets = packetsDict[clientId]
            self.__handleRequests(clientId, packets)
        
        if self.__firstIter:
            clientId = self.game.player(0)
            self.__responsPackets[clientId] = [Packet(self.GO)]
            self.__firstIter = False
                
        return self.__responsPackets

    
    def __handleRequests(self, clientId, packets):

        for packet in packets:
            content = packet.content
            if self.unicodeOrString(content):
            
                if content == self.START:
                    self.__responsPackets[clientId].append(Packet(self.START))
                elif content == self.VIEW:
                    boards = self.game.getBoardsFromPerspective(clientId)
                    self.__responsPackets[clientId].append(Packet(boards))
            
            elif isinstance(content, AttackOrder):
                if self.game.player(self.__currPlayerIdx) == clientId:
                    otherPlayerName = self.game.player(self.incrementPlayerIdx(self.__currPlayerIdx))
                    otherBoard = self.game.boards(otherPlayerName)
                    
                    otherBoard.shoot(content)
                    self.__responsPackets[clientId].append(Packet(self.NGO))
                    self.__responsPackets[otherPlayerName].append(Packet(self.GO))


     

    def incrementPlayerIdx(self, idx):
        return (idx+1)%2

    def nextState(self):
        "Get the GameState that should be used next game loop"
        if self.__complete:
            return ServerPlayState(self.game) #may cause self not to get GC
        else:
            return self
            
    
    

    
    
