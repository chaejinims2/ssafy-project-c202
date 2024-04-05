# my_main.py
from my_sensor import MySensor
# import boto3

from my_detector import MyDetector
import time
ACCIDENT_THRESHOLD =   9.9

# AWS 계정의 액세스 키와 시크릿 키 설정
ACCESS_KEY = ''
SECRET_KEY = ''
 # S3 버킷 이름
BUCKET_NAME = ''

class EdgeLP:
    def __init__(self, network_manager):
        
        self.my_edge = {
            "network_manager":network_manager,
            "sensor_data":MySensor(),
            "detector":MyDetector(),
        }

    def collect_data(self):
        self.my_edge['sensor_data'].get()
        self.check()  # Check for accidents after collecting data
        # print("self.my_edge['sensor_data']",self.my_edge['sensor_data'].ser_data)
        # 만약 데이터 요청 시
        if self.my_edge['network_manager'].request_data:
            self.my_edge['network_manager'].send_data_to_server(self.my_edge['sensor_data'].data) 
            self.my_edge['network_manager'].request_data = False



    # 영상, 오디오, 시리얼 통신을 위한 시작 세팅
    def start_data(self):
        print("Starting sensor data...")
        # Add logic to start sensor data acquisition
        self.collect_data()  # Example: Call the collect_data method

    def check(self):
        self.check_for_sleep()
        self.check_for_event()


    def check_for_sleep(self):
        # Check the sensor data for sleep
        # if self.my_edge['detector'].is_sleep(self.my_edge['sensor_data'].data):
            self.event_handler(0)

    def check_for_event(self):
        # Check the sensor data for accidents
        # This is just a placeholder. Replace with your actual logic.

        if self.my_edge['detector'].is_event(self.my_edge['sensor_data'].data):
            self.event_handler(1)
        
    def event_handler(self, cmd):
        time.sleep(0.5)
        
        return {
            0: print("Sleep detected!"),
            1: print("Accident detected!"),
        }
    
    # def uploadS3(FILE_NAME, file_path):
    #     # S3 클라이언트 생성
    #     s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    #     # 파일 업로드
    #     with open(file_path, 'rb') as file:
    #         s3.upload_fileobj(file, BUCKET_NAME, FILE_NAME)

    #     # 업로드 완료를 확인하기 위해 S3 객체 생성
    #     s3_resource = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    #     obj = s3_resource.Object(BUCKET_NAME, FILE_NAME)


    #     # 업로드 완료를 확인하고 완료될 때까지 대기
    #     while True:
    #         if obj.content_length:
    #             break
    #         time.sleep(1)

    #     print("업로드 성공!")

    #     # 업로드된 파일의 URL 생성
    #     url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{FILE_NAME}"
    #     print("Uploaded file URL:", url)
        
    #     return url

        
