import logging, math, curses

from classes.Size import Size

"""
Methods to draw borders and other things on the screen.
interacts with the console and adds char and strings to the screen.
"""

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
        logging.warning("Screen is not set")
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
        logging.warning("Screen is not set")
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
        logging.warning("Screen is not set")
        return
    
    x_start, y_start, x, y = size.calculate_playfield()
    border_color_pair = curses.color_pair(3)
    
    for i in range(x_start, x_start + x):
        screen.addch(i, y_start, curses.ACS_VLINE | curses.A_BOLD, border_color_pair)  # Left border line
        screen.addch(i, y_start + y, curses.ACS_VLINE | curses.A_BOLD, border_color_pair)  # Right border line
        
    for i in range(y_start, y_start +  y):
        screen.addch(x_start, i, curses.ACS_HLINE | curses.A_BOLD, border_color_pair)  # Top border line
        screen.addch(x_start + x, i, curses.ACS_HLINE | curses.A_BOLD, border_color_pair)  # Bottom border line
        
    screen.addch(x_start, y_start, curses.ACS_ULCORNER | curses.A_BOLD, border_color_pair)  # Upper left corner
    screen.addch(x_start, y_start + y, curses.ACS_URCORNER | curses.A_BOLD, border_color_pair)  # Upper right corner
    screen.addch(x_start + x, y_start, curses.ACS_LLCORNER | curses.A_BOLD, border_color_pair)  # Lower left corner
    screen.addch(x_start + x, y_start + y, curses.ACS_LRCORNER | curses.A_BOLD, border_color_pair)  # Lower right corner
    
    return  x_start, y_start, x, y  # Return the playfield borders for further use

    
def add_arrow_to_playfield(screen: curses.window, playfield_size_original, playfield, step):
    """
    Adds the arrow to the playfield. The arrow is the current step of the user. The arrow is a char and has a color. 

    Args:
        screen (curses.window): The screen to draw on
        playfield_size_original (_type_): The playfield in its orginal size, the size where its getting calculated from 
        playfield (_type_): the playfield, where the arrow is getting drawn on, the playfield_size_original is getting drawn in this field on the screen 
        step (_type_): The current step of the user, the arrow is getting drawn on this position
    """
    
    arrow_color_pair = curses.color_pair(161)
    x_arrow = step[0]
    y_arrow = step[1]
    arrow_position = (x_arrow, y_arrow)
    x_arrow_in_playfield, y_arrow_in_playfield = get_screen_position_from_playfield_position(playfield_size_original, playfield, arrow_position) # Get the screen position of the arrow
    
    screen.addch(x_arrow_in_playfield, y_arrow_in_playfield, step[3], arrow_color_pair)
    

def add_angle_to_playfield(screen: curses.window, size: Size, angle: int):
    """
    Adds the angle to the playfield. The angle is a line, representing the angle of the arrow. Under the angle is the angle value.

    Args:
        screen (curses.window): The screen to draw on
        size (Size): the size of the screen and its positions of playfield and menu
        angle (int): the angle of the arrow, the angle is getting drawn on this position
    """
    
    angle_x_middle = size.get_x_for_angle()
    angle_y_middle = size.get_y_for_angle()

    # Calculate the end coordinates based on the angle
    angle = 360 - angle  # Rotate the angle 180 degrees      
    angle_in_radians = math.radians(angle)
    radius_x = 7 # y radius  
    radius_y = 4 # x radius
    
    # copyed from internet
    end_x = int(angle_y_middle + math.cos(angle_in_radians) * radius_x)
    end_y = int(angle_x_middle + math.sin(angle_in_radians) * radius_y)

    # Draw the line
    draw_line(screen, angle_y_middle, angle_x_middle, end_x, end_y, abs(angle - 360))  # Draw a line between the two points
    screen.addch(angle_x_middle, angle_y_middle, 'o')  # Mark the middle point with 'O'
    screen.addch(end_y, end_x, get_arrow_direction(abs(angle - 360)))  # Draw the line to the end point with 'X'

    # Calculate the angle value
    angle_text = f"Angle: {abs(angle - 360)}°"

    # Write the angle text
    screen.addstr(angle_x_middle + 4, 11, angle_text)  # Adjusted the position for clarity


