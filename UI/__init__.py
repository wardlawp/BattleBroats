import sys

from client_text_ui import ClientTextUI
if sys.platform in ("linux", "linux2","darwin"):
    from curses_ui import CursesUI
