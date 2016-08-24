'''
Created on Aug 21, 2016

@author: Philip Wardlaw
'''
from transmittable import Transmittable


class StringMessage(Transmittable):
    """
    A Transmittable Class that contains a string.
    Can be transmitted within a Packet over a GameSocket
    """

    def __init__(self, msg):
        assert isinstance(msg, str) or isinstance(msg, unicode)
        self.msg = msg

    def __str__(self):
        return self.msg

    def serialize(self):
        return self.msg
    
    @staticmethod
    def deserialize(data):
        return StringMessage(data)
        
