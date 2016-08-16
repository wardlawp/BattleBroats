'''
Created on Aug 15, 2016

@author: Philip Wardlaw
'''


from Sockets import ClientSocket
from BattleBroats import Board
from Protocol import Request

TCP_IP = '127.0.0.1'
TCP_PORT = 5005

if __name__ == '__main__':

    sock = ClientSocket()
    sock.connect(TCP_IP, TCP_PORT)
    
    board = Board(2,2)
    request = Request(Request.STATUS_OK, board)
    
    
    print sock.sendRequest(request)

    
