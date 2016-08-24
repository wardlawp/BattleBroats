'''
Created on Aug 15, 2016

@author: Philip Wardlaw
'''
from game_socket import GameSocket
from Protocol import Request, Response

class ClientSocket(GameSocket):
    "A ClientSocket connects to a ServerSocket and can make send Requests"

    def __init__(self):
        GameSocket.__init__(self)
        
    def connect(self, address, port):
        self.socket.connect((address, port))

    def disconnect(self):
        self.socket.close()

    def sendRequest(self, request):
        "Send a Request, wait and receive the Response"
        assert isinstance(request, Request)
        self.sendString(self.socket, request.serialize())
        msg = self.receiveString(self.socket)
        return Response.deserialize(msg)
     
    
   
        
