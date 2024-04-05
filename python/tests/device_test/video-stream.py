import cv2
from http.server import BaseHTTPRequestHandler, HTTPServer


PAGE="""\
<html>
<head>
<title>picamera MJPEG streaming demo</title>
</head>
<body>
<h1>PiCamera MJPEG Streaming Demo</h1>
<img src="stream.mjpg" width="640" height="480" />
</body>
</html>
"""

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

class StreamingServer(HTTPServer):
    allow_reuse_address = True

cap = cv2.VideoCapture(0)  # Open the camera
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 24)

try:
    address = ('', 8000)
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()
finally:
    cap.release()  # Release the camera