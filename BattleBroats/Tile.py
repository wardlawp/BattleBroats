'''
Created on Aug 16, 2016

@author: Philip Wardlaw
'''

import abc
from Protocol import Transmittable

class Tile(Transmittable):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    
    def serialize(self):
        return 'hi'
    

    def deserialize(self, string):
        print string