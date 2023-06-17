import logging
import curses
import atexit

# My file import
from classes.Game_Level_1 import Game_Level_1
from classes.util.Color_util import Color_util

def add_logging():
    format1 = '%(asctime)s %(levelname)s [%(filename)s - %(funcName)s(): %(lineno)s]: %(message)s'
    format2 = '%(asctime)s | %(name)s | %(levelname)s %(message)s'
    logging.basicConfig(filename='log.log',
                        filemode='a',
                        format=format1,
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    
def log_start():
    logging.info('''
    =====================================
              G A M E   S T A R T
    =====================================
    
              Welcome to Your Game!
    
     Get ready for an exciting adventure!
    
    =====================================
    ''')

    
def exit_handler():
    """
    Exit handler for curses
    flushinp() - flush all input buffers
    """
    
    curses.flushinp() 
    logging.info('Exit program')


def main(screen):
    curses.noecho()                 # disable automatic echoing of keys to the screen
    curses.initscr()                # initialize the library, return a window object representing the whole screen
    
    Color_util.init_colors()        # init colors, color pairs, and set default colors
    
    curses.curs_set(0)              # set cursor state. 0: invisible, 1: normal, 2: very visible
    
    atexit.register(exit_handler)   # register exit handler
    
    add_logging()                   # add logging
    log_start()                     # log start
    
    
    game_level_1: Game_Level_1 = Game_Level_1(screen)
    game_level_1.run()

    

if __name__ == '__main__':
    curses.wrapper(main)
