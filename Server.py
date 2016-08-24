'''
Created on Aug 15, 2016

@author: Philip Wardlaw
'''
from Sockets import ServerSocket
from BattleBroats import Game
from pygame.time import Clock


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
NUM_PLAYERS = 1
SERVER_TICK = 5
DEBUG = True

def printCommunication(requests, responses):
    
    def __print(preMsg, packetDict):
        for clientId in requests:
            
            msg = preMsg + str(clientId) + ': STATUS ' 
            + packetDict[clientId].status
            + ', CONTNET' + str(packetDict[clientId].content)
            
            print msg


if __name__ == '__main__':
    
    sock = ServerSocket(NUM_PLAYERS, TCP_IP, TCP_PORT)
    
    print 'Waiting for players polling'
    
    
    
    game = Game()
    tickClock = Clock()
    

    
    while game.inProgress():
        
        if sock.numConnections() < NUM_PLAYERS:
            newConnections = sock.acceptConnection()
            if newConnections:
                print 'New Connection(s):', newConnections

        droppedConnections, requestsDict = sock.poll()
        responsesDict = game.processRequest(requestsDict)
        
        sock.sendManyResponses(responsesDict)

        if DEBUG:
            printCommunication(requestsDict, responsesDict)
        
        if droppedConnections:
            print 'Dropped Connections', droppedConnections
            print 'Exiting'
            exit(1)
        
        
        tickClock.tick(SERVER_TICK)
