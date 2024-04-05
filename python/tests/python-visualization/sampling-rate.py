import time
import serial
ser = serial.Serial('/dev/ttyACM0', 115200)  # Change '/dev/ttyACM0' to your serial port name
start_time = time.time()
count = 0

while time.time() - start_time < 1:
    line = ser.readline().decode('utf-8').strip()  # Read a line from the serial port
    if line:
        count += 1

print(f"Sample rate: {count} samples per second")