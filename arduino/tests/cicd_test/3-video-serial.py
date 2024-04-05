# 파이썬 배포 테스트
# 1. (now) /dev/video0 웹캠에서 프레임을 캡처하고 서버로 전송합니다.
# 2.       /dev/ttyACM0 시리얼 포트에서 데이터를 읽고 서버로 전송합니다.
# 3.       /dev/video0 웹캠에서 프레임을 캡처하고 /dev/ttyACM0 시리얼 포트에서 데이터를 읽어 서버로 전송합니다.
# 4.       mediapipe를 사용하여 웹캠에서 프레임을 캡처하고 서버로 전송합니다.


# -- requirements.txt
# requests
# opencv-python
# numpy
# mediapipe
# boto3
# pyserial
# ----------------------------------
#
# -- Dockerfile
# FROM python:3.8
# WORKDIR /app
# COPY . .
# RUN pip install -r requirements.txt
# CMD ["python", "main.py"]
#
# docker build -t your_image .
# docker run -it --device /dev/video0 --device=/dev/ttyS0 your_image
# ----------------------------------

import cv2
import requests
import numpy as np
from io import BytesIO

# 웹캠을 엽니다.
cap = cv2.VideoCapture(0)

print('웹캠을 엽니다.')

if not cap.isOpened():
    print('웹캠을 열 수 없습니다.')
    exit()

while True:
    # 웹캠에서 프레임을 캡처합니다.
    ret, frame = cap.read()
    ip = '192.168.0.3'
    port = 8083

    url_icj = f'http://{ip}:{port}/check'
    

    # 프레임을 JPEG 형식으로 인코딩합니다.
    _, jpeg = cv2.imencode('.jpg', frame)
    jpeg_bytes = jpeg.tobytes()
    jpeg_file = BytesIO(jpeg_bytes)

    # 서버로 POST 요청을 보냅니다.
    try:
        response = requests.post(url_icj, files={'frame': ('image.jpg', jpeg_file, 'image/jpeg')}, data={'TH' : [0., 0.]})
        # 응답을 출력합니다.
        print(response.text)
    except requests.exceptions.RequestException as e:
        print(e)


    # 'q' 키를 누르면 루프에서 빠져나옵니다.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 웹캠을 닫습니다.
cap.release()
cv2.destroyAllWindows()


# 각 클라이언트 요청마다 새로운 스레드를 생성하여 독립적인 비디오 스트림을 제공합니다. 
# 이렇게 하면 여러 창에서 동시에 비디오 스트리밍을 볼 수 있습니다.
# http://192.168.100.58:3000/data 로 접속하면 웹캠의 영상을 볼 수 있습니다.