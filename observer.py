'''
Created on Aug 27, 2016

@author: Philip Wardlaw
'''
from abc import ABCMeta, abstractmethod
from subject import Subject

class Observer(object):
    __metaclass__ = ABCMeta
    
    def __init__(self, subject):
        assert isinstance(subject, Subject)
        subject.registerObserver(self)
        self.subject = subject
        
    def unregister(self):
        self.subject.unregisterObserver(self)
    
    
    @abstractmethod
    def recieveEvent(self, event):
        return
    