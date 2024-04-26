"""
This module is the starting point of the game.
It configures logging, sets up the game screen, and runs the game loop.
"""

import logging
import curses
import atexit

# My file import
from classes.Game_Level_1 import Game_Level_1
from classes.util.Color_util import Color_util


def configure_logging():
    """Configure logging settings."""
    format1 = '%(asctime)s %(levelname)s [%(filename)s - %(funcName)s(): %(lineno)s]: %(message)s'
    # format2 = '%(asctime)s | %(name)s | %(levelname)s %(message)s'

    logging.basicConfig(filename='log.log',
                        filemode='a',
                        format=format1,
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)


def log_starting_text():
    """Log the start of the game."""
    logging.info('''
    =====================================
              G A M E   S T A R T
    =====================================

              Welcome to Your Game!

     Get ready for an exciting adventure!

    =====================================
    ''')


def exit_handler():
    """Exit handler for curses."""
    curses.flushinp()
    logging.info('Exit program')


def main(screen):
    """Main function to run the game."""
    curses.noecho()  # disable automatic echoing of keys to the screen
    # initialize the library, return a window object representing the whole screen
    curses.initscr()

    Color_util.init_colors()  # init colors, color pairs, and set default colors

    # set cursor state. 0: invisible, 1: normal, 2: very visible
    curses.curs_set(0)

    atexit.register(exit_handler)  # register exit handler

    configure_logging()  # add logging
    log_starting_text()  # log start

    game_level_1: Game_Level_1 = Game_Level_1(screen)
    game_level_1.run()


if __name__ == '__main__':
    curses.wrapper(main)
