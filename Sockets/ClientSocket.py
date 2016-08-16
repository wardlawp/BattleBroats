'''
Created on Aug 15, 2016

@author: Philip Wardlaw
'''
from GameSocket import GameSocket
from Protocol import Request, Response
class ClientSocket(GameSocket):
    '''
    classdocs
    '''

    def __init__(self):
        GameSocket.__init__(self)
        
    def connect(self, address, port):
        self.socket.connect((address, port))


    def sendRequest(self, request):
        return GameSocket.sendRequest(self, self.socket, request)
    
    def sendResponse(self,  response):
        GameSocket.sendResponse(self, self.socket, response)
      

    
    def disconnect(self):
        self.socket.close()
        