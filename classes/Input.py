from pynput import keyboard
from pynput.keyboard import Key

from classes.Score_Manager import Score_Manager
from classes.Score_Position import ScorePosition


class Input:
    """
    Class for handling input from the user.
    """

    def __init__(self, level, max_power: int = 25):
        self.disable_input = False  # disable input or not
        self.level = level
        self.score_manager = Score_Manager()
        self.score = 0  # Score, the Points

        self.cheats = False  # cheats enabled or not
        self.show_info = False  # show info or not
        self.max_line_count = 0  # max lines that can be shown
        self.line_position = 0  # actual position in the lines
        self.lines_count = 0  # how many lines exist
        self.get_name = False  # get name for highscore

        self.angle = 0
        self.power = 0

        self.max_power = max_power

        # listener is a thread, so it will run in the background
        listener = keyboard.Listener(
            on_press=self.key_down, on_release=self.key_up)
        listener.start()

    def key_down(self, key):
        """
        This function is used to handle key presses.

        Args:
            key : The key that was pressed.
        """
        if self.disable_input:
            return

        if key == Key.up:
            if self.show_info:
                if self.line_position > 0:
                    self.line_position -= 1
            else:
                self.up = 1
                self.angle += 5

        elif key == Key.down:
            if self.show_info:
                if self.line_position < self.lines_count - self.max_line_count:
                    self.line_position += 1
            else:
                self.down = 1
                self.angle -= 5

        elif key == Key.left:
            if self.power > 0:
                self.power -= 1

        elif key == Key.right:
            self.right = 1
            if self.power < self.max_power:
                self.power += 1

        elif key == Key.space:
            self.level.next_step_for_game()

        elif key.char == 'i':
            self.show_info = not self.show_info

        elif key.char == 'q':
            self.q = 1
            self.show_info = False
            self.level.stop_game_and_exit()

        elif key.char == 'c':
            self.cheats = not self.cheats

        elif key.char == 's':
            self.get_name = True

        self.angle %= 360

    def key_up(self, key):
        """
        This function is used to handle key releases.

        Args:
            key: The key that was released.
        """
        if self.disable_input:
            return

        if key == Key.up:
            self.up = 0
        elif key == Key.down:
            self.down = 0
        elif key == Key.left:
            self.left = 0
        elif key == Key.right:
            self.right = 0
        elif key == Key.space:
            pass

    def update_info_input(self, max_line_count: int, lines: int):
        self.max_line_count = max_line_count
        self.lines_count = lines

        if self.line_position + max_line_count > self.lines_count:
            self.line_position = max(0, self.lines_count - self.max_line_count)

    def add_score(self, score_position: ScorePosition):
        self.score_manager.add_score(score_position)
