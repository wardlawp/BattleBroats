'''
Created on Aug 24, 2016

@author: Philip Wardlaw
'''

from abc import ABCMeta, abstractmethod

class GameState(object):
    'An abstract class for expressing game behaviour'
    __metaclass__ = ABCMeta

    def __init__(self, game):
        self.game = game

    @abstractmethod
    def handle(self, packetsDict, inputs):
        "Handle communication"
        return
    


    
    @abstractmethod
    def nextState(self):
        "Get the GameState that should be used next game loop"
        return
    
    @staticmethod
    def unicodeOrString(_input):
        return isinstance(_input, str) or isinstance(_input,unicode)