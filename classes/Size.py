import logging


class Size:
    """
    used to represent the screen size of the used console.
    
    Vars:
        x = rows, Höhe, height \n
        y = columns, Breite, width \n
        screen = the screen object of curses \n
    """
   
    def __init__(self, x: int, y: int, screen):
        self.x = (1, x)[x >= 1]
        self.y = (1, y)[y >= 1]
        self.screen = screen

    @classmethod
    def from_terminal_size(cls, screen):
        """ get the screen size and return new Size() object.

        Args:
            screen (_type_): screen (curses)

        Returns:
            new Size(): with x, y and screen set
        """
        rows, columns = screen.getmaxyx()
        return cls(int(rows) - 1, int(columns), screen)
    
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
        columns = int(columns)

        self.x = (1, rows)[rows >= 1]
        self.y = (1, columns)[columns >= 1]
        
    def refresh_screen(self):
        if self.screen is None:
            logging.warning("size.py | refresh_screen(): screen is None")
            return
        
        self.screen.refresh()
    
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