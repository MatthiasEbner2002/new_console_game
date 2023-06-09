import matplotlib.pyplot as plt
import numpy as np

class GolfShotSimulation:
    def __init__(self, initial_velocity, vertical_angle, horizontal_angle, initial_position, wind_speed, wind_angle):
        self.initial_velocity = initial_velocity
        self.vertical_angle = vertical_angle
        self.horizontal_angle = horizontal_angle
        self.initial_position = initial_position
        self.wind_speed = wind_speed
        self.wind_angle = wind_angle
        self.mass = 0.0459  # Mass of a golf ball (kg)

        self.positions = []
        self.positions_no_wind = []

    def simulate(self):
        # Constants
        g = 9.8  # Acceleration due to gravity (m/s^2)
        dt = 0.01  # Time step (s)

        force_x, force_y = self.calculate_force_components(self.wind_speed, self.wind_angle)
        # Convert angles to radians
        vertical_angle_rad = np.radians(self.vertical_angle)
        horizontal_angle_rad = np.radians(self.horizontal_angle)
        wind_angle_rad = np.radians(self.wind_angle)

        # Calculate initial velocity components
        initial_velocity_x = self.initial_velocity * np.cos(vertical_angle_rad) * np.cos(horizontal_angle_rad)
        initial_velocity_y = self.initial_velocity * np.cos(vertical_angle_rad) * np.sin(horizontal_angle_rad)
        initial_velocity_z = self.initial_velocity * np.sin(vertical_angle_rad)

        # Calculate wind velocity components
        wind_velocity_x = self.wind_speed * np.cos(wind_angle_rad)
        wind_velocity_y = self.wind_speed * np.sin(wind_angle_rad)
        wind_velocity_z = 0  # Assuming wind does not affect the vertical component of the ball's motion

        # Simulate the golf shot
        time = 0
        while True:
            position = [
                self.initial_position[0] + (initial_velocity_x + wind_velocity_x) * time,
                self.initial_position[1] + (initial_velocity_y + wind_velocity_y) * time,
                self.initial_position[2] + (initial_velocity_z + wind_velocity_z) * time - 0.5 * g * time ** 2 * self.mass  
                #self.initial_position[0] + (initial_velocity_x) * time + 0.5 * force_x / self.mass * time**2,
                #self.initial_position[1] + (initial_velocity_y) * time + 0.5 * force_y / self.mass * time**2,
                #self.initial_position[2] + (initial_velocity_z) * time - 0.5 * g * time ** 2 * self.mass  
            ]
            if position[2] < 0:
                break
            self.positions.append(position)
            time += dt

        # Show the plot
        plt.show()



    def simulate_without_wind(self):
        # Constants
        g = 9.8  # Acceleration due to gravity (m/s^2)
        dt = 0.01  # Time step (s)

        # Convert angles to radians
        vertical_angle_rad = np.radians(self.vertical_angle)
        horizontal_angle_rad = np.radians(self.horizontal_angle)

        # Calculate initial velocity components
        initial_velocity_x = self.initial_velocity * np.cos(vertical_angle_rad) * np.cos(horizontal_angle_rad)
        initial_velocity_y = self.initial_velocity * np.cos(vertical_angle_rad) * np.sin(horizontal_angle_rad)
        initial_velocity_z = self.initial_velocity * np.sin(vertical_angle_rad)

        # Simulate the golf shot without wind
        time = 0
        while True:
            position = [
                self.initial_position[0] + initial_velocity_x * time,
                self.initial_position[1] + initial_velocity_y * time,
                self.initial_position[2] + initial_velocity_z * time - 0.5 * g * time ** 2 * self.mass
            ]
            if position[2] < 0:
                break
            self.positions_no_wind.append(position)
            time += dt
    
    def calculate_force_components(self, wind_speed, wind_direction):
        # Convert wind direction from degrees to radians
        wind_direction_rad = np.radians(wind_direction)

        # Calculate the force components
        force_x = wind_speed * np.cos(wind_direction_rad)
        force_y = wind_speed * np.sin(wind_direction_rad)

        return force_x, force_y


    
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

        # Calculate the maximum range among x, y, and z coordinates
        max_range = max(max(abs(max(x_coords)), abs(min(x_coords))),
                        max(abs(max(y_coords)), abs(min(y_coords))),
                        max(abs(max(z_coords)), abs(min(z_coords))))

        # Set limits of the x, y, and z axes
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

        # Show the plot
        plt.show()
        
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
        max_range = max(max(x_coords), max(y_coords), max(x_coords_no_wind), max(y_coords_no_wind))

        # Set limits of the x and y axes with respect to the origin
        plt.xlim(-max_range / 2, max_range / 2)
        plt.ylim(-max_range / 2, max_range / 2)

        # Add a red line for the wind direction
        wind_direction = np.deg2rad(self.wind_angle)
        wind_length = max_range / 4  # Length of the wind line
        x_start = 0  # Start position of the wind line
        y_start = 0  # Start position of the wind line
        x_end = x_start + wind_length * np.sin(wind_direction)
        y_end = y_start + wind_length * np.cos(wind_direction)
        plt.arrow(x_start, y_start, x_end - x_start, y_end - y_start,
                head_width=max_range / 20, head_length=max_range / 15, fc='red', ec='red')

        # Set labels and title
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Top-Down View of Golf Shot')

        # Show the legend
        plt.legend()

        # Show the plot
        plt.show()

    def visualize_x_z(self):
        # Extract x and z coordinates from the positions list
        x_coords, _, z_coords = zip(*self.positions)
        x_coords_no_wind, _, z_coords_no_wind = zip(*self.positions_no_wind)  # Positions without wind

        # Create a 2D plot for the x-z plane
        plt.figure()

        # Plot the trajectory of the golf shot with wind
        plt.plot(x_coords, z_coords, label='With Wind')

        # Plot the trajectory of the golf shot without wind
        plt.plot(x_coords_no_wind, z_coords_no_wind, label='Without Wind')

        # Calculate the maximum range among x and z coordinates
        max_range = max(max(abs(max(x_coords)), abs(min(x_coords))),
                        max(abs(max(z_coords)), abs(min(z_coords))),
                        max(abs(max(x_coords_no_wind)), abs(min(x_coords_no_wind))),
                        max(abs(max(z_coords_no_wind)), abs(min(z_coords_no_wind))))

        # Set limits of the x and z axes with respect to the origin
        plt.xlim(-max_range, max_range)
        plt.ylim(-max_range, max_range)

        # Set aspect ratio to 'equal'
        plt.gca().set_aspect('equal', adjustable='box')

        # Set labels and title
        plt.xlabel('X')
        plt.ylabel('Z')
        plt.title('Trajectory of Golf Shot in X-Z Plane')

        # Show the legend
        plt.legend()

        # Show the plot
        plt.show()

    def visualize_y_z(self):
        # Extract y and z coordinates from the positions list
        _, y_coords, z_coords = zip(*self.positions)
        _, y_coords_no_wind, z_coords_no_wind = zip(*self.positions_no_wind)  # Positions without wind

        # Create a 2D plot for the y-z plane
        plt.figure()

        # Plot the trajectory of the golf shot with wind
        plt.plot(y_coords, z_coords, label='With Wind')

        # Plot the trajectory of the golf shot without wind
        plt.plot(y_coords_no_wind, z_coords_no_wind, label='Without Wind')

        # Calculate the maximum range among y and z coordinates
        max_range = max(max(abs(max(y_coords)), abs(min(y_coords))),
                        max(abs(max(z_coords)), abs(min(z_coords))),
                        max(abs(max(y_coords_no_wind)), abs(min(y_coords_no_wind))),
                        max(abs(max(z_coords_no_wind)), abs(min(z_coords_no_wind))))

        # Set limits of the y and z axes with respect to the origin
        plt.xlim(-max_range, max_range)
        plt.ylim(-max_range, max_range)

        # Set aspect ratio to 'equal'
        plt.gca().set_aspect('equal', adjustable='box')

        # Set labels and title
        plt.xlabel('Y')
        plt.ylabel('Z')
        plt.title('Trajectory of Golf Shot in Y-Z Plane')

        # Show the legend
        plt.legend()

        # Show the plot
        plt.show()



    def visualize_2d_plots(self):
        # Extract x, y, and z coordinates from the positions list
        x_coords, y_coords, z_coords = zip(*self.positions)
        x_coords_no_wind, y_coords_no_wind, z_coords_no_wind = zip(*self.positions_no_wind)

        # Create subplots for X-Z, Y-Z, and Top-Down views
        fig, axs = plt.subplots(1, 3, figsize=(15, 5))

        # X-Z plane plot
        axs[0].plot(x_coords, z_coords, label='With Wind')
        axs[0].plot(x_coords_no_wind, z_coords_no_wind, label='Without Wind')
        axs[0].set_xlabel('X')
        axs[0].set_ylabel('Z')
        axs[0].set_title('X-Z Plane')
        axs[0].legend()

        # Y-Z plane plot
        axs[1].plot(y_coords, z_coords, label='With Wind')
        axs[1].plot(y_coords_no_wind, z_coords_no_wind, label='Without Wind')
        axs[1].set_xlabel('Y')
        axs[1].set_ylabel('Z')
        axs[1].set_title('Y-Z Plane')
        axs[1].legend()

        # Top-Down view plot
        axs[2].plot(x_coords, y_coords, label='With Wind')
        axs[2].plot(x_coords_no_wind, y_coords_no_wind, label='Without Wind')
        axs[2].set_xlabel('X')
        axs[2].set_ylabel('Y')
        axs[2].set_title('Top-Down View')
        axs[2].legend()

        # Adjust spacing between subplots
        plt.subplots_adjust(wspace=0.3)

        # Show the plot
        plt.show()


def main():
    # Initial conditions
    initial_velocity = 50
    vertical_angle = 45
    horizontal_angle = 90
    initial_position = [0, 0, 0]
    wind_speed = 10
    wind_angle = 170

    # Create a GolfShotSimulation instance
    simulation = GolfShotSimulation(
        initial_velocity, vertical_angle, horizontal_angle, initial_position, wind_speed, wind_angle
    )

    # Simulate the golf shot
    simulation.simulate()
    simulation.simulate_without_wind()

    # Visualize the 2D plots
    simulation.visualize_2d_plots()
    
    # Visualize the golf shot in 3D
    simulation.visualize_3d()
    
    simulation.visualize_top_down()

if __name__ == '__main__':
    main()