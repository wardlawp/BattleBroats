'''
Created on Aug 15, 2016

@author: Philip Wardlaw
'''
from GameSocket import GameSocket, ConnectionEndedException
import select
import socket
import errno
from Protocol import Request

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
        incoming, w, e = select.select(inputs, [], inputs, self.TIMEOUT)

        for i in incoming:
            if i == self.socket:
                conn, ip = i.accept()
                
                newConnectionIds.append(ip)
                self.__cons[ip] = conn
        
        return newConnectionIds
    
            
    def sendManyResponses(self, responseDict):
        for id in responseDict:
            self.sendResponse(self.conn(id), responseDict[id])
    
    def connIds(self):
        return self.__cons.keys()

    def conn(self, connectionId):
        return self.__cons[connectionId]
    
    def numConnections(self):
        return len(self.__cons)
    
    def poll(self):
        requests = {}
        droppedConnectionIds = []
        
        for ip in self.__cons:
            conn = self.__cons[ip]

            try:
                requests[ip] = self.recieveRequest(conn)
            except socket.error, e:
                if not self.__asynResponse(e):
                    raise e
               
            except ConnectionEndedException, ce:
                droppedConnectionIds.append(ip)
        
        
        for conId in droppedConnectionIds:
            self.conn(conId).close()
            del self.__cons[conId]

        
        return droppedConnectionIds, requests
    
    def __asynResponse(self, e):
        err = e.args[0]
        return err == errno.EAGAIN or err == errno.EWOULDBLOCK

        