'''
Created on Aug 15, 2016

@author: Philip Wardlaw
'''
from game_socket import GameSocket

class ClientSocket(GameSocket):
    "A ClientSocket connects to a ServerSocket and can send/receive packets"

    def __init__(self):
        GameSocket.__init__(self)
        
    def connect(self, address, port):
        self.socket.setblocking(1)
        self.socket.connect((address, port))
        self.socket.setblocking(0)

    def disconnect(self):
        self.socket.close()

    def poll(self):
        "Poll for incoming Packets"
        return self.receivePackets(self.socket)
    
    def sendPacket(self, packet):
        "Send a Packet to the server"
        GameSocket.sendPacket(self, packet, self.socket)