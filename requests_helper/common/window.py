import curses


class WindowManager(object):
    def __init__(self):
        self.stdscr = curses.initscr()
        self.stdscr.keypad(True)

        self.windows = {}
        self.bounds = {
            'left': {},
            'right': {},
            'top': {},
            'bottom': {}
        }
        self.cur_id = 0

    def register_window(self, window):
        new_id = str(self.cur_id)
        self.cur_id += 1

        self.windows[new_id] = window
        b_top, b_left = window.getbegyx()
        b_bottom, b_right = map(sum, zip((b_top, b_left),
                                         window.getmaxyx()))

        for bound, value in (('left', b_left), ('right', b_right),
                             ('top', b_top), ('bottom', b_bottom)):
            self.bounds[bound][new_id] = value

        return new_id
    
    def unregister_window(self, win_id):
        self.windows.pop(win_id)
        for b in self.bounds.keys():
            self.bounds[b].pop(win_id)

    def __del__(self):
        self.stdscr.keypad(False)


class Window(object):
    manager = WindowManager()
    MV_UP = ('KEY_UP', 'k')
    MV_DOWN = ('KEY_DOWN', 'j')
    MV_LEFT = ('KEY_LEFT', 'h')
    MV_RIGHT = ('KEY_RIGHT', 'l')

    def __init__(self, width, height, x=None, y=None, border=True):
        if x is None and y is None:
            self._window = curses.newwin(height, width)
        elif not (x is None or y is None):
            self._window = curses.newwin(height, width, y, x)
        else:
            raise ValueError('%s position must be specified' %
                             ('x' if (y and not x) else 'y'))

        self._window.keypad(True)
        self._id = self.manager.register_window(self._window)

        self.x_max, self.y_max = (width, height)
        self.border = border

        self.subwins = []

    def __del__(self):
        self._window.keypad(False)
        self.manager.unregister_window(self._id)

    def update(self):
        if self.border:
            self._window.border()
        self._window.refresh()

    def handle_move(self, key):
        if key in self.MV_UP:
            self.move_up()
        elif key in self.MV_DOWN:
            self.move_down()
        elif key in self.MV_LEFT:
            self.move_left()
        elif key in self.MV_RIGHT:
            self.move_right()

    def move_up(self):
        y, x = self._window.getyx()
        if y > 0: 
            self._window.move(y - 1, x)

    def move_down(self):
        y, x = self._window.getyx()
        if y < self.y_max - 1:
            self._window.move(y + 1, x)

    def move_left(self):
        y, x = self._window.getyx()
        if x > 0:
            self._window.move(y, x - 1)

    def move_right(self):
        y, x = self._window.getyx()
        if x < self.x_max - 1:
            self._window.move(y, x + 1)

    def getkey(self):
        return self._window.getkey()
