# my_main.py
from my_sensor import MySensor
from detection.my_detector import MyDetector

class EdgeLP:
    def __init__(self, network_manager):
        
        self.my_edge = {
            "network_manager":network_manager,
            "sensor_data":MySensor(),
            "detector":MyDetector(),
        }


    def collect_data(self):
        self.my_edge['sensor_data'].get()
        # print("self.my_edge['sensor_data']",self.my_edge['sensor_data'].data['ser_data'])
        self.event_rst, self.sleep_rst, self.rst_data = self.my_edge['detector'].detect_start(self.my_edge['sensor_data'].data['ser_data'], self.my_edge['sensor_data'].data['frame'])

        # if self.event_rst:
        
        if self.sleep_rst:
            self.my_edge['network_manager'].send_event_to_server(self.rst_data)
        # 만약 데이터 요청 시
        if self.my_edge['network_manager'].request_data:
            self.my_edge['network_manager'].send_data_to_server(self.my_edge['sensor_data'].data) 




    # 영상, 오디오, 시리얼 통신을 위한 시작 세팅
    def start_data(self):
        print("Starting sensor data...")
        self.collect_data() 


        
