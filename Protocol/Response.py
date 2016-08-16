'''
Created on Aug 16, 2016

@author: Philip Wardlaw
'''
from Packet import Packet

class Response(Packet):
    '''
    classdocs
    '''
    STATUS_OK=1
    STATUS_NOT_OK=2
    STATUS_ERROR=3
    STATUSES = [STATUS_OK, STATUS_NOT_OK, STATUS_ERROR]


    def __init__(self, status, contentType, content):
        "Responses do not necessarily have content"
        if contentType is not None:
            Packet.__init__(self,  status, contentType, content)
        else:
            self.status = status
            self.contentType, self.content = None
    
    def statuses(self):
        return self.STATUSES