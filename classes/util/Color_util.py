import curses


class Color_util:
    # Define your custom color
    # Each terminal has a different number of colors
    # TODO: make a config file for colors

    color_default_background: int = -1

    color_green: int = 41
    color_light_blue: int = 160
    color_red: int = 161
    color_turquoise: int = 50
    color_pink: int = 200
    color_dark_pink: int = 130

    @classmethod
    def init_colors(cls):
        curses.start_color()            # initialize color
        curses.use_default_colors()     # use default colors of terminal
        Color_util.init_color_pairs()   # init color pairs

        cls.PLAYFIELD_BORDER_COLOR = curses.color_pair(cls.color_green)
        cls.ARROW_COLOR = curses.color_pair(cls.color_light_blue)
        cls.ARROW_START_COLOR = curses.color_pair(cls.color_light_blue)
        cls.DEFAULT_TARGET_COLOR = curses.color_pair(cls.color_red)
        cls.SCORE_COLOR = curses.color_pair(cls.color_dark_pink)
        cls.INFO_STAT_COLOR = curses.color_pair(cls.color_turquoise)
        cls.QUIT_STAT_COLOR = curses.color_pair(cls.color_red)
        cls.CHEAT_STAT_COLOR = curses.color_pair(cls.color_pink)

    @classmethod
    def init_color_pairs(cls):
        #  init 255 colors
        for i in range(0, 255):
            curses.init_pair(i + 1, i, cls.color_default_background)

    def get_color_pair_with_number(number: int) -> int:
        return curses.color_pair(number)
