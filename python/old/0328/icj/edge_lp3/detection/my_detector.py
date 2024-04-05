# my_detector.py
from scipy.spatial.transform import Rotation as R
from .algo_th import DetectorTH
from .algo_ai import DetectorAI
import time

SLEEP_ESTIMATION_THRESHOLD = 2
SLEEP_EAR_THRESHOLD = 0.3

class MyDetector:
    def __init__(self):
        self.treshold_ai = {
            'SLEEP_ESTIMATION_THRESHOLD': 2,
            'SLEEP_EAR_THRESHOLD': 0.3,
            'EYE_INDICES': {
                'LEFT': [33, 160, 158, 133, 153, 144],
                'RIGHT': [362, 385, 387, 263, 390, 374]
            }
        }
        self.treshold_th = {    
            'ALERT_FALL': 9.81,
            'ALERT_FLIP': 1000,
            
        }    

        self.detector_ai = DetectorAI(self.treshold_ai)
        self.detector_th = DetectorTH(self.treshold_th)


    def detect_start(self, ser_data, image_data):

        is_eye_closed, sleep_time = self.detector_ai.is_sleep(image_data)
        is_moving, event_time = self.detector_th.is_event(ser_data)
        time.sleep(0.1)

        if is_eye_closed:
            if sleep_time > 2:
                print(f"The eyes are closed for {sleep_time} seconds. This is considered as sleep.")
            else:
                print(".", sleep_time)
        else: # The eyes are open
            print("The eyes are open.")
        
        


      



