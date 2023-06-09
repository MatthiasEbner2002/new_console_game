import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def calculate_trajectory(v_initial, launch_angle, spin_rate, time_step):
    # Constants
    g = 9.8  # Gravitational acceleration

    # Convert launch angle to radians
    launch_angle_rad = math.radians(launch_angle)

    # Initialize variables
    time = 0
    x = [0]
    y = [0]
    z = [0]
    vx = v_initial * math.cos(launch_angle_rad)
    vy = v_initial * math.sin(launch_angle_rad)
    vz = 0

    while y[-1] >= 0:
        # Update time
        time += time_step

        # Calculate forces
        fd = calculate_drag_force(vx, vy, vz)
        fl = calculate_lift_force(spin_rate, vx, vy, vz)

        # Calculate accelerations
        ax = fd * vx
        ay = -g + fd * vy + fl
        az = fd * vz

        # Update velocities
        vx += ax * time_step
        vy += ay * time_step
        vz += az * time_step

        # Update positions
        x.append(x[-1] + vx * time_step)
        y.append(y[-1] + vy * time_step)
        z.append(z[-1] + vz * time_step)

    return x, y, z

def calculate_drag_force(vx, vy, vz):
    # Drag coefficient (example value, adjust as needed)
    cd = 0.3

    # Calculate speed
    speed = math.sqrt(vx ** 2 + vy ** 2 + vz ** 2)

    # Calculate drag force
    fd = -0.5 * cd * speed

    return fd

def calculate_lift_force(spin_rate, vx, vy, vz):
    # Calculate lift force
    fl = (spin_rate * math.pi * vx * vy) / 60

    return fl

# Simulation parameters
v_initial = 50  # Initial velocity (m/s)
launch_angle = 45  # Launch angle (degrees)
spin_rate = 3000  # Spin rate (rpm)
time_step = 0.01  # Time step (s)

# Calculate trajectory
x, y, z = calculate_trajectory(v_initial, launch_angle, spin_rate, time_step)

# Plot trajectory
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z)
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')
plt.show()
x