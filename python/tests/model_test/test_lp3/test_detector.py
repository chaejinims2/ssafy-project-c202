# my_detector.py
from scipy.spatial.transform import Rotation as R
from scipy.spatial import distance as dist

import cv2
import sys
import mediapipe as mp

class MyDetector:
    def __init__(self):
        self.treshold = [9.9, 9.9]
        self.cam = self.webcam_open()  # Open webcam
        self.ret = None
        self.frame = None

    def detect_start(self):
        self.ai_algo_image()

    def webcam_open(self):
        try:
            return cv2.VideoCapture(0)
        except Exception as e:
            print(f'Cannot open the webcam: {e}')
            sys.exit(1)

    def frame_capture(self):
        self.ret, self.frame = self.cam.read()





    def calculate_ear(self,eye):
        # compute the euclidean distances between the two sets of
        # vertical eye landmarks (x, y)-coordinates
        print(eye[1], eye[5])
        # A = dist.euclidean(eye[1][:2], eye[5][:2])
        # B = dist.euclidean(eye[2][:2], eye[4][:2])
        
        A = dist.euclidean([eye[1].x, eye[1].y], [eye[5].x, eye[5].y])
        B = dist.euclidean([eye[2].x, eye[2].y], [eye[4].x, eye[4].y])
        # compute the euclidean distance between the horizontal
        # eye landmark (x, y)-coordinates
        # C = dist.euclidean(eye[0][:2], eye[3][:2])
        C = dist.euclidean([eye[0].x, eye[0].y], [eye[3].x, eye[3].y])

        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)

        # return the eye aspect ratio
        return ear
    def ai_algo_image(self):
        # mediapipe를 사용하여 눈을 감고 있는지 판단
        mp_face_mesh = mp.solutions.face_mesh
        mp_drawing = mp.solutions.drawing_utils  # 추가: 랜드마크를 그리기 위한 drawing_utils

        # For static images:
        with mp_face_mesh.FaceMesh(
            static_image_mode=False,  # 수정: 실시간 영상 처리를 위해 False로 설정
            max_num_faces=1,
            min_detection_confidence=0.5) as face_mesh:
            image = self.frame
            # Convert the BGR image to RGB before processing.
            results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            # If no face detected, return False
            if not results.multi_face_landmarks:
                return False

            # threshold to determine if the eye is closed
            EAR_THRESHOLD = 0.3
            LEFT_EYE_INDICES = [33, 7, 163, 144, 145, 153, 154, 155, 133]
            RIGHT_EYE_INDICES = [362, 263, 249, 390, 373, 374, 380, 381, 382]
            for face_landmarks in results.multi_face_landmarks:
                # Draw all landmarks.
                mp_drawing.draw_landmarks(image, face_landmarks)

                # Draw the eye landmarks in a different color.
                for index in LEFT_EYE_INDICES + RIGHT_EYE_INDICES:
                    landmark = face_landmarks.landmark[index]
                    # Convert the landmark from relative coordinates to image coordinates.
                    x = int(landmark.x * image.shape[1])
                    y = int(landmark.y * image.shape[0])
                    cv2.circle(image, (x, y), 1, (255, 0, 0), -1)  # Red color

                # Get the coordinates of left and right eye landmarks
                left_eye = [face_landmarks.landmark[i] for i in LEFT_EYE_INDICES]
                right_eye = [face_landmarks.landmark[i] for i in RIGHT_EYE_INDICES]

                # Calculate EAR for left and right eye
                leftEAR = self.calculate_ear(left_eye)
                rightEAR = self.calculate_ear(right_eye)

                # Average the eye aspect ratio together for both eyes
                ear = (leftEAR + rightEAR) / 2.0

                # Check if the eye aspect ratio is below the blink threshold
                if ear < EAR_THRESHOLD:
                    return True  # Eye is closed

            # 수정: 눈이 열려 있는 경우, 랜드마크가 그려진 프레임을 보여줍니다.
            cv2.imshow('Frame', image)
            return False  # Eye is open
        

def main():
    # MyDetector 객체를 생성합니다.
    detector = MyDetector()


    while True:
        # 웹캠에서 프레임을 캡처합니다.
        detector.frame_capture()

        # 캡처한 프레임에서 눈이 감겨 있는지 판단합니다.
        is_eye_closed = detector.detect_start()

        # 결과를 출력합니다.
        if is_eye_closed:
            print("The eyes are closed.")
        else:
            print("The eyes are open.")

        # 'q' 키를 누르면 루프에서 빠져나옵니다.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 웹캠을 종료합니다.
    detector.cam.release()

if __name__ == "__main__":
    print(mp.__version__)
    main()