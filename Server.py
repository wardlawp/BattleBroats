'''
Created on Aug 15, 2016

@author: Philip Wardlaw
'''
from Sockets import ServerSocket


TCP_IP = '127.0.0.1'
TCP_PORT = 5005
NUM_PLAYERS = 1

if __name__ == '__main__':
    
    sock = ServerSocket(NUM_PLAYERS, TCP_IP, TCP_PORT)
    
    print 'Starting polling'
    while True:

        # Accept new Players
        while sock.numConnections() < NUM_PLAYERS:
            newConnections = sock.acceptConnection()
            if newConnections:
                print 'New Connection(s):', newConnections
                # Add players to game
                # Send OK response
                
        # Set up the game 
        #    Create game object
        #    Send Clients game start and maps
        
        # Play the game. game still going
        #    Wait for client commands, respond to commands
        #    When games state is appropriate, update clients
        #    Client drops? End game
        #    Throttle the server, 5 ticks per second
    

        droppedConnections, requests = sock.poll()
        
        
        if droppedConnections:
            print  'Dropped Connections', droppedConnections
        
        if requests:
            for clientId in requests:
                print 'Received from ' + str(clientId) + ' :' +  str(requests[clientId].content)
                sock._send(sock.conn(clientId), 'OK')
    

