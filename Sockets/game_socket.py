'''
Created on Aug 15, 2016

@author: Philip Wardlaw
'''
import socket
from Protocol import Response
from Protocol import Request

class ConnectionEndedException(Exception):
    
    def __init__(self, msg):
        Exception.__init__(self, msg)

class GameSocket(object):
    "Base Socket class for sending and receiving messages"
    DELIM = '%'
    CHNK_SIZE = 4096

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def sendString(self, conn, msg):
        "Send a string to a connection/socket"

        assert isinstance(msg, str), 'msg must be string'

        msg += self.DELIM
        totalsent = 0
        while totalsent < len(msg):
            sent = conn.send(msg[totalsent:])
            if sent == 0:
                raise ConnectionEndedException("Connection has closed")
            totalsent = totalsent + sent

    

    def receiveString(self, conn):
        "Receive a string from a connection/socket"
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

