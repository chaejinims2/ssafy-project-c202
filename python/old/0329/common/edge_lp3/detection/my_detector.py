# my_detector.py
from scipy.spatial.transform import Rotation as R
from .algo_th import DetectorTH
from .algo_ai import DetectorAI
import time
import datetime

class MyDetector:
    def __init__(self):

        self.treshold = {
            'AI': {
                'NON_SLEEP_TIME_TOLERANCE': 10, #  비수면 시간 허용 오차
                'NON_EVENT_TIME_TOLERANCE': 5, #  동작 감지 시간 허용 오차
                'NON_LOCATED_TOLERANCE': 3, #  적정 위치 좌표 허용 오차
                'IS_EYE_CLOSED_THRESHOLD': 0.3, # 눈 감김 여부
                'IS_EVENT_FLAG': 0, # 동작의 종류
                'IS_LOCATED_FLAG': [5, 5], # 위치
                'EYE_INDICES': {
                    'LEFT': [33, 160, 158, 133, 153, 144],
                    'RIGHT': [362, 385, 387, 263, 390, 374]
                },
                'BODY_INDICES' : {
                    'NOSE': 0,
                    'EYE' : {
                        'LEFT': [1, 2, 3],
                        'RIGHT' : [4, 5, 6]
                    },
                    'EAR': [7, 8],
                    'MOUTH': [9, 10],
                    'SHOULDER': [11, 12],
                    'ELBOW': [13, 14],
                    'WRIST': [15, 16],
                    'HANDS': {
                        'LEFT': [17, 19, 21],
                        'RIGHT' : [18, 20, 22]
                    },
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
        
        self.th = DetectorTH(self.treshold['TH'])
        self.ai = DetectorAI(self.treshold['AI'])
        self.prev_state = "awake"
        self.data = {
            'ser_data': None,
            'frame': None,
            'time_data': None,
            'timestamp': None,
            'is_eye_closed_ai': None,
            'sleep_time_ai': None,
            'is_event_flag_ai': None,
            'event_flag_ai': None,
            'is_located_flag_ai': None,
            'located_flag_ai': None,
            'th': None,
        }

    def send_notification(self):
        self.my_edge['network_manager'].send_event_to_server(self.data)

    def send_event_notification(self):
        if self.data['is_event_flag_ai'] != 0:
            return True
            if self.data['is_located_flag_ai']:
                return True
        # print("no event detected")
        return False


    def send_sleep_status_notification(self):
        current_time = datetime.datetime.now()
        is_sleeping = self.data['is_eye_closed_ai'] and self.data['sleep_time_ai'] > self.treshold['AI']['NON_SLEEP_TIME_TOLERANCE']

        if is_sleeping:
            if self.prev_state == "awake":
                status_message = "just sleep!"
            else:
                status_message = "sleeping..."
            self.prev_state = "sleep"
        else:
            if self.prev_state == "sleep":
                status_message = "just awake!"
            else:
                status_message = "awaking..."
            self.prev_state = "awake"

        print(f"{current_time}: {status_message}")
        return is_sleeping
    
    def detect_start(self, ser_data, image_data):
        self.data['is_eye_closed_ai'], self.data['sleep_time_ai'] = self.ai.is_sleep(image_data)
        self.data['is_event_flag_ai'], self.data['event_flag_ai'] = self.ai.is_event(image_data)
        self.data['is_located_flag_ai'], self.data['located_flag_ai'] = self.ai.is_located(image_data)
        time.sleep(0.1)

        return self.send_event_notification(), self.send_sleep_status_notification(), self.data