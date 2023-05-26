import time, logging, keyboard


from classes.Screen import *
from classes.Size import Size
from classes.test_arrow import ArrowTrajectory
from classes.Input import Input



class Game_Level_1:
    def __init__(self, screen: curses.window):
        self.screen = screen
        self.size = Size.from_terminal_size(screen)
        self.render_what = 'arrow'
        self.power = 25              # Initial power of the arrow
        self.angle = 45              # Launch angle in degrees
        self.gravity = 9.8           # Acceleration due to gravity    
        self.start_location = (1, 1) # Starting location of the arrow
        self.input = Input(self.render_what)
         
    def run(self):

        trajectory = ArrowTrajectory(self.start_location, self.power, self.angle, self.gravity)
        
        playfield_size_original  = (22.7, 100) # (height, width)
        
        while True:
            self.screen.clear()
            self.size.update_terminal_size_with_screen_refresh()
            draw_borders(self.screen, self.size)
            playfield_size = draw_playfield_borders(self.screen, self.size)
            
                    
            match self.input.space:
                case 1:
                    step = trajectory.calculate_step()
                    if step[0] > playfield_size_original[0] or step[0] < 0 or step[1] > playfield_size_original[1] or step[1] < 0:
                        logging.info("Game_Level_1.py | run(): Arrow is out of bounds")
                        break
                    
                    add_arrow_to_playfield(self.screen, playfield_size_original, playfield_size, step)
                    self.screen.refresh()
                    time.sleep(0.01)
                    
                
                case 0:
                    self.angle += 3
                    self.angle %= 360
                    add_angle_to_playfield(self.screen, self.size, self.angle)
                    self.screen.refresh()
                    time.sleep(2 / 120)
            
            
    def _render():
        pass
    
    def _update():
        pass
    
    def _handle_input():
        pass
            
    