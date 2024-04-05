# algo_ai.py
from scipy.spatial import distance as dist
import math
import time
import cv2
import mediapipe as mp

class DetectorAI:
    def __init__(self, threshold):
        self.threshold = threshold
        self.sleep_start = None  # Initialize sleep_start

    
    # 이미지에서 눈이 감겨있으면 수면으로 판단, 눈이 감겨있지 않으면 수면이 아님
    def is_sleep(self, image_data):
        mp_face_mesh = mp.solutions.face_mesh

        with mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5) as face_mesh:
            image = image_data
            results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            if not results.multi_face_landmarks:
                return False, 0


            for face_landmarks in results.multi_face_landmarks:
                left_eye = [face_landmarks.landmark[i] for i in self.threshold['EYE_INDICES']['LEFT']]
                right_eye = [face_landmarks.landmark[i] for i in self.threshold['EYE_INDICES']['RIGHT']]

                leftEAR = calculate_ear(left_eye)
                rightEAR = calculate_ear(right_eye)

                ear = (leftEAR + rightEAR) / 2.0

                if math.isclose(ear, self.threshold['SLEEP_EAR_THRESHOLD'], abs_tol=0.1):
                    if self.sleep_start is None:
                        self.sleep_start = time.time()
                        return True, 0
                    else:  # 2 seconds
                        return True, time.time() - self.sleep_start
                else:
                    self.sleep_start = None
                    return False, None


    def is_event(self, feature):
        # Implement your event detection algorithm here
        pass


    # 
    def is_accident(self, feature):
        # Implement your accident detection algorithm here
        pass

def calculate_ear(eye):
    # Calculate eye aspect ratio (EAR)
    A = dist.euclidean([eye[1].x, eye[1].y], [eye[5].x, eye[5].y])
    B = dist.euclidean([eye[2].x, eye[2].y], [eye[4].x, eye[4].y])
    C = dist.euclidean([eye[0].x, eye[0].y], [eye[3].x, eye[3].y])
    ear = (A + B) / (2.0 * C)
    return ear
