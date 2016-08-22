'''
Created on Aug 16, 2016

@author: Philip Wardlaw
'''
from Packet import Packet
from Transmittable import Transmittable
import BattleBroats  #TODO does this package have to know of other packages?
import Protocol

class Response(Packet):
    '''
    classdocs
    '''
    STATUS_OK=1
    STATUS_NOT_OK=2
    STATUS_ERROR=3
    STATUSES = [STATUS_OK, STATUS_NOT_OK, STATUS_ERROR]

    #TODO refactor constructor with Request
    def __init__(self, status, content = None):
        "Responses do not necessarily have content"
        if content:
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
    
    @staticmethod
    def deserialize(string):
        status, contentType, content = Packet.deserialize(string)
        
        contentObj = None
        if contentType:
            contentObj = eval(contentType).deserialize(content)
        return Response(status, contentObj) #TODO: refactor this smellynes!!