# algo_th.py

import numpy as np
from scipy.spatial.transform import Rotation as R

class DetectorTH:
    def __init__(self, threshold):
        self.feature = [0, 0]
        self.euler = [0, 0, 0]
        self.raw = [0, 0, 0, 0, 0, 0]
        self.threshold = threshold

    def is_event(self, data):
        self.extract_features(data)
        print("Feature: ", self.feature, "Euler: ", self.euler)
        if self.feature[0] > self.threshold['ALERT_FALL']:
            print("FALL ALERT")
                
        if abs(self.euler[2] - 180) < self.threshold['ALERT_FLIP'] or abs(self.euler[2] + 180) < self.threshold['ALERT_FLIP']:
            print("FLIP ALERT")

        return False, None

    def extract_features(self, data):
        # Normalize raw data
        self.raw = [data.aX/32768.0 * 16, data.aY/32768.0 * 16, data.aZ/32768.0 * 16, 
                    data.gX/32768.0 * 1000, data.gY/32768.0 * 1000, data.gZ/32768.0 * 1000]

        # Calculate features
        self.feature[0] = np.linalg.norm(self.raw[:3])  # Magnitude of acceleration
        self.feature[1] = np.linalg.norm(self.raw[3:])  # Magnitude of gyroscope

        # Convert to Euler angles
        self.euler = self.convert_to_euler(self.raw[:3], self.raw[3:])

    def convert_to_euler(self, accel_data, gyro_data):
        # Normalize the accelerometer data
        accel_data = accel_data / np.linalg.norm(accel_data)

        # Convert accelerometer and gyroscope data to quaternions
        accel_quat = R.from_rotvec(accel_data).as_quat()
        gyro_quat = R.from_rotvec(gyro_data).as_quat()

        # Combine the two quaternions to get a more accurate orientation
        combined_quat = accel_quat * gyro_quat

        # Convert the quaternion to Euler angles
        euler_angles = R.from_quat(combined_quat).as_euler('xyz')

        return euler_angles  # This will return [roll, pitch, yaw]