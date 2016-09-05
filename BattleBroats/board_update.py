'''
Created on Sept 05, 2016

@author: Philip Wardlaw
'''
from board import Board
from Network import Transmittable
import constants as gc

class BoardUpdate(Transmittable):
    BOARD_KEY = 'board'
    PLAYER_KEY = 'pId'
    
    def __init__(self, board, pId = gc.CLIENT_SELF):
        assert isinstance(board, Board)
        assert pId in (gc.CLIENT_OTHER, gc.CLIENT_SELF)
        
        self.board = board
        self.pId = pId
        

    def serialize(self):
        content = {}
        content[self.PLAYER_KEY] = self.pId
        content[self.BOARD_KEY] = self.board.serialize()
        return content
        
    
    @staticmethod
    def deserialize(content):
        return BoardUpdate(Board.deserialize(content[BoardUpdate.BOARD_KEY]), content[BoardUpdate.PLAYER_KEY])
    
    