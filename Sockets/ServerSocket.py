'''
Created on Aug 15, 2016

@author: Philip Wardlaw
'''
from GameSocket import GameSocket, ConnectionEndedException
import select
import socket
import errno

class ServerSocket(GameSocket):
    '''
    classdocs
    '''
   
    TIMEOUT = 0.0


    def __init__(self, numConnections, ip, port):
        GameSocket.__init__(self)
        self.socket.setblocking(0)
        self.socket.bind((ip, port))
        self.socket.listen(numConnections)
        self.__cons = {}

    def acceptConnection(self):
        newConnectionIds = []

        inputs = [self.socket]
        incoming, writable, exceptional = select.select(inputs, [], inputs, self.TIMEOUT)

        for i in incoming:
            if i == self.socket:
                conn, ip = i.accept()
                
                newConnectionIds.append(ip)
                self.__cons[ip] = conn
        
        return newConnectionIds
    

    def conn(self, connectionId):
        return self.__cons[connectionId]
    
    def poll(self):
        msgs = {}
        droppedConnectionIds = []
        
        for ip in self.__cons:
            conn = self.__cons[ip]

            try:
                msgs[ip] = self._receive(conn)
            except socket.error, e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    pass
                else:
                    raise e
            except ConnectionEndedException, ce:
                droppedConnectionIds.append(ip)
        
        
        for conId in droppedConnectionIds:
            self.conn(conId).close()
            del self.__cons[conId]

        
        return droppedConnectionIds, msgs
            
        