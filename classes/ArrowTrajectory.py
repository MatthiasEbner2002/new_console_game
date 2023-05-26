import math
import time

class ArrowTrajectory:
    def __init__(self, start_location, start_power, angle, gravity, time_interval):
        self.start_location = start_location
        self.start_power = start_power
        self.angle = angle
        self.gravity = gravity
        self.time_interval = time_interval
        self.time_of_flight = (2 * start_power * math.sin(math.radians(angle))) / gravity
        self.step_size = time_interval * start_power * math.cos(math.radians(angle))
        self.current_time = 0
        self.current_x = start_location[0]
        self.current_y = start_location[1]
    
    def calculate_new_step(self):
        if self.current_time <= self.time_of_flight:
            self.current_y = self.start_location[1] + (self.start_power * math.sin(math.radians(self.angle)) * self.current_time) - (0.5 * self.gravity * self.current_time ** 2)
            self.current_x = self.start_location[0] + self.step_size * self.current_time / self.time_interval
            self.current_time += self.time_interval
            return (self.current_x, self.current_y)
        else:
            return None

    def calculate_trajectory(self):
        while True:
            step = self.calculate_new_step()
            if step is None:
                break
            direction = math.degrees(math.atan2(self.start_power * math.sin(math.radians(self.angle)) - (self.gravity * self.current_time), self.start_power * math.cos(math.radians(self.angle))))
            self.render_arrow_position(step, direction)
            time.sleep(self.time_interval)

    def render_arrow_position(self, position, direction):
        # Custom rendering function to display or store the arrow position and direction
        print("Arrow Position:", position)
        print("Arrow Direction:", direction)
        

# Example usage
start_location = (0, 0)  # Starting location of the arrow
start_power = 30  # Initial power of the arrow
angle = 45  # Launch angle in degrees
gravity = 9.8  # Acceleration due to gravity
time_interval = 0.1  # Time interval between each render (in seconds)

trajectory = ArrowTrajectory(start_location, start_power, angle, gravity, time_interval)
trajectory.calculate_trajectory()
