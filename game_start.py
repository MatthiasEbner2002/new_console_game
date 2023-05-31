import logging
import curses
import atexit

# My file import
from classes.Game_Level_1 import Game_Level_1
from classes.Color_util import Color_util

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
    curses.noecho()
    curses.initscr()
    curses.start_color()
    curses.use_default_colors()
    
    # init 255 colors 
    for i in range(0, 255):
        curses.init_pair(i + 1, i, -1)
    Color_util.init_colors()
        
    curses.curs_set(0)
    
    atexit.register(exit_handler)
    
    add_logging()
    log_start()
    
    
    game_level_1: Game_Level_1 = Game_Level_1(screen)
    game_level_1.run()

    

if __name__ == '__main__':
    curses.wrapper(main)
