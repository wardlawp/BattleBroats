from observer import Observer
from BattleBroats import Game, Board, Tile
import string
import BattleBroats
from BattleBroats import constants as gc

class ClientTextUI(Observer):
    
    TILE_TRANSLATION = {Tile.WATER: ' ', Tile.BROAT: 'B', 
                        Tile.SHOT: 'X', Tile.DEAD_BROAT: 'D'}
    
    def __init__(self, game):
        assert isinstance(game, Game)
        Observer.__init__(self, game)
        self.__requireRedraw = False
        
        self.__columnChars = list(string.ascii_uppercase)
        

    def recieveEvent(self, event):
        if event == gc.EVENT_BOARD_CHANGED:
            self.__requireRedraw = True
            
    def draw(self):
        if self.__requireRedraw:
            
            print '=============== Your Board ================'
            self.__drawBoard(self.subject.boards[gc.CLIENT_SELF])
            print '=============== Their Board ==============='
            self.__drawBoard(self.subject.boards[gc.CLIENT_OTHER])
            print '==========================================='
            print 'Waiting for other player...'
            
            
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
        

    def getRowFromUser(self):
        row = None
        while row is None:
            row = raw_input('Enter Row [1-N]:')
            if self.__canParseInt(row):
                row = int(row)
                maxRow = self.subject.boards[gc.CLIENT_SELF].nRows() - 1
                if row < 0 or row > maxRow:
                    print "Row must be between 0 and " + str(maxRow)
                    row = None
            else:
                print "Row must be a number"
                row = None
        
        return row
    
    def getColFromUser(self):
        colInput = None
        while colInput is None:
            colInput = raw_input('Enter Column [A-Z]')
            
            
            if  len(colInput) == 1:
                maxCol = self.subject.boards[gc.CLIENT_SELF].nCols() 
                acceptableChars = string.ascii_uppercase[:maxCol]
                if colInput[0] not in acceptableChars:
                    print "Column must be in {" + ','.join(acceptableChars) + '}'
                    colInput = None
            else:
                print "Column must be a single letter"
                colInput = None
                
            
        return string.ascii_uppercase.index(colInput[0])

    def input(self):
        if isinstance(self.subject.state, BattleBroats.GameState.ClientPlayState):
            if self.subject.state.myGo:
                print "It's your go!"
                
                row = self.getRowFromUser()
                col = self.getColFromUser()

                return [row, col]
            
            
    def __canParseInt(self, _input):
        try:
            int(_input)
            return True
        except:
            return False
        
        