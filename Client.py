'''
Created on Aug 15, 2016

@author: Philip Wardlaw
'''


from Sockets import ClientSocket

TCP_IP = '127.0.0.1'
TCP_PORT = 5005

if __name__ == '__main__':

    sock = ClientSocket()
    
    sock.connect(TCP_IP, TCP_PORT)
    
    print sock.request('testing')
    print sock.request('123')
    
