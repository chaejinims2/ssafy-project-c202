# 각 클라이언트 요청마다 새로운 스레드를 생성하여 독립적인 비디오 스트림을 제공합니다. 
# 이렇게 하면 여러 창에서 동시에 비디오 스트리밍을 볼 수 있습니다.
# http://192.168.100.245:8000/ 로 접속하면 웹캠의 영상을 볼 수 있습니다.

import cv2
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

class StreamingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
        self.end_headers()
        while True:
            ret, frame = cap.read()  # Read one frame from the camera
            if not ret:
                break
            ret, jpeg = cv2.imencode('.jpg', frame)  # Encode the frame as JPEG
            if not ret:
                break
            self.wfile.write(b'--frame\r\n')
            self.send_header('Content-type', 'image/jpeg')
            self.send_header('Content-length', str(len(jpeg)))
            self.end_headers()
            self.wfile.write(jpeg)
            self.wfile.write(b'\r\n')

class ThreadingServer(ThreadingMixIn, HTTPServer):
    pass

cap = cv2.VideoCapture(0)  # Open the camera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 24)

try:
    address = ('', 8000)
    server = ThreadingServer(address, StreamingHandler)
    server.serve_forever()
finally:
    cap.release()  # Release the camera