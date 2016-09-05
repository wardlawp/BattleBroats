'''
Created on Aug 15, 2016

@author: Philip Wardlaw
'''


from Network import ClientSocket
from BattleBroats import Game, constants as gc
from pygame.time import Clock
from log import printCommunication
from UI import ClientTextUI

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
CLIENT_TICK = 5
DEBUG = False



if __name__ == '__main__':

    print 'Setting up game'
    game = Game(gc.MODE_CLIENT)
    sock = ClientSocket()
    tickClock = Clock()
    ui = ClientTextUI(game)
    
    print 'Connecting to Server'
    
    sock.connect(TCP_IP, TCP_PORT)
    

    userInput = None
    
    while game.inProgress():
        userInput = ui.input()
        packetsRecieved = sock.poll()
        packetToSend = game.update(packetsRecieved, userInput)
        
        if DEBUG:
            if packetsRecieved:
                print "Recieved"
                for p in packetsRecieved:
                    print p.content
            if packetToSend :
                print "To Send"
                print packetToSend.content
        
        if packetToSend:
            sock.sendPacket(packetToSend)

        
        
        ui.draw()
        
        
        tickClock.tick(CLIENT_TICK)
    print 'Game is over'

    
