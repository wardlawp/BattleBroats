'''
Created on Aug 16, 2016

@author: Philip Wardlaw
'''
from Packet import Packet
from Transmittable import Transmittable
import BattleBroats

class Request(Packet):
    '''
    classdocs
    '''
    STATUS_OK = 1
    STATUSES = [STATUS_OK]


    def __init__(self, status, content):
        assert isinstance(content, Transmittable), 'Content must implement Transmittable Interface'
        assert status in self.STATUSES
        
        self.__status =  status

        self.__content = content
        
    @property
    def status(self):
        return self.__status
    

    @property
    def content(self):
        return self.__content
    

    def serialize(self):
        return Packet.serialize(self)
        
    @staticmethod
    def deserialize(string):
        status, contentType, content = Packet.deserialize(string)
        print contentType
        cls = eval(contentType)
        return Request(status, cls.deserialize(content))