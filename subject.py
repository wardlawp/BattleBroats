'''
Created on Aug 27, 2016

@author: Philip Wardlaw
'''
from abc import ABCMeta, abstractmethod



class Subject(object):
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def emmit(self, event):
        return
    
    @abstractmethod
    def registerObserver(self):
        return
    
    @abstractmethod
    def unregisterObserver(self):
        return
    

    