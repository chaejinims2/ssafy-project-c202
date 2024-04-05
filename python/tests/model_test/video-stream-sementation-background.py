import cv2
import mediapipe as mp
import numpy as np
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation

class StreamingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
        self.end_headers()
        with mp_selfie_segmentation.SelfieSegmentation(model_selection=1) as selfie_segmentation:
            while True:
                ret, frame = cap.read()  # Read one frame from the camera
                if not ret:
                    break
                # Convert the BGR image to RGB and process it with MediaPipe Selfie Segmentation.
                result = selfie_segmentation.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                # Draw selfie segmentation on the background image.
                annotated_image = frame.copy()
                condition = np.stack((result.segmentation_mask,) * 3, axis=-1) > 0.1
                annotated_image = np.where(condition, annotated_image, 255)
                ret, jpeg = cv2.imencode('.jpg', annotated_image)  # Encode the frame as JPEG
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