from observer import Observer
from BattleBroats import Game

class ClientTextUI(Observer):
    
    def __init__(self, game):
        assert isinstance(game, Game)
        Observer.__init__(self, game)
        self.__requireRedraw = False
        

    def recieveEvent(self, event):
        if event == Game.EVENT_BOARD_CHANGED:
            self.__requireRedraw = True
            
    def draw(self):
        if self.__requireRedraw:
            print self.subject.boards['self']
            print self.subject.boards['other']
            
            self.__requireRedraw = False
        
    def input(self):
        return 