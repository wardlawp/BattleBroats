'''
Created on Aug 15, 2016

@author: Philip Wardlaw
'''


class Client(object):
    '''
    classdocs
    '''

    def __init__(self, connection):
        '''
        Constructor
        '''
        self.conn = connection
        self.__welcome()
        
    def __welcome(self):
        "Perform client welcome negotiations"
        
