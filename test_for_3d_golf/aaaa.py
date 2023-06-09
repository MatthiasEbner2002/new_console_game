import matplotlib.pyplot as plt
import numpy as np


class GolfSimulator:
    def __init__(self, initial_position, initial_velocity, mass, drag_coefficient, wind_speed, wind_angle, time_step):
        self.initial_position = np.array(initial_position)
        self.initial_velocity = np.array(initial_velocity)
        self.mass = mass
        self.drag_coefficient = drag_coefficient
        self.wind_speed = wind_speed
        self.wind_angle = wind_angle
        self.time_step = time_step
        self.positions = []
        self.positions_no_wind = []

    def simulate(self):
        position = self.initial_position
        velocity = self.initial_velocity

        while position[2] > 0:
            self.positions.append(position.copy())

            # Calculate the acceleration
            drag_force = -0.5 * self.drag_coefficient * self.wind_speed * velocity
            gravity_force = np.array([0, 0, -9.8 * self.mass])
            acceleration = (drag_force + gravity_force) / self.mass

            # Update the position and velocity using Euler's method
            position += velocity * self.time_step
            velocity += acceleration * self.time_step

            # Update the wind speed and angle
            self.wind_speed -= self.wind_speed * 0.01  # Decrease the wind speed over time

            # Update the position based on the wind
            wind_direction = np.radians(self.wind_angle)
            wind_effect = self.wind_speed * np.array([np.cos(wind_direction), np.sin(wind_direction), 0])
            position += wind_effect * self.time_step

        self.positions.append(position)

    def simulate_without_wind(self):
        position = self.initial_position
        velocity = self.initial_velocity

        while position[2] > 0:
            self.positions_no_wind.append(position.copy())

            # Calculate the acceleration without considering wind
            gravity_force = np.array([0, 0, -9.8 * self.mass])
            acceleration = gravity_force / self.mass

            # Update the position and velocity using Euler's method
            position += velocity * self.time_step
            velocity += acceleration * self.time_step

        self.positions_no_wind.append(position)

    def visualize_top_down(self):
        # Extract x and y coordinates from the positions list
        x_coords, y_coords, _ = zip(*self.positions)
        x_coords_no_wind, y_coords_no_wind, _ = zip(*self.positions_no_wind)  # Positions without wind

        # Create a top-down view plot
        plt.figure()

        # Plot the trajectory of the golf shot with wind
        plt.plot(x_coords, y_coords, label='With Wind')

        # Plot the trajectory of the golf shot without wind
        plt.plot(x_coords_no_wind, y_coords_no_wind, label='Without Wind')

        # Set aspect ratio to 'equal'
        plt.gca().set_aspect('equal', adjustable='box')

        # Calculate the maximum range among x and y coordinates
        max_range = max(max(x_coords), max(y_coords))

        # Set limits of the x and y axes with respect to the origin
        plt.xlim(-max_range / 2, max_range / 2)
        plt.ylim(-max_range / 2, max_range / 2)

        # Add a legend
        plt.legend()

        # Set labels and title
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Top-Down View of Golf Shot')

        # Show the plot
        plt.show()
    
    def visualize_3d(self):
        # Extract x, y, and z coordinates from the positions list
        x_coords, y_coords, z_coords = zip(*self.positions)
        x_coords_no_wind, y_coords_no_wind, z_coords_no_wind = zip(*self.positions_no_wind)  # Positions without wind

        # Create a 3D plot
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Plot the trajectory of the golf shot with wind
        ax.plot(x_coords, y_coords, z_coords, label='With Wind')

        # Plot the trajectory of the golf shot without wind
        ax.plot(x_coords_no_wind, y_coords_no_wind, z_coords_no_wind, label='Without Wind')

        # Combine all coordinates to find the maximum range
        all_coords = x_coords + y_coords + z_coords + x_coords_no_wind + y_coords_no_wind + z_coords_no_wind

        # Calculate the maximum range among all coordinates
        max_range = max(all_coords)

        # Set limits of the x, y, and z axes with respect to the origin
        ax.set_xlim3d(-max_range, max_range)
        ax.set_ylim3d(-max_range, max_range)
        ax.set_zlim3d(0, max_range)

        # Set the view perspective to center the origin
        ax.view_init(elev=30, azim=45)

        # Set labels and title
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Golf Shot Simulation')

        # Show the legend
        ax.legend()

        # Set equal aspect ratio
        ax.set_box_aspect([1, 1, 1])

        # Show the plot
        plt.show()

        
def main():
    initial_position = [0, 0, 0]
    initial_velocity = [50, 0, 50]
    mass = 0.045
    drag_coefficient = 0.25
    wind_speed = 20
    wind_angle = 45
    time_step = 0.01
    simulator = GolfSimulator(initial_position, initial_velocity, mass, drag_coefficient, wind_speed, wind_angle,
                          time_step)
    simulator.simulate()
    simulator.simulate_without_wind()
    simulator.visualize_3d()
    simulator.visualize_top_down()
    
    
if __name__ == '__main__':
    main()