'''
Created on Aug 15, 2016

@author: Philip Wardlaw
'''
import socket
from Protocol import Request, Response

class ConnectionEndedException(Exception):
    
    def __init__(self, msg):
        Exception.__init__(self, msg)

class GameSocket(object):
    """
    Base Socket class for connecting, sending Requests and receiving Responses
    
    """
    DELIM = '%'
    CHNK_SIZE = 4096

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def connect(self, host, port):
        self.socket.connect((host, port))
        
    def sendRequest(self, conn, request):
        assert isinstance(request, Request)
        self.__sendString(conn, request.serialize())
        return Response.deserialize(self.__receive(conn))
    
    def sendResponse(self, conn, response):
        assert isinstance(response, Response)
        self.__sendString(conn, response.serialize())

    def recieveRequest(self, conn):
        msg = self.__receive(conn) 
        return Request.deserialize(msg)
    
    def __sendString(self, conn, msg):

        assert isinstance(msg, str), 'msg must be string'

        msg += self.DELIM
        totalsent = 0
        while totalsent < len(msg):
            sent = conn.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    

    def __receive(self, conn):
        chunks = []

        while 1:
            chunk = self.__getChunk(conn, self.CHNK_SIZE)
            chunks.append(chunk)
            if self.DELIM in chunk:
                break

        lastChunk = chunks[-1]
        chunks[-1] = lastChunk[:lastChunk.find(self.DELIM)]

        return ''.join(chunks)

    def __getChunk(self, conn, chunkSize):
        chunk = conn.recv(chunkSize)

        if not chunk :
            raise ConnectionEndedException("Connection has closed")

        return chunk

