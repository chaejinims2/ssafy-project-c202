from pyfirmata import Arduino, util
import time

# Establish a connection to the Arduino
board = Arduino('/dev/ttyACM0')

# Set up a digital pin for output
pin = board.get_pin('d:13:o')

# Main loop
while True:
    # Turn on the pin
    pin.write(1)
    time.sleep(0.5)

    # Turn off the pin
    pin.write(0)
    time.sleep(1)