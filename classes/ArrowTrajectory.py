import math

class ArrowTrajectory:
    def __init__(self, start_location, start_power, angle, gravity):
        self.start_location = start_location                            # start_location: Tuple[float, float]
        self.start_power = start_power                                  # start_power: int
        self.angle = angle                                              # angle: int
        self.gravity = gravity                                          # gravity: float
        self.current_time = 0                                           # current_time: float
        self.arrows = ['→','↗', '↑', '↖', '←', '↙', '↓', '↘']           # arrows: List[str] list of all arrows
        
        self.actual_step = self.start_location
        self.old_step = None
    
    def calculate_step(self):
        """
        Calculates the next step of the arrow's trajectory.
        There is a time interval of 0.02 seconds between each step.

        Returns:
            Tuple[float, float, float, str]: (x, y, direction, arrow)
        """
        self.old_step = self.actual_step        # safe the old step, so we can set the arrow position back to the old step if the arrow is out of bounds 
        time_interval = 0.02                    # then time_interval for calculating the steps
        current_time = self.current_time
        x: float = self.start_location[0] + self.start_power * math.cos(math.radians(self.angle)) * current_time
        y: float = self.start_location[1] + (self.start_power * math.sin(math.radians(self.angle)) * current_time) - (0.5 * self.gravity * current_time ** 2)
        direction = math.degrees(math.atan2(self.start_power * math.sin(math.radians(self.angle)) - (self.gravity * current_time), self.start_power * math.cos(math.radians(self.angle))))
        self.current_time += time_interval
        arrow: str = self.get_arrow_direction(direction)

        ret =  (y, x, direction, arrow)
        self.actual_step = ret              # safe the step 
        return ret
    
    def get_arrow_direction(self, angle):
        """
        Returns the arrow that corresponds to the given angle.
        Args:
            angle (int): Angle in degrees
        Returns:
            str: Arrow that corresponds to the given angle
        """
        
        normalized_angle = angle % 360
        index = round(normalized_angle / 45) % 8
        return self.arrows[index]
    
    
    
"""

# Example usage

start_location = (0, 0)  # Starting location of the arrow
start_power = 30  # Initial power of the arrow
angle = 45  # Launch angle in degrees
gravity = 9.8  # Acceleration due to gravity

trajectory = ArrowTrajectory(start_location, start_power, angle, gravity)

# Calculate a new step of the arrow's position and angle
while True:
    step = trajectory.calculate_step()
    if step[0] < 0:
        break
    print("Arrow Position:", step[:2])
    print("Arrow Direction:", step[2])

"""
