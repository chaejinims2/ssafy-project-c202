# 각 클라이언트 요청마다 새로운 스레드를 생성하여 독립적인 비디오 스트림을 제공합니다. 
# 이렇게 하면 여러 창에서 동시에 비디오 스트리밍을 볼 수 있습니다.
# http://192.168.100.58:3000/data 로 접속하면 웹캠의 영상을 볼 수 있습니다.
import cv2
import requests
import numpy as np
from io import BytesIO
import time

import mediapipe as mp

# 웹캠을 엽니다.
cap = cv2.VideoCapture(0)

print('웹캠을 엽니다.')

if not cap.isOpened():
    print('웹캠을 열 수 없습니다.')
    exit()

while True:
    # 웹캠에서 프레임을 캡처합니다.
    ret, frame = cap.read()

    

    # 프레임을 JPEG 형식으로 인코딩합니다.
    _, jpeg = cv2.imencode('.jpg', frame)
    jpeg_bytes = jpeg.tobytes()
    jpeg_file = BytesIO(jpeg_bytes)
    a_time = time.time() * 1000
    b_time = time.time() * 1000

    # 서버로 POST 요청을 보냅니다.
    try:
        response = requests.post('http://192.168.100.58:3000/data', files={'image': ('image.jpg', jpeg_file, 'image/jpeg')})
        # 응답을 출력합니다.
        # print(response.text)
        b_time = time.time() * 1000
        print('time: ', round(b_time - a_time, 3), '(ms)')
        a_time = b_time

    except requests.exceptions.RequestException as e:
        print(e)


    # 'q' 키를 누르면 루프에서 빠져나옵니다.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 웹캠을 닫습니다.
cap.release()
cv2.destroyAllWindows()