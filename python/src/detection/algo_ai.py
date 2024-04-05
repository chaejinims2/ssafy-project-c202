# algo_ai.py
import cv2
import math
import time
from scipy.spatial import distance as dist
import mediapipe as mp

class DetectorAI:
    def __init__(self, threshold):
        self.threshold = threshold
        self.sleep_start = None
        self.flag = 0
        self.mp_pose = mp.solutions.pose
        self.mp_face_mesh = mp.solutions.face_mesh

    # 사용자가 잠들었는지 여부를 판단 : 눈의 EAR(Eye Aspect Ratio) 값이 임계값과 가까우면 사용자가 잠들었다고 판단하고, 그렇지 않으면 사용자가 깨어 있다고 판단
    def is_sleep(self, image_data):
        with self.mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5) as face_mesh:
            results = face_mesh.process(cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB))
            if not results.multi_face_landmarks:
                return False, 0, [2, 0, 1]
            for face_landmarks in results.multi_face_landmarks:
                left_eye = [face_landmarks.landmark[i] for i in self.threshold['EYE_INDICES']['LEFT']]
                right_eye = [face_landmarks.landmark[i] for i in self.threshold['EYE_INDICES']['RIGHT']]
                ear = (calculate_ear(left_eye) + calculate_ear(right_eye)) / 2.0
                if math.isclose(ear, self.threshold['IS_EYE_CLOSED_THRESHOLD'], abs_tol=0.1):
                    if self.sleep_start is None:
                        self.sleep_start = time.time()
                        return True, 0, [2, 0, 0]
                    else:
                        return True, time.time() - self.sleep_start, [2, 0, 0]
                else:
                    self.sleep_start = None
                    return False, None, [2, 0, 1]

    # 사용자의 행동을 판단 : 사용자의 자세가 특정 조건을 만족하면 해당 행동을 출력 (옆으로 누움, 만세, 다리 꼬기)
    def is_event(self, image_data):
        with self.mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5) as pose:
            results = pose.process(cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB))
            info= []
            flag = False
            if not results.pose_landmarks:
                info = [2, 2, -1]
                return flag, 0, info
            pose_landmarks = results.pose_landmarks
            body_indices = self.threshold['BODY_INDICES']
            left_shoulder, right_shoulder = pose_landmarks.landmark[body_indices['SHOULDER'][0]], pose_landmarks.landmark[body_indices['SHOULDER'][1]]
            left_elbow, right_elbow = pose_landmarks.landmark[body_indices['ELBOW'][0]], pose_landmarks.landmark[body_indices['ELBOW'][1]]
            left_knee, right_knee = pose_landmarks.landmark[body_indices['KNEE'][0]], pose_landmarks.landmark[body_indices['KNEE'][1]]
            left_ankle, right_ankle = pose_landmarks.landmark[body_indices['ANKLE'][0]], pose_landmarks.landmark[body_indices['ANKLE'][1]]
            if abs(left_shoulder.x - right_shoulder.x) < 0.1:
                self.flag = 1
                info = [2, 1, 0]
                flag = True
                # print("The child's body is seen from the side")
            elif left_elbow.y < left_shoulder.y and right_elbow.y < right_shoulder.y:
                self.flag = 2
                info = [2, 2, 1]
                flag = True
                # print("The child is cheering")
            elif (left_knee.x - right_knee.x) * (left_ankle.x - right_ankle.x) <= 0:
                self.flag = 3
                info = [2, 2, 2]
                flag = True
                # print("The child has crossed legs")
            else:
                self.flag = 0
                info = [2, 2, -1]
                flag = False
                # print("The child is in a normal state")
            return flag, self.flag, info

    # 머리 위치가 목표 위치와 일정 허용 오차 내에 있는지를 판단
    def is_located(self, image_data):
        with self.mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5) as pose:
            results = pose.process(cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB))
            info = []
            if not results.pose_landmarks:
                return False, 0, info
            pose_landmarks = results.pose_landmarks
            body_indices = self.threshold['BODY_INDICES']
            nose = pose_landmarks.landmark[body_indices['NOSE']]
            if abs(nose.x - self.threshold['IS_LOCATED_FLAG'][0]) < self.threshold['NON_LOCATED_TOLERANCE'] and abs(nose.y - self.threshold['IS_LOCATED_FLAG'][1]) < self.threshold['NON_LOCATED_TOLERANCE']:
                info = [2, 2, 0]
                return True, 1, info
            return False, 0, info

    # 사용자가 사고를 당했는지 여부를 판단
    def is_accident(self, feature):
        pass

def calculate_ear(eye):
    A = dist.euclidean([eye[1].x, eye[1].y], [eye[5].x, eye[5].y])
    B = dist.euclidean([eye[2].x, eye[2].y], [eye[4].x, eye[4].y])
    C = dist.euclidean([eye[0].x, eye[0].y], [eye[3].x, eye[3].y])
    return (A + B) / (2.0 * C)