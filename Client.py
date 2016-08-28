'''
Created on Aug 15, 2016

@author: Philip Wardlaw
'''


from Sockets import ClientSocket
from BattleBroats import Game
from pygame.time import Clock
from log import printCommunication
from UI import ClientTextUI

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
CLIENT_TICK = 5
DEBUG = False



if __name__ == '__main__':

    print 'Setting up game'
    game = Game(Game.MODE_CLIENT)
    sock = ClientSocket()
    tickClock = Clock()
    ui = ClientTextUI(game)
    
    print 'Connecting to Server'
    
    sock.connect(TCP_IP, TCP_PORT)
    
    request = None
    response = None
    userInput = None
    
    while game.inProgress():
       
        if request:
            response = sock.sendRequest(request)
        else:
            response = None
            
        request  = game.update(response, userInput)
        
        if DEBUG:
            printCommunication([request], [response])
        
        ui.draw()
        userInput = ui.input()
        
        
        tickClock.tick(CLIENT_TICK)

    
