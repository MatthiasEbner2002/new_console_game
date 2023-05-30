import time, logging, curses


from classes.Screen import *
from classes.Size import Size
from classes.ArrowTrajectory import ArrowTrajectory
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
        self.run_game: bool = True                              # Boolean, used to stop the game loop
        self.playfield_size_original = (22.7, 100)              # (height, width), original size of the playfield, for scaling purposes and calculations
        self.game_step_for_game_loop = 0                        # Integer, used to keep track of the current game step in the game loop
        self.power_up = True                                    # Boolean, used to keep track of the power direction
        self.targets = [((21, 99), (1, 1))]                     # List, used to keep track of the targets ((x, y), (diameter_x, diameter_y))

    def run(self):

        
        step = None
        
        
        while self.run_game:
            self.screen.clear()                                             # Clear the screen
            self.size.update_terminal_size_with_screen_refresh()            # Update the size object with the new terminal size
            draw_borders(self.screen, self.size)                            # Draw the borders of the screen
            playfield_size = draw_playfield_borders(self.screen, self.size) # Draw the borders of the playfield
            add_arrow_start_to_playfield(self.screen, self.playfield_size_original, playfield_size, self.start_location) # Draw the starting location of the arrow
            
            center_of_target = (10, 50)
            target_diameter = 3
            add_test_target(self.screen, self.playfield_size_original, playfield_size, center_of_target, target_diameter) # Draw the test target
            add_targets_to_playfield(self.screen, self.playfield_size_original, playfield_size, self.targets) # Draw the target
            
                    
            match self.game_step_for_game_loop:
                                
                case 0:
                    """
                    This code snippet is used to change the angle of the arrow.
                    """
                    self.angle += 3
                    self.angle %= 360
                    add_angle_to_playfield(self.screen, self.size, self.angle) # Draw the angle of the arrow
                    self.screen.refresh()
                    time.sleep(3 / 120)
                    
                    
                case 1:
                    """
                    This code snippet is used to change the power of the arrow.
                    """
                    # starts at 0, goes to 25, then starts at 0 again
                    # self.power = (self.power + 1) % (self.max_power + 1)
                    
                    # starts at 0, goes to 25, then back to 0
                    if self.power_up:
                        self.power += 1
                    else:
                        self.power -= 1
                    
                    if self.power == self.max_power:
                        self.power_up = False
                        
                    elif self.power == 0:
                        self.power_up = True
                        
                    
                    
                    add_angle_to_playfield(self.screen, self.size, self.angle)
                    add_power_to_playfield(self.screen, self.size, self.power, self.max_power)
                    self.screen.refresh()
                    time.sleep(4 / 120)
                    
                case 2: 
                    """
                    This code snippet is used to calculate the trajectory of the arrow.
                    """
                    
                    add_angle_to_playfield(self.screen, self.size, self.angle)
                    add_power_to_playfield(self.screen, self.size, self.power, 25)
                        
                    if self.trajectory is None:
                        logging.error("Trajectory is None")                        
                    else:
                        step = self.trajectory.calculate_step() # Calculate the next step of the arrow
                        if step[0] > self.playfield_size_original[0] or step[0] < 0 or step[1] > self.playfield_size_original[1] or step[1] < 0:
                            logging.info("Arrow is out of bounds")
                            if self.trajectory.old_step is not None:
                                self.start_location = (self.trajectory.old_step[1], self.trajectory.old_step[0])
                                self.remove_arrow_and_set_input_to_get_new_angle()
                            else:
                                logging.error("Old_step is None")
                                self.stop_game_and_exit()


                        if self.trajectory is not None:
                            for target in self.targets:
                                if self.trajectory.old_step is not None:
                                    if line_intersects_square(self.trajectory.old_step[0], self.trajectory.old_step[1], step[0], step[1], target):
                                        logging.info("Arrow hit target")
                                        self.stop_game_and_exit()
                                        break
                                else:
                                    if point_inside_square(step[0], step[1], target):
                                        logging.info("Arrow hit target")
                                        self.stop_game_and_exit()
                                        break
                        
                        add_arrow_to_playfield(self.screen, self.playfield_size_original, playfield_size, step)
                        self.screen.refresh()
                        time.sleep(0.01)
        logging.info("Game loop exited.")
                    
            
            
    def _render():
        pass
    
    def _update():
        pass
    
    def remove_arrow_and_set_input_to_get_new_angle(self):
        self.game_step_for_game_loop = 0
        self.trajectory = None
        logging.info("Arrow removed and input set to get new angle.")
    
    
    def stop_game_and_exit(self):
        """
        This function is used to stop the game loop and exit the game.
        """
        
        self.run_game = False
        logging.info("Game stopped and should exit.")
        
        
    def stop_arrow_and_remove_arrow_and_safe_last_position(self):
        """
        This function is used to stop the arrow and remove it from Level and safe the new starting location.

        """
        
        if self.trajectory is None  or self.trajectory.actual_step is None:
            logging.error("trajectory does not exist or has not calculated any step")
        
        self.start_location = (self.trajectory.actual_step[1], self.trajectory.actual_step[0])
        self.trajectory = None
        
        
    def next_step_for_game(self):
        """
        This function is used to go to the next step in the game.
        Swtiches between the different game steps.
        """
        
        match self.game_step_for_game_loop:
            case 0:
                logging.info("Next step | getting angle finished") 
                self.game_step_for_game_loop = 1

            case 1:
                logging.info("Next step | getting power finished")
                
                self.trajectory = ArrowTrajectory(self.start_location, self.power, self.angle, self.gravity)                    
                self.game_step_for_game_loop = 2
                
            case 2:
                logging.info("Next step | trajectory finished")
                self.stop_arrow_and_remove_arrow_and_safe_last_position()
                self.game_step_for_game_loop = 0
            
            case default:
                logging.error(f"Next step | default case: no case found for game_step_for_game_loop = {self.game_step_for_game_loop}")
                
            
            
def line_intersects_square(x1, y1, x2, y2, target):
    ((square_x, square_y), (square_width, square_height)) = target
    # Check if any of the line endpoints are inside the square
    if point_inside_square(x1, y1, target) or \
            point_inside_square(x2, y2,target):
        logging.debug("Point inside square")
        return True

    # Check if the line intersects any of the square's sides
    """


    if line_intersects_side(x1, y1, x2, y2, square_x, square_y, square_x + square_width, square_y) or \
            line_intersects_side(x1, y1, x2, y2, square_x + square_width, square_y, square_x + square_width, square_y + square_height) or \
            line_intersects_side(x1, y1, x2, y2, square_x + square_width, square_y + square_height, square_x, square_y + square_height) or \
            line_intersects_side(x1, y1, x2, y2, square_x, square_y + square_height, square_x, square_y):
        logging.debug("Line intersects side")   
        return True
    """

    return False


def point_inside_square(x, y, target):
    ((square_x, square_y), (square_width, square_height)) = target
    
    return square_x <= x <= square_x + square_width and square_y <= y <= square_y + square_height


def line_intersects_side(x1, y1, x2, y2, side_x1, side_y1, side_x2, side_y2):
    # Determine if the line intersects the side using line-line intersection algorithm
    # (Assuming the line endpoints are not on the same side)
    return (
            (y1 - side_y1) * (side_x2 - side_x1) - (x1 - side_x1) * (side_y2 - side_y1)
    ) * (
            (y2 - side_y1) * (side_x2 - side_x1) - (x2 - side_x1) * (side_y2 - side_y1)
    ) <= 0
