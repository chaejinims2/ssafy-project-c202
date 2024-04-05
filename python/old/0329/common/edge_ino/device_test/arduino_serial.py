import serial
import time

# Open the serial port
ser = serial.Serial('/dev/ttyACM0', 115200)  # Change to the port that your Arduino is connected to

# Main loop
while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)
    else: 
        print("no data")