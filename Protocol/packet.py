'''
Created on Aug 16, 2016

@author: Philip Wardlaw
'''
import json
from abc import ABCMeta, abstractproperty
from transmittable import Transmittable


class Packet(object):
    "Packet of information that can be sent or recieved"
    __metaclass__ = ABCMeta
    
    STATUS_KEY='status'
    CONTENT_MODULE_KEY='contentModule'
    CONTENT_CLASS_KEY='contentClass'
    CONTENT_KEY='content'
    KEYS = [STATUS_KEY, CONTENT_PACKAGE_KEY, CONTENT_CLASS_KEY, CONTENT_KEY]

    @abstractproperty
    def status(self):
        "Status attribute must return integer"
        return
    
       
    @abstractproperty
    def content(self):
        "Content attribute must return Transmittable"
        return 

    
    @staticmethod    
    def __deserializePayload(string):
        "Returned string is JSON"
        

        data = json.loads(string)

        for key in Packet.KEYS:
            assert key in data.keys(), "Serial data is missing elements"
        
        return  [data[Packet.STATUS_KEY], 
                data[Packet.CONTENT_MODULE_KEY],
                data[Packet.CONTENT_CLASS_KEY],
                data[Packet.CONTENT_KEY]]

    @staticmethod
    def deserialize(_type, string):
        "Construct a _type with internal Transmittable from serialized Packet"
        status, contentModule, contentClass, content = Packet.__deserializePayload(string)

        _module = __import__(contentPackage)
        _class = getattr(_module, contentClass)

        assert issubclass(_class, Transmittable)

        return _type(_class.deserialize(content))
    
    def serialize(self):
        "Prepare the body of the Packet to be transmitted"
        assert isinstance(self, Packet), 'Invalid object supplied, must be of type Packet'
        
        status = self.status
        contentType = None
        content = None
        
        if self.content:
            contentModule =  self.content.__module__ 
            contentClass = self.content.__class__.__name__
            content = self.content.serialize()
        
        data = {Packet.STATUS_KEY: status, 
                Packet.CONTENT_MODULE_KEY: contentModule, 
                Packet.CONTENT_CLASS_KEY: contentClass, 
                Packet.CONTENT_KEY: content}

        return json.dumps(data)
