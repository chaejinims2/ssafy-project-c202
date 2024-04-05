import cv2
import sys
import re
import serial as pyserial
from io import BytesIO
from collections import deque, namedtuple
from datetime import datetime
import time

# Namedtuples for sensor and feature data
SensorData = namedtuple('SensorData', ['aX', 'aY', 'aZ', 'gX', 'gY', 'gZ', 'Tmp', 'dh', 'dt'])
SensorData2 = namedtuple('SensorData', ['dh', 'dt'])
FeatureData = namedtuple('FeatureData', ['f1', 'f2', 'rtn'])

class MySensor:
    def __init__(self):
        self.cam = self.webcam_open()  # Open webcam
        self.ser = self.serial_connect()  # Connect to serial
        self.initialize_data()

    def initialize_data(self):
        self.cam_data = 1
        self.ser_data = SensorData2(0, 0)
        self.prev_data = SensorData2(0, 0)
        self.prev_ser = SensorData(0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.data = {
            'index': None,
            'event_type': None,
            'detail': None,
            'frame' : ['image.jpg', 1],
            'th': [0, 0],
            'form_data' : {'line': SensorData2(0, 0), 'baby_id': 1},
            'time_data': '2021-03-25 12:00:00.000000',
            'timestamp': 1711873161.4333634,
        
            'aud':1,
            'ser_data': SensorData(0, 0, 0, 0, 0, 0, 0, 0, 0),
            'image_data' : 1
        }
        self.line = '111'

    def get(self):
        self.frame_capture()
        self.data['frame'][1] = self.frame_encode()
        # print(self.data['frame'][1])
        self.data['ser_data'] = self.data_get()
        self.data['form_data']['line'] = self.prev_data
        self.data['th'][0], self.data['th'][1] = self.prev_data[0], self.prev_data[1]
        # print(self.prev_data)
        self.data['image_data'] = self.frame

        # print(self.data['image_data'][1])
        # print(self.data['form_data'])
        # print(self.data['ser_data'])

    def data_get(self):
        if self.ser.in_waiting > 0:
            self.line = self.ser.readline().decode('utf-8').rstrip()
            # print(self.line)
            if self.line:
                try:
                    match = re.match(r'(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*)', self.line)

                    if match:
                        self.prev_data = SensorData2(match.group(8), match.group(9)) # 온도 (8), 습도 (9)
                        self.prev_ser = SensorData(*map(float, match.groups()))  # Add data to the window
                except ValueError:
                    print("Missing data, using previous data.")
        return self.prev_ser

    def webcam_open(self):
        try:
            print("Opening webcam...")
            return cv2.VideoCapture(0)
        except Exception as e:
            print(f'Cannot open the webcam: {e}')
            sys.exit(1)

    def frame_capture(self):
        self.ret, self.frame = self.cam.read()
        # print("ddddd",self.frame)
        self.data['time_data'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        self.data['timestamp'] = time.time()

    def frame_encode(self):
        try:
            _, self.jpeg = cv2.imencode('.jpg', self.frame)
            return BytesIO(self.jpeg.tobytes())
        except Exception as e:
            print(f'Cannot encode the frame: {e}')
            return None

    def webcam_release(self):
        self.cam.release()
        cv2.destroyAllWindows()

    def serial_connect(self):
        try:
            print("Connecting to serial...")
            return pyserial.Serial('/dev/ttyACM0', 115200)
        except pyserial.SerialException:
            print("Cannot start serial communication.")
            return None



    def __del__(self):
        self.webcam_release()
        if self.ser:
            self.ser.close()