# cam
# audio
# serial - sensor data
#
# my_sensor.py
import cv2
import sys
import re
import serial as pyserial
import pyaudio
from io import BytesIO
import audioop
import math
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
        self.p = self.sound_open()  # Open sound device

        # self.cam_data
        ret = 1
        self.cam_data = 1
        self.ser_data = SensorData2(0, 0)

        self.prev_data = None
        self.prev_ser = None
        self.data = {
            'image_data' : ['image.jpg', 1, 'image/jpeg'],
            'form_data' : {'line': SensorData2(0, 0), 'baby_id': 1},
            'time_data' : {'timestamp': 1, 'datetime': '2021-03-25 12:00:00.000000'},
            'aud':1,
            'ser': SensorData(0, 0, 0, 0, 0, 0, 0, 0, 0)

        }

        # self.audio_data
        self.line = '111'

        # Initialize data window for sliding window processing
        self.window_size = 30
        self.data_window = deque(maxlen=self.window_size)
        
    def get(self):
        # Capture frame, get data, preprocess data, process data window, get sound
        self.frame_capture()
        self.data['image_data'][1] = self.frame_encode()
        self.data['ser'] = self.data_get()
        self.data['form_data']['line'] = self.prev_data
        # print('온습도', self.data['form_data']['line'])

    def data_get(self):
        if self.ser.in_waiting > 0:
            self.line = self.ser.readline().decode('utf-8').rstrip()
            if self.line:
                match = re.match(r'(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*),(.*)', self.line)     

                if match:
                    # print("matched")
                    self.data_window.append(map(float, match.groups()))   # Add data to the window
                    self.prev_data = SensorData2(match.group(8), match.group(9)) # 온도 (8), 습도 (9)
                    self.prev_ser = SensorData(*map(float, match.groups()))  # Add data to the window
        return self.prev_ser
    
    def webcam_open(self):
        try:
            return cv2.VideoCapture(0)
        except Exception as e:
            print(f'Cannot open the webcam: {e}')
            sys.exit(1)

    def frame_capture(self):
        self.ret, self.frame = self.cam.read()
        self.data['time_data']['datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        self.data['time_data']['timestamp'] = time.time()
        print(self.data['time_data']['timestamp'] )

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

    def sound_open(self):
        try:
            return pyaudio.PyAudio()
        except Exception as e:
            print(f'Cannot open the sound device: {e}')
            return None

    def sound_get(self):
        chunk = 1024
        sample_format = pyaudio.paInt16
        channels = 1
        fs = 44100
        stream = self.p.open(format=sample_format, channels=channels, rate=fs, frames_per_buffer=chunk, input=True)
        data = stream.read(chunk)
        self.p = 20 * math.log10(audioop.rms(data, 2))

    def sound_close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        
    def serial_connect(self):
        try:
            print("Connecting to serial...")
            return pyserial.Serial('/dev/ttyACM0', 115200)
        except pyserial.SerialException:
            print("Cannot start serial communication.")
            return None



    def process_data_window(self):
        print("Processing data window:", self.data_window)

    def data_features(self):
        self.features = [self.f1, self.f2, self.rtn]


    def data_preprocess(self):
        self.f1 = (self.data.aX**2 + self.data.aY**2 + self.data.aZ**2)**0.5
        self.f2 = (self.data.gX**2 + self.data.gY**2 + self.data.gZ**2)**0.5

    def __del__(self):
        self.webcam_release()
        if self.ser:
            self.ser.close()