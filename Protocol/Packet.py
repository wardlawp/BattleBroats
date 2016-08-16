'''
Created on Aug 16, 2016

@author: Philip Wardlaw
'''
import json
from abc import ABCMeta, abstractproperty
from Transmittable import Transmittable


class Packet(object):
    '''
    classdocs
    '''
    __metaclass__ = ABCMeta
    
    STATUS_KEY='status'
    CONTENT_TYPE_KEY='contentType'
    CONTENT_KEY='content'
    KEYS = [STATUS_KEY, CONTENT_TYPE_KEY, CONTENT_KEY]

    @abstractproperty
    def status(self):
        return
    
       
    @abstractproperty
    def content(self):
        self 

    
    @staticmethod    
    def deserialize(string):
        "Returned string is JSON"
        

        data = json.loads(string)

        for key in Packet.KEYS:
            assert key in data.keys(), "Serial data is missing elements"
        
        return  [data[Packet.STATUS_KEY], 
                data[Packet.CONTENT_TYPE_KEY],
                data[Packet.CONTENT_KEY]]
        
    
    
    

    @staticmethod  
    def serialize(obj):
        assert isinstance(obj, Packet), 'Invalid object supplied, must be of type Packet'
        
        status = obj.status
        content = obj.content
        contentClass = content.__class__
        contentType =  contentClass.__module__ +  '.' + contentClass.__name__
        content = content.serialize()
        
        data = {Packet.STATUS_KEY: status, 
                Packet.CONTENT_TYPE_KEY: contentType, 
                Packet.CONTENT_KEY: content}

        return json.dumps(data)
