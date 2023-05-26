import logging
import curses

from classes.Size import Size

def draw_borders(screen: curses.window, size: Size):
    """
    Draws the borders of the screen. If screen is None, logs warning.
    

    Args:
        screen (): screen (curses)
        size (Size): Size of the screen
    """
    
    y = size.get_y_for_border()
    x = size.get_x_for_border()
    if screen is None:
        logging.warning("Size.py | draw_border(): Screen is not set")
        return

    # Draw horizontal lines
    for i in range(y):
        screen.addch(0, i, curses.ACS_HLINE)  # Top border line
        screen.addch(x, i, curses.ACS_HLINE)  # Bottom border line
        screen.addch(x - size.menu_x_size, i, curses.ACS_HLINE)  # Menu line

    # Draw vertical lines
    for i in range(x):
        screen.addch(i, 0, curses.ACS_VLINE)  # Left border line
        screen.addch(i, y, curses.ACS_VLINE)  # Right border line

    # Draw corner characters
    screen.addch(0, 0, curses.ACS_ULCORNER)  # Upper left corner
    screen.addch(0, y, curses.ACS_URCORNER)  # Upper right corner
    screen.addch(x, 0, curses.ACS_LLCORNER)  # Lower left corner
    screen.addch(x - 1, y, curses.ACS_LRCORNER)  # Lower right corner
    screen.addch(x - size.menu_x_size, 0, curses.ACS_LTEE)  # Menu line left corner
    screen.addch(x - size.menu_x_size, y, curses.ACS_RTEE)  # Menu line right corner


def add_user_platform(screen: curses.window, size: Size):
    """
    Adds the user platform to the screen.

    Args:
        screen (_type_): _description_
        size (Size): _description_
    """
    
    if screen is None:
        logging.warning("Size.py | add_user_platform(): Screen is not set")
        return

    x = size.get_x()
    y = size.get_y_start()
    screen.addstr(x, y, "######")
    
    
def draw_playfield_borders(screen: curses.window, size:Size):
    """
    Draws the borders of the playfield.

    Args:
        screen (_type_): _description_
        size (Size): _description_
    """
    
    if screen is None:
        logging.warning("Size.py | draw_playfield_borders(): Screen is not set")
        return
    
    x_start, y_start, x, y = size.calculate_playfield()
    
    for i in range(x_start, x_start + x):
        screen.addch(i, y_start, curses.ACS_VLINE | curses.A_BOLD)  # Left border line
        screen.addch(i, y_start + y, curses.ACS_VLINE | curses.A_BOLD)  # Right border line
        
    for i in range(y_start, y_start +  y):
        screen.addch(x_start, i, curses.ACS_HLINE | curses.A_BOLD)  # Top border line
        screen.addch(x_start + x, i, curses.ACS_HLINE | curses.A_BOLD)  # Bottom border line
        
    screen.addch(x_start, y_start, curses.ACS_ULCORNER | curses.A_BOLD)  # Upper left corner
    screen.addch(x_start, y_start + y, curses.ACS_URCORNER | curses.A_BOLD)  # Upper right corner
    screen.addch(x_start + x, y_start, curses.ACS_LLCORNER | curses.A_BOLD)  # Lower left corner
    screen.addch(x_start + x, y_start + y, curses.ACS_LRCORNER | curses.A_BOLD)  # Lower right corner