import time
import serial
import re
import matplotlib.pyplot as plt
from collections import deque

# Open the serial port.
ser = serial.Serial('/dev/ttyACM0', 115200)  # Change '/dev/ttyACM0' to your serial port name

# Create a deque for storing data
data_gravity = deque(maxlen=1705)  # Adjust this value based on your sample rate
data_omegaSumAngle = deque(maxlen=1705)  # Adjust this value based on your sample rate

# Create a figure for plotting
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()

while True:
    line = ser.readline().decode('utf-8').strip()  # Read a line from the serial port
    print(line)
    if line:
        # Use regular expressions to parse the sensor values from the line.
        match = re.match(r'(.*) , (.*) , (.*) , (.*) , (.*) , (.*) , (.*)', line)

        if match:
            aX, aY, aZ, gX, gY, gZ, Tmp = map(float, match.groups())

            aX_g = aX / 32768.0 * 16
            aY_g = aY / 32768.0 * 16
            aZ_g = aZ / 32768.0 * 16
            gX_dps = gX / 32768.0 * 1000
            gY_dps = gY / 32768.0 * 1000
            gZ_dps = gZ / 32768.0 * 1000

            gravity = pow(aX_g*aX_g + aY_g*aY_g + aZ_g*aZ_g, 0.5)
            omegaSumAngle = pow(gX_dps*gX_dps + gY_dps*gY_dps + gZ_dps*gZ_dps, 0.5)

            ttt = Tmp/340.00+36.53
            print(f'gravity = {gravity} g, omegaSumAngle = {omegaSumAngle} °/s')

            # Add the new data to the deque
            data_gravity.append(gravity)
            data_omegaSumAngle.append(omegaSumAngle)

            # Update the plot
            ax.clear()
            ax.plot(data_gravity, label='gravity')
            ax.plot(data_omegaSumAngle, label='omegaSumAngle')
            ax.set_ylim([0, 30])  # Set y-axis limits
            ax.legend()  # Add a legend
            plt.draw()
            plt.pause(0.01)