import mediapipe as mp

mp_pose = mp.solutions.pose

# PoseLandmark 열거형을 순회하면서 각 랜드마크의 이름과 인덱스 번호 출력
for landmark in mp_pose.PoseLandmark:
    print(landmark.name, landmark.value)
