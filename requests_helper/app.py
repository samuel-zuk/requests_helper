import sys

from requests_helper.common.curses_app import CursesApp
from requests_helper.common.window import Window

class RequestsHelperApp(CursesApp):
    def __init__(self):
        super().__init__()

        self.windows = {}
        self.windows['main'] = Window(50, 10, 0, 0)
        self.windows['secondary'] = Window(30, 8, 52, 1)
        self.windows['third'] = Window(30, 4, 0, 11)
        self.current_window = 'secondary'

        for x in self.windows.values():
            x.update()

    def main(self):
        new_active_win = None
        for x in self.windows.keys():
            self.windows[x].update()
            if x == self.current_window:
                ch = self.windows[x].getkey()
                self.windows[x].handle_move(ch)
                if ch == 'q':
                    sys.exit(0)
                elif ch == '1':
                    new_active_win = 'main' 
                elif ch == '2':
                    new_active_win = 'secondary' 
                elif ch == '3':
                    new_active_win = 'third' 
        if new_active_win:
            self.current_window = new_active_win
