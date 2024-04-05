# my_detector.py
from scipy.spatial.transform import Rotation as R
from .algo_th import DetectorTH
from .algo_ai import DetectorAI
import time

SLEEP_ESTIMATION_THRESHOLD = 2
SLEEP_EAR_THRESHOLD = 0.3

class MyDetector:
    def __init__(self):
        self.treshold = {
            'AI': {
                'SLEEP_ESTIMATION_THRESHOLD': 2, # 시간 
                'SLEEP_EAR_THRESHOLD': 0.3, # 눈 감김 여부
                'EYE_INDICES': {
                    'LEFT': [33, 160, 158, 133, 153, 144],
                    'RIGHT': [362, 385, 387, 263, 390, 374]
                },
                'EVENT_ETTIMATION_THRESHOLD': 5, # 시간
                'EVENT_EAR_THRESHOLD': 0.3, # 눈 감김 여부
                'BODY_INDICES' : {
                    'NOSE': [0],
                    'EYE' : {
                        'INNER': [1, 4],
                        'MID' : [2, 5],                 
                        'OUTER': [3, 6]
                    },
                    'EAR': [7, 8],
                    'MOUTH': [9, 10],
                    'SHOULDER': [11, 12],
                    'ELBOW': [13, 14],
                    'WRIST': [15, 16],
                    'HANDS': {
                        'PINKY': [17, 18],
                        'INDEX': [19, 20],
                        'THUMB': [21, 22],
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

        self.detector = {
            'AI': DetectorAI(self.treshold['AI']),
            'TH': DetectorTH(self.treshold['TH'])
        }



    def detect_start(self, ser_data, image_data):

        is_eye_closed_ai, sleep_time_ai = self.detector['AI'].is_sleep(image_data)
        is_moving_th, event_flag_th = self.detector['TH'].is_event(ser_data)
        is_moving_ai, event_flag_ai = self.detector['AI'].is_event(image_data)
        time.sleep(0.1)

        if is_eye_closed_ai:
            if sleep_time_ai > self.treshold_ai['SLEEP_ESTIMATION_THRESHOLD']:
                print(f"The eyes are closed for {sleep_time_ai} seconds. This is considered as sleep.")
            else:
                print(".", sleep_time_ai)
        if is_moving_th: # The eyes are open
            print("TH_event_flag", event_flag_th)

        if is_moving_ai: # The eyes are open
            print("AI_event_flag", event_flag_ai)
        
        


      



