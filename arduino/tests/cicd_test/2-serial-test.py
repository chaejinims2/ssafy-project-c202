# 파이썬 배포 테스트
# 1.       /dev/video0 웹캠에서 프레임을 캡처하고 서버로 전송합니다.
# 2. (now) /dev/ttyACM0 시리얼 포트에서 데이터를 읽고 서버로 전송합니다.
# 3.       /dev/video0 웹캠에서 프레임을 캡처하고 /dev/ttyACM0 시리얼 포트에서 데이터를 읽어 서버로 전송합니다.
# 4.       mediapipe를 사용하여 웹캠에서 프레임을 캡처하고 서버로 전송합니다.

# -- requirements.txt
# requests
# opencv-python
# numpy
# mediapipe
# boto3
# pyserial
# ----------------------------------
#
# -- Dockerfile
# FROM python:3.8
# WORKDIR /app
# COPY . .
# RUN pip install -r requirements.txt
# CMD ["python", "main.py"]
#
# docker build -t your_image .
# docker run -it --device /dev/video0 --device=/dev/ttyS0 your_image
# ----------------------------------
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