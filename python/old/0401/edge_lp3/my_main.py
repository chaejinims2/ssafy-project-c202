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
        self.prev_data = {
            'detail': False,
        }


    def collect_data(self):
        self.my_edge['sensor_data'].get()
        # print("self.my_edge['sensor_data']",self.my_edge['sensor_data'].data['ser_data'])
        sensor_data = self.my_edge['sensor_data'].data
        self.rst = self.my_edge['detector'].detect_start(
            sensor_data['timestamp'], 
            sensor_data['th'], 
            sensor_data['ser_data'], 
            sensor_data['image_data'], 
            sensor_data['frame']
        )
        # print("self.rst: ", self.rst)
        self.sleep_rst = self.rst['sleep_data']
        self.event_rst = self.rst['event_data']


        if self.event_rst['index'] is not None and self.event_rst['index'] != 0 :
            # print(self.event_rst)
            self.my_edge['network_manager'].send_event_to_server(self.event_rst)
            
        if self.sleep_rst['detail'] is not None and self.sleep_rst['detail'] != self.prev_data['detail']:
            # print(self.sleep_rst)
            self.my_edge['network_manager'].send_event_to_server(self.sleep_rst)
        
        
        # 만약 데이터 요청 시
        if self.my_edge['network_manager'].is_requested():
            self.my_edge['sensor_data'].data['index'] = 1
            self.my_edge['sensor_data'].data['event_type'] = None
            self.my_edge['sensor_data'].data['detail'] = None
            self.my_edge['network_manager'].send_data_to_server(self.my_edge['sensor_data'].data) 
        
        self.prev_data['detail'] = self.sleep_rst['detail']



    # 영상, 오디오, 시리얼 통신을 위한 시작 세팅
    def start_data(self):
        print("Starting sensor data...")
        self.collect_data() 


        
