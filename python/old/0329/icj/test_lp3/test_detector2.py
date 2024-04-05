from scipy.spatial.transform import Rotation as R
from scipy.spatial import distance as dist
import cv2
import sys
import mediapipe as mp
import time
import math

class MyDetector:
    def __init__(self):
        self.cam = self.webcam_open()  # Open webcam
        self.sleep_start = None  # Initialize sleep_start

    def webcam_open(self):
        try:
            return cv2.VideoCapture(0)
        except Exception as e:
            print(f'Cannot open the webcam: {e}')
            sys.exit(1)

    def frame_capture(self):
        ret, frame = self.cam.read()
        return frame

    def calculate_ear(self, eye):
        # Calculate eye aspect ratio (EAR)
        A = dist.euclidean([eye[1].x, eye[1].y], [eye[5].x, eye[5].y])
        B = dist.euclidean([eye[2].x, eye[2].y], [eye[4].x, eye[4].y])
        C = dist.euclidean([eye[0].x, eye[0].y], [eye[3].x, eye[3].y])
        ear = (A + B) / (2.0 * C)
        return ear

    def is_sleep(self):
        mp_face_mesh = mp.solutions.face_mesh

        with mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5) as face_mesh:
            image = self.frame_capture()
            results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            if not results.multi_face_landmarks:
                return False, 0

            EAR_THRESHOLD = 0.3
            LEFT_EYE_INDICES = [33, 160, 158, 133, 153, 144]
            RIGHT_EYE_INDICES = [362, 385, 387, 263, 390, 374]

            for face_landmarks in results.multi_face_landmarks:
                left_eye = [face_landmarks.landmark[i] for i in LEFT_EYE_INDICES]
                right_eye = [face_landmarks.landmark[i] for i in RIGHT_EYE_INDICES]

                leftEAR = self.calculate_ear(left_eye)
                rightEAR = self.calculate_ear(right_eye)

                ear = (leftEAR + rightEAR) / 2.0

                if math.isclose(ear, EAR_THRESHOLD, abs_tol=0.1):
                    if self.sleep_start is None:
                        self.sleep_start = time.time()
                        return True, 0
                    else:  # 2 seconds
                        return True, time.time() - self.sleep_start
                else:
                    self.sleep_start = None
                    return False, None

def main():
    detector = MyDetector()

    while True:
        is_eye_closed, sleep_time = detector.is_sleep()
        time.sleep(0.1)

        if is_eye_closed:
            if sleep_time > 10:
                print(f"The eyes are closed for {sleep_time} seconds. This is considered as sleep.")
            else:
                print(".", sleep_time)
        else:
            print("The eyes are open.")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    detector.cam.release()

if __name__ == "__main__":
    main()