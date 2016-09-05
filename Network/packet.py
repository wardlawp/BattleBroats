'''
Created on Aug 16, 2016

@author: Philip Wardlaw
'''
import json
from transmittable import Transmittable
from datetime import datetime, time

class Packet(object):
    "Packet of information that can be sent or received"

    TIME_KEY='time stamp'
    CONTENT_MODULE_KEY='contentModule'
    CONTENT_CLASS_KEY='contentClass'
    CONTENT_KEY='content'
    TIMESTAMP_FORMAT="%Y-%m-%d %H:%M:%S.%f"
    KEYS = [ TIME_KEY, CONTENT_MODULE_KEY, CONTENT_CLASS_KEY, CONTENT_KEY]

    def __init__(self, content, timestamp = None):

        if content:
            self.__testConstructorContentInputs(content)
            self.content = content
            
        if timestamp is None:
            self.timestamp = datetime.now()
        else:
            self.timestamp = timestamp



    def __testConstructorContentInputs(self, content):
        def __test(item):
            errorMsg = 'Array elements must be objects implementing the Transmittable Interface or be an instance of str'
            isTransmittable = isinstance(item, Transmittable)
            isStr = isinstance(item, str) or isinstance(item, unicode)
            assert isTransmittable or isStr, errorMsg
            
        if isinstance(content, list):
            for c in content:
                __test(c)   
        
        else:
            __test(content)
            
    @staticmethod
    def deserialize(string):
        "Construct a _type with internal Transmittable from serialized Packet"
        timestampStr, contentModule, contentClass, content = Packet.__deserialize(string)
        
        transmittables = Packet.__deserializeContentPayload(contentModule, contentClass, content)
        timestamp = datetime.strptime(timestampStr, Packet.TIMESTAMP_FORMAT) 
        
        return Packet(transmittables, timestamp)
    
    def serialize(self):
        "Prepare the body of the Packet to be transmitted"

        contentModule, contentClass, content = self.__serializeContentPayload()
       
       

        data = {Packet.TIME_KEY: datetime.now().strftime(self.TIMESTAMP_FORMAT) , 
                Packet.CONTENT_MODULE_KEY: contentModule, 
                Packet.CONTENT_CLASS_KEY: contentClass, 
                Packet.CONTENT_KEY: content}

        return json.dumps(data)
    
    @staticmethod    
    def __deserialize(string):
        "Convert received string into primitive python types"
        
        data = json.loads(string)

        for key in Packet.KEYS:
            assert key in data.keys(), "Serial data is missing elements"
        
        return  [data[Packet.TIME_KEY],
                data[Packet.CONTENT_MODULE_KEY],
                data[Packet.CONTENT_CLASS_KEY],
                data[Packet.CONTENT_KEY]]

   
    
    
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
            if isinstance(self.content, str):
                return None, self.content.__class__.__name__, self.content
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
        

        if contentClass == 'str':
            return content
        else:
            _module = __import__(contentModule)
            _class = getattr(_module, contentClass)
            assert issubclass(_class, Transmittable)
            obj = _class.deserialize(content)
            return obj
            
        
