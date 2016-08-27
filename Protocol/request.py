'''
Created on Aug 16, 2016

@author: Philip Wardlaw
'''
from packet import Packet
from transmittable import Transmittable


class Request(Packet):
    "Request Packet for sending a request over Network"
    STATUS_OK = 1


    def __testInputs(self, content):
        if isinstance(content, list):
            errorMsg = 'Array elements must be objects implementing the Transmittable Interface'
            for c in content:
                assert isinstance(c, Transmittable), errorMsg
        
        else:
            errorMsg = 'Content must implement Transmittable Interface'
            assert isinstance(content, Transmittable), errorMsg

    def __init__(self, content, status = STATUS_OK):
        
        self.__testInputs(content)
        
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
        return Packet.deserialize(Request, string)
