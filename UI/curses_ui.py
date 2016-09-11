from observer import Observer
from BattleBroats import Game, Board, Tile
import string
import BattleBroats
from BattleBroats import constants as gc

import curses

class CursesUI(Observer):

    def __init__(self, game):
        assert isinstance(game, Game)
        Observer.__init__(self, game)
        # Initialize the curses screen
        self.stdscr = curses.initscr()
        self.stdscr.keypad(True)
        self.stdscr.nodelay(True)
        curses.noecho()
        curses.cbreak()
        curses.curs_set(False)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_YELLOW)
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)

        self.selected_col = 0
        self.selected_row = 0

    def __del__(self):
        self.stdscr.keypad(False)
        curses.curs_set(True)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def recieveEvent(self, event):
        if event == gc.EVENT_BOARD_CHANGED:
            self.__requireRedraw = True

    def draw(self):
        if gc.CLIENT_SELF in self.subject.boards:

            self.stdscr.addstr(0, 0, "Your Board:")
            self.__drawBoard(self.subject.boards[gc.CLIENT_SELF], 1, 0, False)
            offsetx = 2*self.subject.boards[gc.CLIENT_SELF].nCols()+1
            self.stdscr.addstr(0, offsetx, "Their Board:")
            self.__drawBoard(self.subject.boards[gc.CLIENT_OTHER], 1, offsetx, True)

            offsety = self.subject.boards[gc.CLIENT_SELF].nRows()+1
            if self.ismyturn():
                self.stdscr.addstr(offsety, 0, "It is your turn! ")
            else:
                self.stdscr.addstr(offsety, 0, "It is their turn!")
            self.stdscr.refresh()

    def __drawBoard(self, board, offsety, offsetx, show_selection):
        for y in range(board.nRows()):
            for x in range(board.nCols()):
                e = board.element(y,x)
                char = "  "
                if e == Tile.WATER:
                    style = 1
                elif e == Tile.BROAT:
                    style = 2
                elif e == Tile.SHOT:
                    style = 3
                elif e == Tile.DEAD_BROAT:
                    style = 4
                if show_selection and y == self.selected_row and x == self.selected_col:
                    char = "##"
                self.stdscr.addstr(y+offsety, x*2+offsetx, char,
                                   curses.color_pair(style))
    def input(self):

        c = self.stdscr.getch()
        if c == curses.KEY_RIGHT:
            self.selected_col += 1
        elif c == curses.KEY_LEFT:
            self.selected_col -= 1
        elif c == curses.KEY_UP:
            self.selected_row -= 1
        elif c == curses.KEY_DOWN:
            self.selected_row += 1
        elif self.ismyturn() and c == ord(' '):
            return [self.selected_row, self.selected_col]


    def ismyturn(self):
        return isinstance(self.subject.state, BattleBroats.GameState.ClientPlayState) and self.subject.state.myGo

    def __canParseInt(self, _input):
        try:
            int(_input)
            return True
        except:
            return False
