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
    KEYS = [STATUS_KEY, CONTENT_MODULE_KEY, CONTENT_CLASS_KEY, CONTENT_KEY]

    @abstractproperty
    def status(self):
        "Status attribute must return integer"
        return
    
       
    @abstractproperty
    def content(self):
        "Content attribute must return Transmittable"
        return 

    @staticmethod
    def testConstructorContentInputs(content):
        if isinstance(content, list):
            errorMsg = 'Array elements must be objects implementing the Transmittable Interface'
            for c in content:
                assert isinstance(c, Transmittable), errorMsg
        
        else:
            errorMsg = 'Content must implement Transmittable Interface'
            assert isinstance(content, Transmittable), errorMsg
    
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

        transmittables = Packet.__deserializeContentPayload(contentModule, contentClass, content)

        return _type(transmittables, status)
    
    def serialize(self):
        "Prepare the body of the Packet to be transmitted"
        assert isinstance(self, Packet), 'Invalid object supplied, must be of type Packet'
        
        status = self.status
        contentModule, contentClass, content = self.__serializeContentPayload()
        
       
        data = {Packet.STATUS_KEY: status, 
                Packet.CONTENT_MODULE_KEY: contentModule, 
                Packet.CONTENT_CLASS_KEY: contentClass, 
                Packet.CONTENT_KEY: content}

        return json.dumps(data)
    
    def __serializeContentPayload(self):
        if self.content == None:
            return None, None, None
        
        elif isinstance(self.content, list):
            
            contentModule =  []
            contentClass = []
            content = []
            for c in self.content:
                contentModule.append(c.__module__) 
                contentClass.append(c.__class__.__name__)
                content.append(c.serialize())
                
            return contentModule, contentClass, content
        else:
            contentModule =  self.content.__module__ 
            contentClass = self.content.__class__.__name__
            content = self.content.serialize()
            
            return contentModule, contentClass, content
    
    @staticmethod
    def __deserializeContentPayload(contentModule, contentClass, content):
        
        if not isinstance(contentModule, list):
                return Packet.__deserializeTransmittable(contentModule,
                                                        contentClass,
                                                        content)
            
        transmittables = [] 
        for i in range(len(contentModule)):
            transmittables.append(Packet.__deserializeTransmittable(contentModule[i],
                                                        contentClass[i],
                                                        content[i]))
        return transmittables
        
    @staticmethod
    def __deserializeTransmittable( contentModule, contentClass, content):
        _module = __import__(contentModule)
        _class = getattr(_module, contentClass)

        assert issubclass(_class, Transmittable)
        obj = _class.deserialize(content)
        return obj
            
        
