import cv2
import requests
import numpy as np

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

    # 서버로 POST 요청을 보냅니다.
    try:
        response = requests.post('http://192.168.100.58:3000/data', data=jpeg_bytes)
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
