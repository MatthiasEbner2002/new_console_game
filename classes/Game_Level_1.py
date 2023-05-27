import time, logging, keyboard, curses


from classes.Screen import *
from classes.Size import Size
from classes.test_arrow import ArrowTrajectory
from classes.Input import Input



class Game_Level_1:
    def __init__(self, screen: curses.window):
        self.screen: curses.window = screen                     # Curses window object, handles screen refreshes
        self.size: Size = Size.from_terminal_size(screen)       # Size object, handles screen size and calculations for screen positions
        self.power: int = 0                                     # Launch power   
        self.max_power: int  = 25                               # Maximum launch power
        self.angle: int = 45                                    # Launch angle in degrees
        self.gravity: float = 9.8                               # Acceleration due to gravity    
        self.start_location = (1, 1)                            # Starting location of the arrow
        self.input: Input = Input(self)                         # Input object, handles keyboard input
        self.trajectory: ArrowTrajectory = None                 # ArrowTrajectory object, handles arrow trajectory calculations
         
    def run(self):

        
        playfield_size_original  = (22.7, 100) # (height, width)
        trajectory = None
        step = None
        
        
        while True:
            self.screen.clear()
            self.size.update_terminal_size_with_screen_refresh()
            draw_borders(self.screen, self.size)
            playfield_size = draw_playfield_borders(self.screen, self.size)
            
                    
            match self.input.space:
                                
                case 0:
                    """
                    This code snippet is used to change the angle of the arrow.
                    """
                    self.angle += 3
                    self.angle %= 360
                    add_angle_to_playfield(self.screen, self.size, self.angle)
                    add_arrow_start_to_playfield(self.screen, playfield_size_original,playfield_size, self.start_location)
                    self.screen.refresh()
                    time.sleep(3 / 120)
                    
                    
                case 1:
                    """
                    This code snippet is used to change the power of the arrow.
                    """
                    self.power = (self.power + 1) % self.max_power
                    add_angle_to_playfield(self.screen, self.size, self.angle)
                    add_power_to_playfield(self.screen, self.size, self.power, self.max_power)
                    self.screen.refresh()
                    time.sleep(4 / 120)
                    
                case 2: 
                    
                    add_angle_to_playfield(self.screen, self.size, self.angle)
                    add_power_to_playfield(self.screen, self.size, self.power, 25)
                        
                    if self.trajectory is None:
                        logging.error("Game_Level_1.py | run(): Trajectory is None")                        
                    else:
                        old_step = step
                        step = self.trajectory.calculate_step()
                        if step[0] > playfield_size_original[0] or step[0] < 0 or step[1] > playfield_size_original[1] or step[1] < 0:
                            logging.info("Game_Level_1.py | run(): Arrow is out of bounds")
                            if old_step is not None:
                                self.start_location = (old_step[1], old_step[0])
                                self.remove_arrow_and_set_input_to_get_new_angle()
                            else:
                                logging.error("Game_Level_1.py | run(): old_step is None, start location was out of bounds.")
                                break
                        
                        add_arrow_to_playfield(self.screen, playfield_size_original, playfield_size, step)
                        self.screen.refresh()
                        time.sleep(0.01)
                    
            
            
    def _render():
        pass
    
    def _update():
        pass
    
    def remove_arrow_and_set_input_to_get_new_angle(self):
        self.input.space = 0
        self.trajectory = None
        logging.info("Game_Level_1.py | remove_arrow_and_set_input_to_get_new_angle(): Arrow removed and input set to get new angle.")
    