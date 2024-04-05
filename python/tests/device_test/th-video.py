# 1. 웹캠에서 프레임을 캡처하고, 이를 JPEG 형식으로 인코딩하여 서버로 보내는 작업을 반복
# 2. 시리얼 포트에서 데이터를 읽어 서버로 보내는 작업도 함께 수행
# 3. 각 요청의 지연 시간을 측정하고 출력
# 4. 'q' 키를 누르면 루프에서 빠져나와 웹캠을 닫기

import cv2
import requests
import numpy as np
from io import BytesIO
import time
import serial

# Initialize webcam
webcam = cv2.VideoCapture(0)
print('Webcam is opened.')

# Initialize serial communication
serial_port = serial.Serial('/dev/ttyACM0', 9600)  # Change to the port that your Arduino is connected to
print('Serial communication is started.')

# Check if webcam is opened
if not webcam.isOpened():
    print('Cannot open the webcam.')
    exit()

while True:
    # Capture frame from webcam
    ret, frame = webcam.read()

    # Encode the frame into JPEG format
    _, jpeg = cv2.imencode('.jpg', frame)
    jpeg_bytes = jpeg.tobytes()
    jpeg_file = BytesIO(jpeg_bytes)

    # Initialize time for measuring the delay
    start_time = time.time() * 1000
    end_time = time.time() * 1000

    # Initialize line data
    line_data = ''

    # Read line data from serial port
    if serial_port.in_waiting > 0:
        line_data = serial_port.readline().decode('utf-8').rstrip()

    # Send POST request to the server
    try:
        response = requests.post('http://192.168.100.58:3001/data', files={'image': ('image.jpg', jpeg_file, 'image/jpeg')}, data={'line': line_data})
        # Print the response
        # print(response.text)
        end_time = time.time() * 1000
        print('time: ', round(end_time - start_time, 3), '(ms)')
        start_time = end_time

    except requests.exceptions.RequestException as e:
        print(e)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam
webcam.release()
cv2.destroyAllWindows()