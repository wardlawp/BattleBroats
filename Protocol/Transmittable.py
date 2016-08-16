'''
Created on Aug 16, 2016

@author: Philip Wardlaw
'''
from abc import ABCMeta, abstractmethod

class Transmittable(object):
    'Any object that wants to be transmitted must implement this class'
    __metaclass__ = ABCMeta


    @abstractmethod
    def serialize(self):
        "Serialize the objects data into JSON"
        return
    
    @abstractmethod
    def deserialize(string):
        "Deserialize string to object"
        return
        