def add_power_to_playfield(screen: curses.window, size: Size, value: int, maximum: int):
    """
    Adds the power to the playfield. The power is a progress bar, representing the power of the arrow. At the left of the power is the power value.

    Args:
        screen (curses.window): The screen to draw on
        size (Size): the size of the screen and its positions of playfield and menu
        value (int): The current power of the arrow, the power is getting drawn on this position
        maximum (int): The maximum power of the arrow.
    """

    x = size.get_x_for_progress_bar()
    y = size.get_y_for_progress_bar()
    progress = value * 100 // maximum
    filled_length = value * 20 // maximum
    empty_length = 20 - filled_length
    screen.addstr(x, y, str(value) + (" ","")[value >= 10] + "p [" + "=" * filled_length + " " * empty_length + "]")


def draw_line(screen: curses.window, x1: int, y1: int, x2: int, y2: int, angle: int):
    """
    Bresenham's line algorithm. copyed from internet


    Args:
        screen (curses.window): The screen to draw on.
        x1 (int): The x coordinate of the starting point.
        y1 (int): The y coordinate of the starting point.
        x2 (int): The x coordinate of the end point.
        y2 (int): The y coordinate of the end point.
        angle (int): The angle of the line.
    """
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        screen.addch(y1, x1, get_arrow_line(angle))

        if x1 == x2 and y1 == y2:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy


def get_arrow_line(angle: int):
    """
    returns the line of the arrow, based on the angle

    Args:
        angle (int): the angle, that needs to be drawn

    Returns:
        string: the line of the arrow to use, based on the angle
    """
    
    normalized_angle = angle % 360
    index = round(normalized_angle / 45) % 8
    arrows = ['─', '/', '|', '\\', '─', '/', '|', '\\']
    return arrows[index]
    
    
def get_arrow_direction(angle: int):
    """
    returns the direction of the arrow, based on the angle

    Args:
        angle (int): the angle, that needs to be drawn

    Returns:
        string : Arrow pointing in the direction of the angle
    """
    
    normalized_angle = angle % 360
    index = round(normalized_angle / 45) % 8
    arrows = ['→','↗', '↑', '↖', '←', '↙', '↓', '↘']
    return arrows[index]

    
def add_arrow_start_to_playfield(screen: curses.window, playfield_size_original, playfield,  start_position):
    """
    Adds the start of the arrow to the playfield. The start is a bullet, representing the start of the arrow.

    Args:
        screen (curses.window): The screen to draw on
        playfield_size_original (_type_): The size of the original playfield, before it got drawn on the screen
        playfield (_type_): The playfield, the space  on the screen, where the playfield is getting drawn
        start_position (_type_): The position of the start of the arrow
    """
    
    arrow_color_pair = curses.color_pair(161)
    start_char = curses.ACS_BULLET | curses.A_BOLD

    x_arrow_in_playfield, y_arrow_in_playfield = get_screen_position_from_playfield_position(playfield_size_original, playfield, (start_position[1], start_position[0])) # Get the screen position of the arrow
    screen.addch(x_arrow_in_playfield, y_arrow_in_playfield, start_char, arrow_color_pair)
    
    
def get_screen_position_from_playfield_position(playfield_size_original, playfield, position):
    """
    Converts a position in the playfield to a position on the screen

    Args:
        playfield_size_original (_type_): The size of the original playfield, before it got drawn on the screen
        playfield (_type_): the playfield, the space  on the screen, where the playfield is getting drawn
        position (_type_): the position to be converted

    Returns:
        _type_: the position on the screen
    """
    x = position[0]
    y = position[1]
    
    x_in_playfield = (x / playfield_size_original[0]) * playfield[2]
    y_in_playfield = (y / playfield_size_original[1]) * playfield[3]
    
    x_start, y_start, x, y = playfield
    
    return (x_start + x - int(x_in_playfield), y_start + int(y_in_playfield))