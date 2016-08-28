'''
Created on Aug 16, 2016

@author: Philip Wardlaw
'''
from packet import Packet
from transmittable import Transmittable

class Response(Packet):
    "Response Packet for sending a response over Network"
    STATUS_OK=1
    STATUS_NO=2
    STATUS_ERROR=3
    STATUSES = [STATUS_OK, STATUS_NO, STATUS_ERROR]


    def __init__(self, content, status):
        #Responses do not necessarily have content
        if content:
            self.testConstructorContentInputs(content)
        
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
        return Packet.deserialize(Response, string)
