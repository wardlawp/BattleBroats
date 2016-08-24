'''
Created on Aug 16, 2016

@author: Philip Wardlaw
'''
from packet import Packet
from transmittable import Transmittable


class Request(Packet):
    '''
    classdocs
    '''
    STATUS_OK = 1



    #TODO refactor constructor with Response
    def __init__(self, content):
        assert isinstance(content, Transmittable), 'Content must implement Transmittable Interface'

        
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
        status, contentType, content = Packet.deserialize(string)
        print status, contentType, content
        
        cls = eval(contentType)
        return Request(cls.deserialize(content))