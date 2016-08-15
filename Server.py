'''
Created on Aug 15, 2016

@author: Philip Wardlaw
'''
from Sockets import ServerSocket


TCP_IP = '127.0.0.1'
TCP_PORT = 5005


if __name__ == '__main__':
    # Accept two connections
    #     On connect do Client negotiation (get name, tell wait)
    #     Ignore first Client and wait for second
    
    # Two connects? Start game
    #    Send Clients game start and maps
    #    Wait for client commands, respond to commands
    #    When games state is appropriate, update clients
    #    Client drops? End game
    
    
    s = ServerSocket(2, TCP_IP, TCP_PORT)
    
    print 'Starting polling'
    while True:

        newConnections = s.acceptConnection()
        
        if newConnections:
            print 'New Connections', newConnections

        droppedConnections, msgs = s.poll()
        
        
        if droppedConnections:
            print  'Dropped Connections', droppedConnections
        
        if msgs:
            for key in msgs:
                print 'Received: ' +  msgs[key]
                s._send(s.conn(key), 'OK')
    

