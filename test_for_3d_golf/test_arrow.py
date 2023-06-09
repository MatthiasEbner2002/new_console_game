import matplotlib.pyplot as plt
from ArrowTrajectory import ArrowTrajectory
start_location = (0, 0)  # Starting location of the arrow
start_power = 30  # Initial power of the arrow
angle = 45  # Launch angle in degrees
gravity = 9.8  # Acceleration due to gravity

trajectory = ArrowTrajectory(start_location, start_power, angle, gravity)

x_values = []  # X-coordinate values
y_values = []  # Y-coordinate values

# Calculate the trajectory and collect position data
while True:
    step = trajectory.calculate_step()
    if step[0] < 0:
        break
    x_values.append(step[1])
    y_values.append(step[0])

# Plot the trajectory
plt.plot(x_values, y_values)
plt.xlabel('X-coordinate')
plt.ylabel('Y-coordinate')
plt.title('Arrow Trajectory')
plt.grid(True)
plt.show()
