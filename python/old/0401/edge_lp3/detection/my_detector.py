# my_detector.py
from scipy.spatial.transform import Rotation as R
from .algo_th import DetectorTH
from .algo_ai import DetectorAI
import time

class MyDetector:
    def __init__(self):
        self.initialize_thresholds()
        self.th = DetectorTH(self.threshold['TH'])
        self.ai = DetectorAI(self.threshold['AI'])
        self.prev_sleep_state = 0
        self.prev_event_state = 0

        self.initialize_data()

    def initialize_thresholds(self):
        self.threshold = {
            'AI': {
                'NON_SLEEP_TIME_TOLERANCE': 10,
                'NON_EVENT_TIME_TOLERANCE': 1,
                'NON_LOCATED_TOLERANCE': 3,
                'IS_EYE_CLOSED_THRESHOLD': 0.3,
                'IS_EVENT_FLAG': 0,
                'IS_LOCATED_FLAG': [5, 5],
                'EYE_INDICES': {'LEFT': [33, 160, 158, 133, 153, 144], 'RIGHT': [362, 385, 387, 263, 390, 374]},
                'BODY_INDICES' : {
                    'NOSE': 0,
                    'EYE' : {'LEFT': [1, 2, 3], 'RIGHT' : [4, 5, 6]},
                    'EAR': [7, 8],
                    'MOUTH': [9, 10],
                    'SHOULDER': [11, 12],
                    'ELBOW': [13, 14],
                    'WRIST': [15, 16],
                    'HANDS': {'LEFT': [17, 19, 21], 'RIGHT' : [18, 20, 22]},
                    'HIP': [23, 24],
                    'KNEE': [25, 26],
                    'ANKLE': [27, 28],
                    'HEEL': [29, 30],
                    'FOOT_INDEX': [31, 32]
                },
            },
            'TH': {    
                'ALERT_FALL': 9.81,
                'ALERT_FLIP': 1000,
            }
        }

    def initialize_data(self):
        self.data = {
            'index': None, 
            'event_type': None, 
            'detail': None, 
            'ser_data': None, 
            'frame': None, 
            'th': None, 
            'timestamp': None,
            'sleep_info': {'flag': 0, 'index': 0}, 
            'event_info': {'flag': 0, 'index': 0}, 
            'located_info': {'flag': 0, 'index': 0},
            'sleep_data': {'index': None, 'event_type': None, 'detail': None, 'time_data': None, 'timestamp': None, 'ser_data': None, 'frame': None, 'th': None},
            'event_data': {'index': None, 'event_type': None, 'detail': None, 'time_data': None, 'timestamp': None, 'ser_data': None, 'frame': None, 'th': None},
            'located_data': {'index': None, 'event_type': None, 'detail': None, 'time_data': None, 'timestamp': None, 'ser_data': None, 'frame': None, 'th': None},
        }


    def update_sleep_data(self, index, event_type, detail, timestamp):
        self.data['sleep_data'].update({
                'index': index,
                'event_type': event_type,
                'detail': detail,
                'timestamp': timestamp,
                'ser_data': self.data['ser_data'],
                'frame': self.data['frame'],
                'th': self.data['th']
            })
    def update_event_data(self, index, event_type, detail, timestamp):
        self.data['event_data'].update({
                'index': index,
                'event_type': event_type,
                'detail': detail,
                'timestamp': timestamp,
                'ser_data': self.data['ser_data'],
                'frame': self.data['frame'],
                'th': self.data['th']
            })


    def detect_start(self, timestamp, th_data, ser_data, image_data, frame_data):
        self.data.update({
            'ser_data': ser_data,
            'image_data': image_data,
            'frame': frame_data,
            'th': th_data,
            'timestamp': timestamp
        })


        self.update_info_flags_and_times()
        self.handle_sleep_statuses()
        self.handle_event_statuses()

        # time.sleep(0.1)

        return self.data

    def update_info_flags_and_times(self):
        info_types = ['sleep_info', 'event_info', 'located_info']
        methods = [self.ai.is_sleep, self.ai.is_event, self.ai.is_located]
        
        for info_type, method in zip(info_types, methods):
            self.data[info_type]['flag'], self.data[info_type]['index'] = method(self.data['image_data'])

    def handle_sleep_statuses(self):
        status = self.get_sleep_status()
        
        self.update_sleep_data(status['index'], status['event_type'], status['detail'], status['timestamp'])

        self.handle_status_update(status, 'sleep')


    def handle_event_statuses(self):
        status = self.get_event_status()
        self.update_event_data(status['index'], status['event_type'], status['detail'], status['timestamp'])

        self.handle_status_update(status, 'event')

    def get_sleep_status(self):
        
        if self.data['sleep_info']['flag'] and self.data['sleep_info']['index'] > self.threshold['AI']['NON_SLEEP_TIME_TOLERANCE']:
            return {'index': 2, 'event_type': 2, 'detail': 1, 'timestamp': self.data['timestamp'], 'just_message': 'just sleep!', 'ongoing_message': 'sleeping...'}
        else:
            return {'index': 2, 'event_type': 2, 'detail': 0, 'timestamp': self.data['timestamp'], 'just_message': 'just awake!', 'ongoing_message': 'awaking...'}

    def get_event_status(self):
        if self.data['event_info']['flag']:
            if self.data['event_info']['index'] == 1: # 사고
                return {'index': 2, 'event_type': 1, 'detail': 0, 'timestamp': self.data['timestamp'], 'just_message': 'just fell!', 'ongoing_message': 'dangerous!!'}
            else: # 행동
                return {'index': 2, 'event_type': 0, 'detail': self.data['event_info']['index'], 'timestamp': self.data['timestamp'], 'just_message': 'just event!', 'ongoing_message': 'evented!!'}
        else: 
            return {'index': 0, 'event_type': 0, 'detail': 0, 'timestamp': self.data['timestamp'], 'just_message': 'just doing nothing!', 'ongoing_message': 'doing nothing...'}
    def handle_status_update(self, status, status_type):
        
        prev_state = self.prev_sleep_state if status_type == 'sleep' else self.prev_event_state
        if status['detail'] != prev_state:
            if status_type == 'sleep':
                self.update_sleep_data(status['index'], status['event_type'], status['detail'], self.data['timestamp'])
            else:
                self.update_event_data(status['index'], status['event_type'], status['detail'], self.data['timestamp'])
            print(status['just_message'])
        else:
            print(status['ongoing_message'])

        if status_type == 'sleep':
            self.prev_sleep_state = status['detail']
        else:
            self.prev_event_state = status['detail']