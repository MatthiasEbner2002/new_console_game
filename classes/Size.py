import logging
import curses


class Size:
    """
    used to represent the screen size of the used console.

    Vars:
        x = rows, Höhe, height \n
        y = columns, Breite, width \n
        screen = the screen object of curses \n
    """

    def __init__(self, screen: curses.window, x_start: int = 1, y_start: int = 0):
        self.screen = screen
        self.x = 10
        self.y = 10
        self.Y_SCORE = 5
        self.X_SCORE = 0
        self.menu_x_size = 10
        self.x_verhältnis = 0.185
        self.y_verhältnis = 1 - self.x_verhältnis

        if x_start < 0:
            logging.error("x_start is smaller then 1, setting it to 1")
            x_start = 0
        self.x_start = x_start

        if y_start < 0:
            logging.error("y_start is smaller then 1, setting it to 1")
            y_start = 0
        self.y_start = y_start

    def __str__(self):
        return f"console_size: x= {self.x}, y= {self.y}"

    @classmethod
    def from_terminal_size(cls, screen: curses.window):
        """ get the screen size and return new Size() object."""
        ret = cls(screen)
        ret.update_terminal_size()
        return ret

    def set_new_size(self, x: int, y: int):
        """ sets the new x and y values"""
        if x < 10 or y < 10:
            logging.warning("x or y is smaller then 10, cant urn like this")

        self.x = x
        self.y = y

    def update_terminal_size_with_logging(self):
        """calls Size methode to update size and logs the new x and y values."""
        self.update_terminal_size()
        logging.info(self)

    def update_terminal_size_with_screen_refresh(self):
        """
        Updates the screen, to get the actual screen size,
        if not refreshed the size is of the last refresh and if never refresed, from the programm-Start.
        """

        self.refresh_screen()
        self.update_terminal_size()

    def update_terminal_size(self):
        """Updates the screen x and y of the Console."""

        if self.screen is None:
            logging.warn("Cannot update, because screen is not set")
            return

        rows, columns = self.screen.getmaxyx()

        rows = int(rows) - 2
        columns = int(columns) - 1
        self.set_new_size(rows, columns)

    def refresh_screen(self):
        """Refreshes the screen, if screen is None, logs warning."""

        if self.screen is None:
            logging.warning("Screen is None")
            return

        self.screen.refresh()

    def calculate_playfield(self):
        """
        calculates the playfield size, based on the console size and the x and y verhältnis.
        if the x verhältnis is bigger then the y verhältnis, the playfield_y is the max_y and
        the playfield_x is calculated from the y verhältnis.

        Returns:
            tuple: playfield_x, playfield_y
        """

        max_x = self.get_x()
        max_y = self.get_y()

        if max_x / (max_x + max_y) < self.x_verhältnis:
            playfield_x = max_x
            playfield_y = min(int(max_x / self.x_verhältnis * self.y_verhältnis), max_y)
            playfield_y_start = int((max_y - playfield_y) / 2)
            playfield_x_start = self.x_start

        else:
            playfield_y = max_y
            playfield_x = min(int(max_y / self.y_verhältnis * self.x_verhältnis), max_x)
            playfield_x_start = max(int((max_x - playfield_x) / 2), 1)
            playfield_y_start = self.y_start

        return playfield_x_start, playfield_y_start, playfield_x, playfield_y

    def is_playfield_x_smaller_then_x_verhältnis(self):
        return self.get_x() / (self.get_x() + self.get_y()) <= self.x_verhältnis

    def get_x(self):
        """returns x, the x value of the playfield"""
        return self.x - self.x_start - self.menu_x_size

    def get_y(self):
        """returns y, the y value of the playfield"""
        return self.y - self.y_start

    def get_x_for_angle(self):
        return self.get_x() + (self.menu_x_size // 2) + 1

    def get_y_for_angle(self):
        return self.y_start + (self.menu_x_size // 2) + 10

    def get_x_for_progress_bar(self):
        return self.get_x_for_angle()

    def get_y_for_progress_bar(self):
        return self.get_y_for_angle() + 20
