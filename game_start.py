import logging
import curses
import time
import atexit

# My file import
from classes.Game_Level_1 import Game_Level_1

def add_logging():
    logging.basicConfig(filename='log.log',
                        filemode='a',
                        format='%(asctime)s | %(name)s | %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    
def exit_handler():
    """
    Exit handler for curses
    flushinp() - flush all input buffers
    """
    curses.flushinp() 
    logging.info('Exit program')


def main(screen):
    curses.noecho()
    curses.initscr()
    curses.start_color()
    curses.use_default_colors()
    
    # init 255 colors 
    for i in range(0, 255):
        curses.init_pair(i + 1, i, -1)
        
    curses.curs_set(0)
    
    atexit.register(exit_handler)
    
    add_logging()
    
    game_level_1: Game_Level_1 = Game_Level_1(screen)
    
    game_level_1.run()

    

if __name__ == '__main__':
    curses.wrapper(main)
