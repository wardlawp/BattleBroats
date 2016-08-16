'''
Created on Aug 16, 2016

@author: Philip Wardlaw
'''

import abc
from Protocol import Transmittable
class Tile(Transmittable.Transmittable):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    
    def serialize(self):
        return 'hi'
    

    @staticmethod
    def deserialize(string):
        print string