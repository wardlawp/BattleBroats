'''
Created on Aug 15, 2016

@author: Philip Wardlaw
'''
import socket
from packet import Packet
import errno

class ConnectionEndedException(Exception):
    
    def __init__(self, msg):
        Exception.__init__(self, msg)

class GameSocket(object):
    "Base Socket class for sending and receiving messages"
    DELIM = '%'
    CHNK_SIZE = 4096

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Set Socket as non blocking so we can process connections async
        self.socket.setblocking(0)
        self.__msgOverflow = ''
        
    def receivePacket(self, conn):
        "Receive a single Packet Async, returns None if no Packets available"
        try:
            msg = self.__receiveString(conn) 
            return Packet.deserialize(msg)
            
        except socket.error, e:
            if not self.__isAsynResponse(e):
                raise e
            
        return None
    
    def receivePackets(self, conn):
        "Receive all pending Packet Async"
        packets = []
        while True:
            packet = self.receivePacket(conn)
            
            if packet is not None:
                packets.append(packet)
            else:
                break
            
        return packets
    
    def sendPacket(self, packet, conn):
        "Send a Packet to a connection"
        assert isinstance(packet, Packet)
        self.__sendString(conn, packet.serialize())


    def __isAsynResponse(self, e):
        err = e.args[0]
        return err == errno.EAGAIN or err == errno.EWOULDBLOCK

    def __sendString(self, conn, msg):
        "Send a string to a connection/socket"

        assert isinstance(msg, str), 'msg must be string'

        msg += self.DELIM
        totalsent = 0
        while totalsent < len(msg):
            sent = conn.send(msg[totalsent:])
            if sent == 0:
                raise ConnectionEndedException("Connection has closed")
            totalsent = totalsent + sent

    def __receiveString(self, conn):
        "Receive a string from a connection/socket"
        chunks = []

        while 1:
            chunk = self.__getChunk(conn, self.CHNK_SIZE)
            chunks.append(chunk)
            if self.DELIM in chunk:
                break

        lastChunk = chunks[-1]
        chunks[-1] = lastChunk[:lastChunk.find(self.DELIM)]

        msg = self.__msgOverflow.join(chunks)
        self.__msgOverflow = lastChunk[(lastChunk.find(self.DELIM) +1):]

        return msg
    
    def __getChunk(self, conn, chunkSize):
        chunk = conn.recv(chunkSize)

        if not chunk :
            raise ConnectionEndedException("Connection has closed")

        return chunk

