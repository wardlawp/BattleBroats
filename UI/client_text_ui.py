from observer import Observer
from BattleBroats import Game, Board, Tile
import string
import BattleBroats


class ClientTextUI(Observer):
    
    TILE_TRANSLATION = {Tile.WATER: ' ', Tile.BROAT: 'B', 
                        Tile.SHOT: 'X', Tile.DEAD_BROAT: 'D'}
    
    def __init__(self, game):
        assert isinstance(game, Game)
        Observer.__init__(self, game)
        self.__requireRedraw = False
        
        self.__columnChars = list(string.ascii_uppercase)
        

    def recieveEvent(self, event):
        if event == Game.EVENT_BOARD_CHANGED:
            self.__requireRedraw = True
            
    def draw(self):
        if self.__requireRedraw:
            
            print '============ Your Board ============'
            self.__drawBoard(self.subject.boards[Game.CLIENT_SELF])
            print '============ Their Board ==========='
            self.__drawBoard(self.subject.boards[Game.CLIENT_OTHER])
            print '===================================='
            
            
            self.__requireRedraw = False
        
        
    def __drawBoard(self, board):
        assert isinstance(board, Board)
        
        template =   '  {0}  |'
        br =         '------'
        headerRow = ['     |']
        for y in range(board.nCols()):
            headerRow.append(template.format(self.__columnChars[y]))
        
        print ''.join(headerRow)
        
        for x in range(board.nRows()):
            print br*(board.nCols() +1 )
            row = [template.format(x)]
            for y in range(board.nCols()):
                herp =board.element(x, y)
                _char = self.TILE_TRANSLATION[herp.type]
                row.append(str(template.format(_char)))
            
            print ''.join(row)
        
    def input(self):
        if isinstance(self.subject.state, BattleBroats.GameState.ClientPlayState):
            if self.subject.state.ourGo:
                move = input('?')
                return [move[0], move[1]]