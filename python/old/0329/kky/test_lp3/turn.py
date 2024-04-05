import cv2
import mediapipe as mp
import math
import os

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# 함수: 양쪽 어깨의 위치를 기준으로 아이의 몸이 옆으로 보이는지 감지
def detect_side_pose(landmarks):
    left_shoulder_x = landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x
    right_shoulder_x = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x
    
    # 양쪽 어깨의 위치가 일정 범위 이내로 차이나면 옆모습으로 판단
    if abs(left_shoulder_x - right_shoulder_x) < 0.1: # 예시로 0.1의 임계값 사용
        return True
    else:
        return False

# Mediapipe Pose 모델 로드
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

# 입력 이미지가 있는 폴더 경로
input_folder_path = './input/'
# 출력 이미지를 저장할 폴더 경로
output_folder_path = './output/'

# 입력 폴더 내의 모든 이미지 파일에 대해 처리
for filename in os.listdir(input_folder_path):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(input_folder_path, filename)
        # 이미지 불러오기
        image = cv2.imread(image_path)
        # 이미지를 RGB로 변환
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Mediapipe Pose 모델을 사용하여 포즈 감지
        results = pose.process(image_rgb)
        # 결과에서 포즈 랜드마크 추출
        landmarks = results.pose_landmarks

        # 감지 함수를 사용하여 감지
        if detect_side_pose(landmarks):
            print(f"The child's body is seen from the side in {filename}.")
        else:
            print(f"The child's body is not seen from the side in {filename}.")

        # 랜드마크를 이미지에 그리기
        if landmarks is not None:
            image_with_landmarks = image.copy()
            mp_drawing.draw_landmarks(
                image_with_landmarks,
                landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=2, circle_radius=2)
            )
            # 출력 이미지 저장
            output_image_path = os.path.join(output_folder_path, filename.split('.')[0] + '_pose.jpg')
            cv2.imwrite(output_image_path, image_with_landmarks)
            print(f"Pose landmarks saved for {filename}.")

cv2.destroyAllWindows()
