import time, logging, curses, random, numpy as np


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
        self.gravity: float = 9.8                               # Acceleration due to gravity    
        self.start_location = (1, 1)                            # Starting location of the arrow
        self.input: Input = Input(self, self.max_power)         # Input object, handles keyboard input
        self.trajectory: ArrowTrajectory = None                 # ArrowTrajectory object, handles arrow trajectory calculations
        self.run_game: bool = True                              # Boolean, used to stop the game loop
        self.playfield_size_original = (22.7, 100)              # (height, width), original size of the playfield, for scaling purposes and calculations
        self.playfield_size = None                              # (height, width), size of the playfield, for scaling purposes and calculations
        self.game_step_for_game_loop: int = 0                   # Integer, used to keep track of the current game step in the game loop
        self.targets = [((0, 10), (1, 1))]                      # List, used to keep track of the targets ((x, y), (diameter_x, diameter_y))
        self.arrow_radius = 0.25                                # Radius of the arrow, its a circle to make it easier to calculate the collision with the targets
        self.cheat_trajectory: ArrowTrajectory = None           # ArrowTrajectory object, used to show the trajectory of the arrow when the cheats are enabled
    def run(self):

        
        step = None
        
        
        while self.run_game:
            
            if self.input.show_info: # Show info
                self.show_info_in_own_loop()
                if self.run_game is False: # if info was interupted by quit
                    break

            
            self.screen.clear()                                                                                                                 # Clear the screen
            
            self.size.update_terminal_size_with_screen_refresh()                                                                                # Update the size object with the new terminal size
            
            draw_borders(self.screen, self.size)                                                                                                # Draw the borders of the screen
            self.playfield_size = draw_playfield_borders(self.screen, self.size)                                                                # Draw the borders of the playfield
            add_arrow_start_to_playfield(self.screen, self.playfield_size_original, self.playfield_size, self.start_location)                   # Draw the starting location of the arrow
            add_targets_to_playfield(self.screen, self.playfield_size_original, self.playfield_size, self.targets)                              # Draw the target
            add_top_stats_to_playfield(self.screen, self.playfield_size_original, self.playfield_size, self.input.score, self.size)                   # Draw the score
                    
            match self.game_step_for_game_loop:
                                
                case 0: # Getting angle / power
                    
                    add_angle_to_playfield(self.screen, self.size, self.input.angle)
                    add_power_to_playfield(self.screen, self.size, self.input.power, self.max_power)
                    
                    
                    if self.input.cheats:
                        if self.cheat_trajectory is None or self.cheat_trajectory.angle != self.input.angle or self.cheat_trajectory.start_power != self.input.power:
                            # if cheat_trajectory is None or the input values (angle, power) changed, update the trajectory
                            
                            self.cheat_trajectory = ArrowTrajectory(self.start_location, self.input.power, self.input.angle, self.gravity)
                            self.cheat_trajectory.calculate_all_steps(self.playfield_size_original)
                        add_cheats_to_playfield(self.screen, self.size, self.playfield_size, self.playfield_size_original, self.cheat_trajectory)
                    
                    self.screen.refresh()
                    
                    time.sleep(1 / 60)
                    
                    
                case 1: # Trajectory calculation
                    self.cheat_trajectory = None                    
                    add_angle_to_playfield(self.screen, self.size, self.input.angle)
                    add_power_to_playfield(self.screen, self.size, self.input.power, self.max_power)
                    self.step_for_trajectory()
                    time.sleep(1 / 60) 
 
                    
                    
                    
                    
        logging.info("Game loop exited.")
                    
    
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
                logging.info("Next step | getting angle / power finished") 
                self.trajectory = ArrowTrajectory(self.start_location, self.input.power, self.input.angle, self.gravity)                    
                self.game_step_for_game_loop = 1

            case 1:
                logging.info("Next step | trajectory finished")
                self.stop_arrow_and_remove_arrow_and_safe_last_position()
                self.game_step_for_game_loop = 0
            
            case default:
                logging.error(f"Next step | default case: no case found for game_step_for_game_loop = {self.game_step_for_game_loop}")
      
                
    def move_target_to_new_random_location_and_increase_score(self, target):
        self.input.score += 1
        logging.info(f"New Score: {self.input.score}")
        old_target = target
        (x_position, y_position), diameter = target
        while old_target[0][0] == x_position or old_target[0][1] == y_position:
            x_position = random.uniform(0, self.playfield_size_original[0] - diameter[0])
            y_position = random.uniform(0, self.playfield_size_original[1] - diameter[1])
            
        
        return ((x_position, y_position), diameter)
      
      
    def step_for_angle(self):
        """
        This code snippet is used to change the angle of the arrow.
        """

        add_angle_to_playfield(self.screen, self.size, self.input.angle) # Draw the angle of the arrow
        self.screen.refresh()
        
        
    def step_for_power(self):
        """
        This code snippet is used to change the power of the arrow.
        """

        add_power_to_playfield(self.screen, self.size, self.input.power, self.max_power)
        self.screen.refresh()
    
    
    def step_for_trajectory(self):
        """
        This code snippet is used to calculate the trajectory of the arrow.
        """
            
        if self.trajectory is None:
            logging.error("Trajectory is None")
            return   
                          
        else:
            step = self.trajectory.calculate_step() # Calculate the next position of the arrow
            if step[0] > self.playfield_size_original[0] or step[0] < 0 or step[1] > self.playfield_size_original[1] or step[1] < 0:
                logging.info("Arrow is out of bounds")
                if self.trajectory.old_step is not None:
                    self.start_location = (self.trajectory.old_step[1], self.trajectory.old_step[0])
                    self.remove_arrow_and_set_input_to_get_new_angle()
                else:
                    logging.error("Old_step is None")
                    self.stop_game_and_exit()


            if self.trajectory is not None:
                for i, target in enumerate(self.targets):
                    if self.trajectory.old_step is not None:
                        
                        if line_intersects_square(self.trajectory.old_step[0], self.trajectory.old_step[1], step[0], step[1], target, self.arrow_radius):
                            logging.info("Arrow hit target")
                            self.targets[i] = self.move_target_to_new_random_location_and_increase_score(target)
                            break
                    else:
                        if point_inside_square(step[0], step[1], target):
                            logging.info("Arrow hit target")
                            self.targets[i] = self.move_target_to_new_random_location_and_increase_score(target)
                            break
            
            add_arrow_to_playfield(self.screen, self.playfield_size_original, self.playfield_size, step)
            self.screen.refresh()

   
    def show_info_in_own_loop(self):
        while self.input.show_info:
            self.screen.clear()                                  # Clear the screen
            self.size.update_terminal_size_with_screen_refresh() # Update the size object with the new terminal size
            
            add_info_for_level(self.screen, self.size, self.get_infos(), self.input)

            self.screen.refresh()

            time.sleep(1/60)
            
        logging.info("exit the info Box for level.")

      
    def get_infos(self):
        ret = []
        
        ret.append("INFOS FOR LEVEL")
        ret.append("")
        ret.append("Press 'arrow_up' to increase the angle of the arrow")
        ret.append("Press 'arrow_down' to decrease the angle of the arrow")
        ret.append("")
        ret.append("Press 'arrow_right' to increase the power of the arrow")
        ret.append("Press 'arrow_left' to decrease the power of the arrow")
        ret.append("press 'space' to shoot the arrow")
        ret.append("")
        ret.append("Press 'i' to show this info box")
        ret.append("")
        ret.append("Press 'q' to quit the game")
        ret.append("")
        ret.append("Press 'c' to activale cheats")
        
        
        return ret

       
    def get_test_infos(self):
        info_list = []
        for i in range (100):
            info_list.append("This is a test info: test test test test test test test test" + str(i))
        return info_list


