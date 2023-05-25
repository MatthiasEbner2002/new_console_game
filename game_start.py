import logging
import curses
import time

# My file import
from classes.Size import Size

def add_logging():
    logging.basicConfig(filename='log.log',
                        filemode='a',
                        format='%(asctime)s | %(name)s | %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

def main(screen):
    curses.noecho()
    curses.initscr()
    curses.start_color()
    curses.use_default_colors()
    
    # init 255 colors 
    for i in range(0, 255):
        curses.init_pair(i + 1, i, -1)
        
    curses.curs_set(0)
       
    add_logging()
    
    size: Size = Size.from_terminal_size(screen=screen)

    while True:
        size.update_terminal_size_with_logging_and_screen_refresh()
        time.sleep(1)

if __name__ == '__main__':
    curses.wrapper(main)

