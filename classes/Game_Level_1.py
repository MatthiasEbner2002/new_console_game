import time, logging
from classes.Screen import *
from classes.Size import Size


class Game_Level_1:
    def __init__(self, screen: curses.window):
         self.screen = screen
         self.size = Size.from_terminal_size(screen)
         
         
    def run(self):
        while True:
            self.screen.clear()
            time.sleep(1)
            self.size.update_terminal_size_with_logging_and_screen_refresh()
            draw_borders(self.screen, self.size)
            draw_playfield_borders(self.screen, self.size)
            # add_user_platform(self.screen, self.size)
            self.screen.refresh()
            
    def _render():
        pass
    
    def _update():
        pass
    
    def _handle_input():
        pass
            
    