def line_intersects_square(x1, y1, x2, y2, target, radius_arrow):
    ((square_x, square_y), (square_width, square_height)) = target
    # Check if any of the line endpoints are inside the square
    if point_inside_square(x1, y1, target) or \
            point_inside_square(x2, y2,target):
        return True
    
    # Check if radius of circle intersects any of the square's sides
    new_nearest_point = calculate_nearest_point(x1, y1, square_x + square_width/2, square_y + square_height/2 , radius_arrow)

    if point_inside_square(new_nearest_point[0], new_nearest_point[1], target): # not jet tested TODO: TEST
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


def calculate_nearest_point(circle_x, cirle_y, point_x, point_y, r):
    """
    Calculates the nearest point on the circle to the point.
    

    Args:
        circle_x (_type_): _description_
        cirle_y (_type_): _description_
        point_x (_type_): _description_
        point_y (_type_): _description_
        r (_type_): _description_

    Returns:
        [x,y]: new point on the circle
    """
    
    point1 = [circle_x, cirle_y]
    point2 = [point_x, point_y]
    
    vector = np.array(point2) - np.array(point1)
    normalized_vector = vector / np.linalg.norm(vector)
    new_point = np.array(point1) + normalized_vector * r
    
    # Check if the distance between point1 and new_point is greater than the distance between point1 and point2
    if np.linalg.norm(new_point - np.array(point1)) > np.linalg.norm(vector):
        new_point = np.array(point2)
    
    return new_point.tolist()


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
