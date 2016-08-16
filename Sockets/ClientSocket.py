'''
Created on Aug 15, 2016

@author: Philip Wardlaw
'''
from GameSocket import GameSocket
from Protocol import Request
class ClientSocket(GameSocket):
    '''
    classdocs
    '''

    def __init__(self):
        GameSocket.__init__(self)
        
    def connect(self, address, port):
        self.socket.connect((address, port))


    def sendRequest(self, request):
        assert isinstance(request, Request)
        self._send(self.socket, request.serialize())
        return self._receive(self.socket)
    
    def disconnect(self):
        self.socket.close()
        