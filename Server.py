'''
Created on Aug 15, 2016

@author: Philip Wardlaw
'''
from Sockets import ServerSocket
from BattleBroats import Game
from pygame.time import Clock
from log import printCommunication


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
SERVER_TICK = 5
DEBUG = False



if __name__ == '__main__':
    
    print 'Setting up game'
    
    game = Game(Game.MODE_SERVER)
    sock = ServerSocket( game.MAX_PLAYERS, TCP_IP, TCP_PORT)
    tickClock = Clock()
    
    print 'Waiting for players'
    
    while game.inProgress():
        
        if sock.numConnections() < game.MAX_PLAYERS:
            newConnections = sock.acceptConnection()
            if newConnections:
                print 'New Connection(s):', newConnections

        droppedConnections, requestsDict = sock.poll()
        responsesDict = game.update(requestsDict, None)
        
        sock.sendManyResponses(responsesDict)

        if DEBUG:
            printCommunication(requestsDict, responsesDict)
        
        if droppedConnections:
            print 'Dropped Connections', droppedConnections
            print 'Exiting'
            exit(1)
        
        
        tickClock.tick(SERVER_TICK)
