# my_detector.py
from scipy.spatial.transform import Rotation as R

import cv2
import mediapipe as mp
import urllib
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np


class MyDetector:
    def __init__(self):

                
        self.f1 = 0
        self.f2 = 0
        self.f1_threshold = 9.9  # 중력 센서에서의 충격 감지 임계값
        self.f2_threshold = 9.9


        # self.detect_config = {
        #     'score_sleep': 0.5,
        #     'score_event': 0.5,
        #     'score_accident': 0.5
        # }

        BG_COLOR = (192, 192, 192) # gray
        MASK_COLOR = (255, 255, 255) # white
        IMAGE_FILENAMES = ['./images/1.jpg', './images/2.jpg']

        # Create the options that will be used for ImageSegmenter
        base_options = python.BaseOptions(model_asset_path='./models/selfie_multiclass_256x256.tflite')
        options = vision.ImageSegmenterOptions(base_options=base_options,
                                            output_category_mask=True)

        # Create the image segmenter
        with vision.ImageSegmenter.create_from_options(options) as segmenter:

        # Loop through demo image(s)
            for image_file_name in IMAGE_FILENAMES:

                # Create the MediaPipe image file that will be segmented
                image = mp.Image.create_from_file(image_file_name)

                # Retrieve the masks for the segmented image
                segmentation_result = segmenter.segment(image)
                category_mask = segmentation_result.category_mask

                # Generate solid color images for showing the output segmentation mask.
                image_data = image.numpy_view()
                fg_image = np.zeros(image_data.shape, dtype=np.uint8)
                fg_image[:] = MASK_COLOR
                bg_image = np.zeros(image_data.shape, dtype=np.uint8)
                bg_image[:] = BG_COLOR

                condition = np.stack((category_mask.numpy_view(),) * 3, axis=-1) > 0.2
                output_image = np.where(condition, fg_image, bg_image)

                self.resize_and_show(output_image)

    def resize_and_show(image):
        image = cv2.imread('./new/new.jpg')

        # 이미지를 화면에 표시
        cv2.imshow('Image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def extract_features(self, data):
        self.f1 = (data['ser'].aX**2 + data['ser'].aY**2 + data['ser'].aZ**2)**0.5
        self.f2 = (data['ser'].gX**2 + data['ser'].gY**2 + data['ser'].gZ**2)**0.5


    def is_sleep(self, data):
        """수면을 감지하는 함수"""
        print("data", data)
        self.threshold_algo(data)
        return self.f1 < self.f1_threshold

    def is_event(self, data):
        """사건을 감지하는 함수"""
        return self.f2 > self.f1_threshold
    
    
    def is_accident(self, data):
        """사고를 감지하는 함수"""
        return self.f1 > 0
    





    def LPF(Input, PastInput, PastOutput):
        # CutOffFrequency is 10hz
        # SamplingFrequency is 1/0.001 => 1000

        CutOffFrequency = 10.0
        SamplingFrequency = 500.0

        w0 = 2 * 3.14 * CutOffFrequency
        a1 = (w0 - 2 * SamplingFrequency) / (2 * SamplingFrequency + w0)
        b0 = w0 / (2 * SamplingFrequency + w0)
        b1 = b0

        Output = b0 * Input + b1 * PastInput - a1 * PastOutput
        PastOutput = Output
        PastInput = Input

        return Output, PastInput, PastOutput

    def convert_to_euler(accel_data, gyro_data):
        # Assuming accel_data and gyro_data are numpy arrays of shape (3,)
        # and represent acceleration and angular velocity respectively

        # First, we normalize the accelerometer data
        accel_data = accel_data / np.linalg.norm(accel_data)

        # Assuming that the device is not accelerating, the accelerometer data can be considered as the orientation
        # We can convert this orientation into a quaternion
        accel_quat = R.from_rotvec(accel_data).as_quat()

        # Next, we integrate the gyroscope data over time to get the orientation
        # This is a very simple integration and might not be accurate over long periods of time
        gyro_quat = R.from_rotvec(gyro_data).as_quat()

        # We combine the two quaternions to get a more accurate orientation
        combined_quat = accel_quat * gyro_quat

        # Finally, we convert the quaternion to Euler angles
        euler_angles = R.from_quat(combined_quat).as_euler('xyz')

        return euler_angles  # This will return [roll, pitch, yaw]

    # def ai_algo_image(self, cam_data):
    #     mp_drawing = mp.solutions.drawing_utils
    #     mp_objectron = mp.solutions.objectron

    #     # For static images:
    #     with mp_objectron.Objectron(static_image_mode=True) as objectron:
    #         # Convert the BGR image to RGB and process it with MediaPipe Objectron.
    #         results = objectron.process(cv2.cvtColor(cam_data, cv2.COLOR_BGR2RGB))

    #         # Draw the box landmarks on the image.
    #         if results.detected_objects:
    #             for detected_object in results.detected_objects:
    #                 mp_drawing.draw_landmarks(cam_data, detected_object.landmarks_2d, mp_objectron.BOX_CONNECTIONS)
    #                 mp_drawing.draw_axis(cam_data, detected_object.rotation, detected_object.translation)

    #                 # Check if the object is out of the image bounds
    #                 for landmark in detected_object.landmarks_2d.landmark:
    #                     if landmark.x < 0 or landmark.y < 0 or landmark.x > cam_data.shape[1] or landmark.y > cam_data.shape[0]:
    #                         print("Accident detected: Object is out of image bounds")
    #                         return True

    #     return False
        

    def threshold_algo(self, data):
        nn1 = ((float)(data.aX))/32768.0 * 16 
        nn2 = ((float)(data.aY))/32768.0 * 16 
        nn3 = ((float)(data.aZ))/32768.0 * 16
        
        nn4 = ((float)(data.gX))/32768.0 * 1000 
        nn5 = ((float)(data.gY))/32768.0 * 1000 
        nn6 = ((float)(data.gZ))/32768.0 * 1000

        lpf_X, ax_1, ax_2, ax_3 = self.LPF(nn1, ax_1, ax_2, ax_3)
        lpf_Y, ay_1, ay_2, ay_3 = self.LPF(nn2, ay_1, ay_2, ay_3)
        lpf_Z, az_1, az_2, az_3 = self.LPF(nn3, az_1, az_2, az_3)

        self.f1 = (data.aX**2 + data.aY**2 + data.aZ**2)**0.5
        self.f2 = (data.gX**2 + data.gY**2 + data.gZ**2)**0.5
        self.euler = self.convert_to_euler([lpf_X, lpf_Y, lpf_Z], [nn4, nn5, nn6])
       

