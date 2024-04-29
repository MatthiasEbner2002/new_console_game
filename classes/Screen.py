import logging
import math
import curses

from classes.Size import Size
from classes.util.Color_util import Color_util
from classes.Input import Input
from classes.ArrowTrajectory import ArrowTrajectory

"""
Methods to draw borders and other things on the screen.
interacts with the console and adds char and strings to the screen.
"""


def draw_borders(screen: curses.window, size: Size):
    """Draws the borders of the screen and info box borders."""

    if screen is None:
        logging.warning("Screen is not set")
        return

    # Get the size of the terminal
    height, width = screen.getmaxyx()

    box1 = screen.subwin(height, width, 0, 0)
    box1.box()

    # Draw horizontal lines
    for i in range(size.y):
        screen.addch(size.x - size.menu_x_size, i, curses.ACS_HLINE)  # Menu line

    # Menu line left corner
    screen.addch(size.x - size.menu_x_size, 0, curses.ACS_LTEE)
    # Menu line right corner
    screen.addch(size.x - size.menu_x_size, size.y, curses.ACS_RTEE)


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


def draw_playfield_borders(screen: curses.window, size: Size):
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
    border_color_pair = Color_util.PLAYFIELD_BORDER_COLOR

    for i in range(x_start, x_start + x):
        # Left border line
        screen.addch(i, y_start, '┃', border_color_pair)
        # Right border line
        screen.addch(i, y_start + y, '┃', border_color_pair)

    for i in range(y_start, y_start + y):
        # Top border line
        screen.addch(x_start, i, '━', border_color_pair)
        # Bottom border line
        screen.addch(x_start + x, i, '━', border_color_pair)

    if size.is_playfield_x_smaller_then_x_verhältnis():
        # Upper left corner
        screen.addch(x_start, y_start, '┏', border_color_pair)
        # Upper right corner
        screen.addch(x_start, y_start + y, '┓', border_color_pair)
        screen.addch(x_start + x, y_start, '┺',
                     border_color_pair)      # Lower left corner
        screen.addch(x_start + x, y_start + y, '┹',
                     border_color_pair)  # Lower right corner
    else:
        # Upper left corner
        screen.addch(x_start, y_start, '┢', border_color_pair)
        # Upper right corner
        screen.addch(x_start, y_start + y, "┪", border_color_pair)
        screen.addch(x_start + x, y_start, '┡',
                     border_color_pair)      # Lower left corner
        screen.addch(x_start + x, y_start + y, '┩',
                     border_color_pair)  # Lower right corner

    return x_start, y_start, x, y  # Return the playfield borders for further use


def add_arrow_to_playfield(screen: curses.window, playfield_size_original, playfield, step):
    """
    Adds the arrow to the playfield. The arrow is the current step of the user. The arrow is a char and has a color.

    Args:
        screen (curses.window): The screen to draw on
        playfield_size_original (_type_): The playfield in its orginal size,
            the size where its getting calculated from
        playfield (_type_): the playfield, where the arrow is getting drawn on,
            the playfield_size_original is getting drawn in this field on the screen
        step (_type_): The current step of the user, the arrow is getting drawn on this position
    """

    arrow_color_pair = Color_util.ARROW_COLOR  # Get the color of the arrow
    x_arrow = step[0]
    y_arrow = step[1]
    arrow_position = (x_arrow, y_arrow)
    x_arrow_in_playfield, y_arrow_in_playfield = get_screen_position_from_playfield_position(
        playfield_size_original, playfield, arrow_position)  # Get the screen position of the arrow

    screen.addch(x_arrow_in_playfield, y_arrow_in_playfield,
                 step[3], arrow_color_pair)


