import curses



class Color_util:
    DEFAULT_TARGET_COLOR = 0
    ARROW_COLOR = 0
    ARROW_START_COLOR = 0
    PLAYFIELD_BORDER_COLOR = 0
    BORDER_COLOR = 0
    SCORE_COLOR = 0
        
    @classmethod
    def init_colors(cls):
        cls.PLAYFIELD_BORDER_COLOR = curses.color_pair(41)
        cls.ARROW_COLOR = curses.color_pair(160)
        cls.ARROW_START_COLOR = curses.color_pair(160)
        cls.DEFAULT_TARGET_COLOR = curses.color_pair(161)
        cls.SCORE_COLOR = curses.color_pair(130)
        