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
   
    def __init__(self, x: int, y: int, screen: curses.window):
        self.x = max(1, x)
        self.y = max(1, y)
        self.screen = screen
        self.menu_x_size = 10
        self.x_verhältnis = 0.185
        self.y_verhältnis = 0.815

    @classmethod
    def from_terminal_size(cls, screen):
        """ get the screen size and return new Size() object.

        Args:
            screen (_type_): screen (curses)

        Returns:
            new Size(): with x, y and screen set
        """
        rows, columns = screen.getmaxyx()
        return cls(int(rows) - 1, int(columns) - 1, screen)
    
    def update_terminal_size_with_logging_and_screen_refresh(self):
        """
        refreshed screen and udpates the console_size and logs the new x and y.
        """
        
        self.refresh_screen()
        self.update_terminal_size_with_logging()
        

    def update_terminal_size_with_logging(self):
        """
        calls Size methode to update size and logs the new x and y values.
        """
        
        self.update_terminal_size()
        self.toLogging()
    
    def update_terminal_size_with_screen_refresh(self):
        """
        Updates the screen, to get the actual screen size,
        if not refreshed the size is of the last refresh and if never refresed, from the programm-Start.
        """
        
        self.refresh_screen()
        self.update_terminal_size()
    
    def update_terminal_size(self):
        """
        Updates the screen x and y of the Console.
        If smaller then 1 sets it to 1.
        If screen is not set and still None, logs warning.
        """
        if self.screen == None:
            logging.warn("Size.py | update_terminal_size(): cannot update, because screen is not set")
            return
        
        rows, columns = self.screen.getmaxyx()
        
        rows = int(rows) - 1
        columns = int(columns) - 1

        self.x = max(1, rows)
        self.y = max(1, columns)
        
    def refresh_screen(self):
        """
        Refreshes the screen, if screen is None, logs warning.
        """
        
        if self.screen is None:
            logging.warning("size.py | refresh_screen(): screen is None")
            return
        
        self.screen.refresh()
        
    def get_x_start(self):
        """ returns x_start, the x value where the playfield starts

        Returns:
            int: x_start
        """
        
        return 1
    
    def get_y_start(self):
        """
        returns y_start, the y value where the playfield starts

        Returns:
            int: y_start
        """
        
        return 1
        
    def get_x(self):
        """
        returns x, the x value of the playfield

        Returns:
            int: x
        """
        
        return self.x - 1 - self.menu_x_size
    
    def get_y(self):
        """
        returns y, the y value of the playfield

        Returns:
            int: y
        """
        
        return self.y - 1
    
    def calculate_playfield(self):
        """
        calculates the playfield size, based on the console size and the x and y verhältnis.
        if the x verhältnis is bigger then the y verhältnis, the playfield_y is the max_y and the playfield_x is calculated from the y verhältnis.

        Returns:
            tuple: playfield_x, playfield_y
        """
        
        max_x = self.get_x() + 1
        max_y = self.get_y() + 1
        
        if max_x / (max_x + max_y) <= self.x_verhältnis:
            playfield_x = max_x
            playfield_y = min(int(max_x / self.x_verhältnis * self.y_verhältnis), max_y)
            playfield_y_start = int((max_y - playfield_y) / 2)
            playfield_x_start = 0
            
        else:
            playfield_y = max_y
            playfield_x = min(int(max_y / self.y_verhältnis * self.x_verhältnis), max_x)
            playfield_x_start = int((max_x - playfield_x) / 2)
            playfield_y_start = 0
            
        return playfield_x_start, playfield_y_start, playfield_x, playfield_y
    
    
    def get_x_for_border(self):
        """ returns x for border, the biggest x possible

        Returns:
            _type_: _description_
        """
        return self.x
    
    
    
    def get_y_for_border(self):
        """ returns y for border, the biggest y possible

        Returns:
            _type_: _description_
        """
        return self.y
    
    def get_x_for_angle(self):
        """
        
        """
        return self.get_x() + (self.menu_x_size // 2) + 1
    
    def get_y_for_angle(self):
        """
        
        """
        return self.get_y_start() + (self.menu_x_size // 2) + 10
    
    
    def get_x_for_progress_bar(self):
        """
        
        """
        return self.get_x_for_angle()
    
    def get_y_for_progress_bar(self):
        """
        
        """
        return self.get_y_for_angle() + 20
    
    
    def toLogging(self):
        """
        loggs info of the toString() aka. x and y values
        """
        
        logging.info(self.toString())

    def toString(self):
        """
        return x and y

        Returns:
            string: x, y values
        """
        
        ret = f"console_size: x= {self.x}, y= {self.y}"
        return ret 