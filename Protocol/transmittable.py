'''
Created on Aug 16, 2016

@author: Philip Wardlaw
'''
from abc import ABCMeta, abstractmethod

class Transmittable(object):
    'An Abstract Class for transmitting Data via Packets'
    __metaclass__ = ABCMeta


    @abstractmethod
    def serialize(self):
        "Serialize the Transmittable object into JSON"
        return
    
    @staticmethod
    @abstractmethod
    def deserialize(data):
        "Create Transmittable object from JSON data"
        return
        
