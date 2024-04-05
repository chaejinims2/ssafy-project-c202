import cv2
import asyncio
import websockets

async def send_video(websocket, path):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 24)
    
    try:
        while True:
            ret, frame = cap.read()  # Read one frame from the camera
            if not ret:
                break
            ret, jpeg = cv2.imencode('.jpg', frame)  # Encode the frame as JPEG
            if not ret:
                break
            await websocket.send(jpeg.tobytes())  # Send the JPEG frame over WebSocket
            await asyncio.sleep(0)  # Allow other tasks to run
    finally:
        cap.release()  # Release the camera

start_server = websockets.serve(send_video, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()