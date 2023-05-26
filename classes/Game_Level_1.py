import time, logging
from classes.Screen import *
from classes.Size import Size
from classes.test_arrow import ArrowTrajectory


class Game_Level_1:
    def __init__(self, screen: curses.window):
         self.screen = screen
         self.size = Size.from_terminal_size(screen)
         
         
    def run(self):
        start_location = (1, 1)  # Starting location of the arrow
        start_power = 25  # Initial power of the arrow
        angle = 45  # Launch angle in degrees
        gravity = 9.8  # Acceleration due to gravity

        trajectory = ArrowTrajectory(start_location, start_power, angle, gravity)
        
        playfield_size_original  = (22.7, 100)
        
        
        while True:
            self.screen.clear()
            time.sleep(0.01)
            
            self.size.update_terminal_size_with_logging_and_screen_refresh()
            draw_borders(self.screen, self.size)
            
            playfield_size = draw_playfield_borders(self.screen, self.size)
            
            step = trajectory.calculate_step()
            if step[0] > playfield_size_original[0] or step[0] < 0 or step[1] > playfield_size_original[1] or step[1] < 0:
                logging.info("Game_Level_1.py | run(): Arrow is out of bounds")
                break
            
            add_arrow_to_playfield(self.screen, playfield_size_original, playfield_size, step)
            
            self.screen.refresh()
            
    def _render():
        pass
    
    def _update():
        pass
    
    def _handle_input():
        pass
            
    