def add_angle_to_playfield(screen: curses.window, size: Size, angle: int):
    """
    Adds the angle to the playfield. The angle is a line, representing the angle of the arrow.
    Under the angle is the angle value.

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
    radius_x = 7  # y radius
    radius_y = 4  # x radius

    # copyed from internet
    end_x = int(angle_y_middle + math.cos(angle_in_radians) * radius_x)
    end_y = int(angle_x_middle + math.sin(angle_in_radians) * radius_y)

    # Draw the line
    draw_line(screen, angle_y_middle, angle_x_middle, end_x, end_y,
              abs(angle - 360))  # Draw a line between the two points
    # Mark the middle point with 'O'
    screen.addch(angle_x_middle, angle_y_middle, 'o')
    # Draw the line to the end point with 'X'
    screen.addch(end_y, end_x, get_arrow_direction(abs(angle - 360)))

    # Calculate the angle value
    angle_text = f"Angle: {abs(angle - 360)}°"

    # Write the angle text
    # Adjusted the position for clarity
    screen.addstr(angle_x_middle + 4, 11, angle_text)


def add_power_to_playfield(screen: curses.window, size: Size, value: int, maximum: int):
    """
    Adds the power to the playfield. The power is a progress bar, representing the power of the arrow.
    At the left of the power is the power value.

    Args:
        screen (curses.window): The screen to draw on
        size (Size): the size of the screen and its positions of playfield and menu
        value (int): The current power of the arrow, the power is getting drawn on this position
        maximum (int): The maximum power of the arrow.
    """

    x = size.get_x_for_progress_bar()
    y = size.get_y_for_progress_bar()
    # progress = value * 100 // maximum
    filled_length = value * 20 // maximum
    empty_length = 20 - filled_length
    screen.addstr(x, y, str(value) + (" ", "")
                  [value >= 10] + "p [" + "=" * filled_length + " " * empty_length + "]")


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
        screen.addch(y1, x1, get_line_to_draw_angel(angle))

        if x1 == x2 and y1 == y2:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy


def get_line_to_draw_angel(angle: int):
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
    arrows = ['→', '↗', '↑', '↖', '←', '↙', '↓', '↘']
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

    arrow_color_pair = Color_util.ARROW_START_COLOR
    # start_char = curses.ACS_BULLET | curses.A_BOLD
    start_char = 'o'
    # Get the screen position of the arrow
    x_arrow_in_playfield, y_arrow_in_playfield = get_screen_position_from_playfield_position(
        playfield_size_original, playfield, (start_position[1], start_position[0]))
    screen.addch(x_arrow_in_playfield, y_arrow_in_playfield,
                 start_char, arrow_color_pair)


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

    return (x_start + x - round(x_in_playfield), y_start + round(y_in_playfield))


def add_targets_to_playfield(screen: curses.window, playfield_size_original, playfield_size, targets: list):
    target_color_pair = Color_util.DEFAULT_TARGET_COLOR

    for target in targets:
        position, diameter = target
        x_target_in_playfield, y_target_in_playfield = get_screen_position_from_playfield_position(
            playfield_size_original, playfield_size, position)  # Get the screen position of the arrow

        # Get the size of the target in the playfield
        x_target_size_in_playfield = round(
            (diameter[0] / playfield_size_original[0]) * playfield_size[2])
        # Get the size of the target in the playfield
        y_target_size_in_playfield = round(
            (diameter[1] / playfield_size_original[1]) * playfield_size[3])

        # Make sure the target is at least 1 pixel big
        x_target_size_in_playfield = max(1, x_target_size_in_playfield)
        # Make sure the target is at least 1 pixel big
        y_target_size_in_playfield = max(1, y_target_size_in_playfield)

        # Print the square line by line
        for row in range(x_target_size_in_playfield):
            square_line = '#' * y_target_size_in_playfield
            screen.addstr(x_target_in_playfield - row,
                          y_target_in_playfield, square_line, target_color_pair)


def add_top_stats_to_playfield(screen: curses.window, score, size: Size):
    stats = [
        (f'Score: {score}', Color_util.SCORE_COLOR),
        ('[I]nfo', Color_util.INFO_STAT_COLOR),
        ('[Q]uit', Color_util.QUIT_STAT_COLOR),
        ('[C]heats', Color_util.CHEAT_STAT_COLOR),
        ('[S]ave', Color_util.SAVE_STAT_COLOR)
    ]

    score_x = size.get_x_for_score()
    score_y = size.get_y_for_score()
    score_y_offset = 0

    for text, color_pair in stats:
        screen.addstr(score_x, score_y + score_y_offset, text, color_pair)
        score_y_offset += len(text) + 1


def add_info_for_level(screen: curses.window, size: Size, info_list: list, input: Input):
    x_start = int(size.x * 0.1)  # Start 10% from the left
    y_start = int(size.y * 0.1)  # Start 10% from the top
    x_length = int(size.x * 0.8)  # 80% of the width
    y_length = int(size.y * 0.8)  # 80% of the height

    draw_full_lined_border(
        screen=screen,
        x_start=x_start,
        y_start=y_start,
        x_length=x_length,
        y_length=y_length
    )

    if info_list is None or len(info_list) == 0:
        logging.warning('No info for level given')
        info_list = ["No info for level found"]

    line_count = 0
    max_line_count = x_length - 1
    max_line_length = y_length - 3
    new_info_strings = []   # split strings that are to long to print
    for i, info_string in enumerate(info_list):
        if len(info_string) > max_line_length:
            new_strings = split_long_string(info_string, max_line_length)
            new_info_strings += new_strings
            line_count += len(new_strings)
        else:
            new_info_strings.append(info_string)
            line_count += 1

    input.update_info_input(max_line_count, len(new_info_strings))

    if input.max_line_count < input.lines_count:
        add_scoll_bar_for_info(
            screen=screen,
            input=input,
            x_start=x_start,
            x_length=x_length,
            y_start=y_start,
            y_length=y_length)
    for j in range(min(input.lines_count, input.max_line_count)):
        screen.addstr(x_start + 1 + j, y_start + 1,
                      new_info_strings[j + input.line_position])


def add_scoll_bar_for_info(screen: curses.window, input: Input,
                           x_start: int, y_start: int, x_length: int, y_length: int):
    """
    Adds a scroll bar to the info box


    Args:
        screen (curses.window): _description_
        input (Input): _description_
        x_start (int): _description_
        y_start (int): _description_
        x_length (int): _description_
        y_length (int): _description_
    """

    screen.addch(x_start + 1, y_start + y_length -
                 1, '┬')              # top Border
    screen.addch(x_start + x_length - 1, y_start +
                 y_length - 1, '┴')   # bottom Border

    len_bar = max(1, round((input.max_line_count - 1) *
                  ((input.max_line_count - 1) / input.lines_count)))

    x_start_bar = round((input.max_line_count - 1) *
                        (input.line_position / input.lines_count))

    if len_bar + x_start_bar >= input.max_line_count - 1:
        x_start_bar -= 1
    # vertical line for the scroll bar - thin
    for i in range(x_start + 2, x_start + x_length - 1):
        screen.addch(i, y_start + y_length - 1, curses.ACS_VLINE)

    # vertical line for the scroll bar - thick
    for i in range(x_start_bar, x_start_bar + len_bar):
        screen.addch(x_start + i + 2, y_start + y_length - 1, '█')


def split_long_string(string, max_length: int):
    """
    splits a string into substring with a max_len

    Args:
        string (str): the string to split
        max_length (int): the max_length the string should have

    Returns:
        _type_: list of new strings with the content of the old one
    """

    substrings = []
    len_string = len(string)
    for i in range(0, len_string, max_length):
        substrings.append(string[i: i+max_length])
    return substrings


def draw_full_lined_border(screen: curses.window, x_start: int, y_start: int, x_length: int,  y_length: int):
    if screen is None:
        logging.warning("Screen is not set")
        return

    # Draw horizontal lines
    for i in range(y_start, y_start + y_length):
        screen.addch(x_start, i, curses.ACS_HLINE)  # Top border line
        # Bottom border line
        screen.addch(x_start + x_length, i, curses.ACS_HLINE)

    # Draw vertical lines
    for i in range(x_start, x_start + x_length):
        screen.addch(i, y_start, curses.ACS_VLINE)  # Left border line
        # Right border line
        screen.addch(i, y_start + y_length, curses.ACS_VLINE)

    # Draw corner characters
    screen.addch(x_start, y_start, curses.ACS_ULCORNER)  # Upper left corner
    screen.addch(x_start, y_start + y_length,
                 curses.ACS_URCORNER)  # Upper right corner
    screen.addch(x_start + x_length, y_start,
                 curses.ACS_LLCORNER)  # Lower left corner
    screen.addch(x_start + x_length, y_start + y_length,
                 curses.ACS_LRCORNER)  # Lower right corner


def add_cheats_to_playfield(screen: curses.window,
                            size: Size, playfield, playfield_size_original, trajectory: ArrowTrajectory):
    """Adds the cheats to the playfield

    Args:
        screen (curses.window): the screen to draw on
        size (Size): the size of the screen
        playfield (Playfield): the playfield to draw
        playfield_size_original (Size): the original size of the playfield
        trajectory (ArrowTrajectory): the trajectory to draw
    """
    if screen is None:
        logging.warning("Screen is not set")
        return
    for step in trajectory.all_steps:
        add_arrow_to_playfield(
            screen, playfield_size_original, playfield, step)


def draw_full_lined_border_with_message(screen: curses.window,
                                        x_start: int, y_start, x_length: int, y_length,
                                        message: str, color_for_message: int = 0):
    """
    Draws a border around the screen and adds a message in the middle

    Args:
        screen (curses.window): the screen to draw on
        x_start (int): the x start position of the border
        y_start (int): the y start position of the border
        x_length (int): the x length of the border
        y_length (int): the y length of the border
        message (str): the message to display in the middle
    """
    draw_full_lined_border(screen, x_start, y_start, x_length, y_length)
    # box1 = screen.subwin(x_length, y_length, x_start, y_start)
    # box1.box()

    if message is None or len(message) == 0:
        # No message to display, return early
        return

    color_for_message = Color_util.get_color_pair_with_number(
        color_for_message)                        # Get the color pair for the message

    if len(message) > y_length:
        # Message is too long to display, cut it
        logging.warning("Message is too long to display")
        message = message[:y_length]

    screen.addstr(x_start, y_start + y_length // 2 -
                  len(message) // 2, message, color_for_message)
