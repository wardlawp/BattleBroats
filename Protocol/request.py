'''
Created on Aug 16, 2016

@author: Philip Wardlaw
'''
from packet import Packet
from transmittable import Transmittable


class Request(Packet):
    "Request Packet for sending a request over Network"
    STATUS_OK = 1

    def __init__(self, content):
        errorMsg = 'Content must implement Transmittable Interface'
        assert isinstance(content, Transmittable), errorMsg
        
        self.__status =  Request.STATUS_OK
        self.__content = content
        
    @property
    def status(self):
        return self.__status
    

    @property
    def content(self):
        return self.__content
    
        
    @staticmethod
    def deserialize(string):
        Packet.deserialize(Request, string)
