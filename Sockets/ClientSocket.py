'''
Created on Aug 15, 2016

@author: Philip Wardlaw
'''
from GameSocket import GameSocket

class ClientSocket(GameSocket):
    '''
    classdocs
    '''

    def __init__(self):
        GameSocket.__init__(self)
        
    def connect(self, address, port):
        self.socket.connect((address, port))


    def request(self, msg):
        self._send(self.socket, msg)
        return self._receive(self.socket)
    
    def disconnect(self):
        self.socket.close()
        