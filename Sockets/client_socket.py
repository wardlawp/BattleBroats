'''
Created on Aug 15, 2016

@author: Philip Wardlaw
'''
from game_socket import GameSocket
class ClientSocket(GameSocket):
    '''
    classdocs
    '''

    def __init__(self):
        GameSocket.__init__(self)
        
    def connect(self, address, port):
        self.socket.connect((address, port))

    def sendRequest(self, request):
        "Send a request, receive the response"
        return GameSocket.sendRequest(self, self.socket, request)
    
    def sendResponse(self,  response):
        GameSocket.sendResponse(self, self.socket, response)      
    
    def disconnect(self):
        self.socket.close()
        