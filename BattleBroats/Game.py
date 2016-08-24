'''
Created on Aug 16, 2016

@author: Philip Wardlaw
'''

from board import Board
import Protocol
class Game(object):
    
    #Request Verbs
    JOIN = 'JOIN'
    VIEW = 'VIEW'
    


    def __init__(self):

        self.__players = []
        self.__boards = {}
        

    def inProgress(self):
        return True
        
    def addPlayers(self, player):
        print player
        self.__players.append(player)
        self.__boards[player] = Board(5,5)
 
    def processRequest(self, requestDict):
        responses = {}
        for id in requestDict:
            request = requestDict[id]
            assert isinstance(request, Protocol.request)
            
            _type = type(request.content)
            
            if _type == Protocol.StringMessage:
                verb = request.content.serialize()
                if verb == self.VIEW:
                    responses[id] = Protocol.Response(1, self.__boards[id])
                elif verb == self.JOIN:
                    self.addPlayers(id)
                    responses[id] = Protocol.Response(1, self.__boards[id])
                    
        return responses