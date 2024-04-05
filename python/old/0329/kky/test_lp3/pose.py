import os
import cv2
import mediapipe as mp
import math

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def detect_cheer_pose(landmarks):
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value]
    right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value]

    # 양 어깨보다 양쪽 팔꿈치가 더 위에 있는 경우 만세 포즈로 간주
    if left_elbow.y < left_shoulder.y and right_elbow.y < right_shoulder.y:
        return True
    else:
        return False


# 입력 이미지가 있는 폴더 경로
input_folder_path = './input/'

# 출력 이미지를 저장할 폴더 경로
output_folder_path = './output/'

# 입력 폴더 내의 모든 이미지 파일에 대해 처리
for filename in os.listdir(input_folder_path):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(input_folder_path, filename)
        image = cv2.imread(image_path)

        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.pose_landmarks:
                annotated_image = image.copy()
                for lm_id, landmark in enumerate(results.pose_landmarks.landmark):
                    # 랜드마크 좌표
                    height, width, _ = image.shape
                    cx, cy = int(landmark.x * width), int(landmark.y * height)
                    cv2.putText(annotated_image, f'{mp_pose.PoseLandmark(lm_id).name} ({cx}, {cy})', (cx, cy),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1, cv2.LINE_AA)
                
                mp_drawing.draw_landmarks(
                    annotated_image,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2),
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(255,255,0), thickness=2, circle_radius=2))


                # 출력 이미지 저장
                output_image_path = os.path.join(output_folder_path, filename.split('.')[0] + '_OUTPUT.jpg')
                cv2.imwrite(output_image_path, annotated_image)

                # 만세 포즈 감지
                if detect_cheer_pose(results.pose_landmarks.landmark):
                    print(f"Cheer pose detected in {filename}!")

cv2.destroyAllWindows()