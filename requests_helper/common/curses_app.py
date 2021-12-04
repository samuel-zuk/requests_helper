import curses
import locale
import sys


class CursesApp(object):
    def __init__(self):
        # set encoding from default system encoding
        locale.setlocale(locale.LC_ALL, '')
        code = locale.getpreferredencoding()

        # initialize curses
        curses.noecho()
        curses.cbreak()
        try:
            curses.start_color()
        except:
            pass

    def __del__(self):
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def __call__(self):
        try:
            while 1:
                self.main()
        except:
            self.__del__()
            raise
        else:
            sys.exit(0)

    def main(self):
        raise NotImplementedError()
