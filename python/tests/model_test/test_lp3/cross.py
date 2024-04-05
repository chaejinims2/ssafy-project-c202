import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# 함수: 다리 꼰 자세 감지
def detect_crossed_legs(landmarks, annotated_image):
    # left_knee = (landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE.value].y)
    # left_ankle = (landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE.value].y)
    # right_knee = (landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE.value].y)
    # right_ankle = (landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y)
    
    # # 무릎과 발목을 이은 선 그리기
    # cv2.line(annotated_image, (int(left_knee[0]*width), int(left_knee[1]*height)), 
    #          (int(left_ankle[0]*width), int(left_ankle[1]*height)), (0, 255, 0), 2)
    # cv2.line(annotated_image, (int(right_knee[0]*width), int(right_knee[1]*height)), 
    #          (int(right_ankle[0]*width), int(right_ankle[1]*height)), (0, 255, 0), 2)
    
    # # 무릎과 발목을 이은 선 사이의 거리 계산
    # left_distance = abs(left_knee[1] - left_ankle[1])
    # right_distance = abs(right_knee[1] - right_ankle[1])
    
    # # 무릎과 발목을 이은 선이 교차하는지 확인
    # if left_distance > right_distance:
    #     return True
    # else:
    #     return False
    left_knee_x = landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE.value].x
    right_knee_x = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE.value].x
    left_ankle_x = landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE.value].x
    right_ankle_x = landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x

    # 왼쪽 무릎의 위치가 오른쪽 무릎의 위치와 다를 때 다리가 꼰 자세로 판단
    if (left_knee_x - right_knee_x) * (left_ankle_x - right_ankle_x) <= 0:
        return True
    else:
        return False

# Mediapipe Pose 모델 로드
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

# 이미지 파일 경로 설정
image_path = './input/유아다리.jpg'

# 이미지 불러오기
image = cv2.imread(image_path)
height, width, _ = image.shape

# 이미지를 RGB로 변환
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Mediapipe Pose 모델을 사용하여 포즈 감지
results = pose.process(image_rgb)

# 결과에서 포즈 랜드마크 추출
landmarks = results.pose_landmarks

# 랜드마크가 적용된 이미지 표시
annotated_image = image.copy()
mp_drawing.draw_landmarks(
    annotated_image,
    results.pose_landmarks,
    mp_pose.POSE_CONNECTIONS,
    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2),
    connection_drawing_spec=mp_drawing.DrawingSpec(color=(255,255,0), thickness=2, circle_radius=2))

# 다리 꼰 자세 감지
if detect_crossed_legs(landmarks, annotated_image):
    print("다리 꼰 자세를 감지했습니다.")
else:
    print("다리 꼰 자세를 감지하지 못했습니다.")

# 이미지 저장
output_image_path = './output/다리_꼰_자세_감지.jpg'
cv2.imwrite(output_image_path, annotated_image)
print(f"감지된 이미지를 {output_image_path}에 저장했습니다.")

# # 결과 이미지를 화면에 표시
# cv2.imshow('Annotated Image', annotated_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
