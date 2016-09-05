'''
Created on Aug 24, 2016

@author: Philip Wardlaw
'''

from abc import ABCMeta, abstractmethod
from Network import Packet

class ContentNotHandledException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

class GameState(object):
    'An abstract class for expressing game behaviour'
    __metaclass__ = ABCMeta

    def __init__(self, game):
        self.game = game
        self.handlers = {}
        self.registerHandlers()


    @abstractmethod
    def handle(self, packetsDict, inputs):
        "Handle communication"
        return
    
    @abstractmethod
    def registerHandlers(self):
        "Handle communication"
        return
    
    
    @abstractmethod
    def nextState(self):
        "Get the GameState that should be used next game loop"
        return
    
    @staticmethod
    def unicodeOrString(_input):
        return isinstance(_input, str) or isinstance(_input,unicode)
    
    
    
class ServerState(GameState):
    
    def __init__(self, game):
        GameState.__init__(self, game)
    

    def handlePackets(self, packetsDict):
        "Handle incoming Client Packets, returns a dictionary of content to reply with"
        outgoingContent = {}
        
        def dispatchHandler(content, clientId):
            key = content.__class__.__name__
            if  self.handlers.has_key(key):
                return self.handlers[key](content, clientId)
            else:
                raise ContentNotHandledException("No content handler for " + key)
        
        for clientId in packetsDict:
            packets = packetsDict[clientId]
            outgoingContent[clientId] = []
            
            for packet in packets:
                for el in packet.content:
                    responseContent = dispatchHandler(el, clientId)
                    if isinstance(responseContent, list):
                        outgoingContent[clientId] += responseContent
                    elif responseContent is not None:
                        outgoingContent[clientId].append(responseContent)

            outgoingContent[clientId] = [x  for x in outgoingContent[clientId] if x is not None]
        
        
     
        return outgoingContent
        
    def packageContent(self, responseContent):
        responsePackets = {}
        for clientId in responseContent:
            content = responseContent[clientId]
            
            if len(content):
                responsePackets[clientId] = Packet(content)
                
        return responsePackets
           
class ClientState(GameState):

    def __init__(self, game):
        GameState.__init__(self, game)
        

    def handlePackets(self, packets):
        "Handle incoming Server Packets, returns a list of content to reply with"
        outgoingContent = []
        
        def dispatchHandler(content):
            key = content.__class__.__name__
            if  self.handlers.has_key(key):
                return self.handlers[key](content)
            else:
                raise ContentNotHandledException("No content handler for " + key)
        

        for packet in packets:
            content = packet.content
            
            for el in content:
                responseContent = dispatchHandler(el)
                if isinstance(responseContent, list):
                    outgoingContent += responseContent
                elif responseContent is not None:
                    outgoingContent.append(responseContent)

        
        
        return [x  for x in outgoingContent if x is not None]
        
    def packageContent(self, responseContent):
        if len(responseContent):
            return Packet(responseContent)
                
        return None
        