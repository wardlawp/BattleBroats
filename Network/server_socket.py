'''
Created on Aug 15, 2016

@author: Philip Wardlaw
'''
from game_socket import GameSocket, ConnectionEndedException
import select


class ServerSocket(GameSocket):
    "A ServerSocket Accepts connections and can send/receive packets"
   

    def __init__(self, numConnections, ip, port):
        "Create a ServerSocjet that listens for connections on a ip:port"
        GameSocket.__init__(self)

        self.socket.bind((ip, port))
        self.socket.listen(numConnections)
        self.__cons = {}

   
    def acceptConnection(self):
        "Accept available connections async"
        newConnectionIds = []

        inputs = [self.socket]
        incoming, w, e = select.select(inputs, [], inputs, 0.0)

        for i in incoming:
            if i == self.socket:
                conn, ip = i.accept()
                
                newConnectionIds.append(ip)
                self.__cons[ip] = conn
        
        return newConnectionIds
    
    def sendManyPackets(self, packetDict):
        "Send a Packet to each connection"
        for  connId in packetDict:
            
            packet = packetDict[connId]
            conn = self.conn(connId)
            
            self.sendPacket(packet, conn)
    
    def connIds(self):
        "Get a list of connection Tuples (Ip, Port)"
        return self.__cons.keys()

    def conn(self, connectionId):
        "Get a connection object corresponding ot a connection id"
        return self.__cons[connectionId]
    
    def numConnections(self):
        return len(self.__cons)
    
    def poll(self):
        "Poll for incoming Packets and dropped connections"
        packets = {}
        droppedConnectionIds = []
        
        for ip in self.__cons:

            try:
                packets[ip] = self.receivePackets(self.__cons[ip])
        
            except ConnectionEndedException:
                droppedConnectionIds.append(ip)
        
        
        for conId in droppedConnectionIds:
            self.conn(conId).close()
            del self.__cons[conId]
        
        return droppedConnectionIds, packets
    
   

        
