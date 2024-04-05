# my_main.py
from my_sensor import MySensor
from detection.my_detector import MyDetector

class EdgeLP:
    """
    The EdgeLP class is responsible for managing the edge device, including collecting sensor data, 
    detecting events, and sending data to the server.
    """

    def __init__(self, network_manager):
        """
        Initialize the EdgeLP with a network manager, a sensor, and a detector.
        """
        self.my_edge = {
            "network_manager": network_manager,
            "sensor_data": MySensor(),
            "detector": MyDetector(),
        }
        self.prev_data = [2, 0, 0]

    def collect_data(self):
        """
        Collect sensor data, detect events, and send data to the server.
        """
        self.my_edge['sensor_data'].get()
        # de = False
        # if de:
        if self.my_edge['network_manager'].is_requested():
            self.my_edge['sensor_data'].data['info'] = [1, 0, 0]
            self.my_edge['network_manager'].send_data_to_server(self.my_edge['sensor_data'].data) 
            
        else:
            
            sensor_data = self.my_edge['sensor_data'].data
            self.rst = self.my_edge['detector'].detect_start(
                sensor_data['timestamp'], 
                sensor_data['th'], 
                sensor_data['ser_data'], 
                sensor_data['image_data'], 
                sensor_data['frame']
            )
            self.sleep_rst = self.rst['sleep_data']
            self.event_rst = self.rst['event_data']

            if self.event_rst['info'] is not None and self.event_rst['info'][2] != -1 :
                self.my_edge['network_manager'].send_event_to_server(self.event_rst)
                print("event",self.event_rst['info'])
            if self.sleep_rst['info'][2] is not None and self.sleep_rst['info'][2] != self.prev_data[2]:
                print("sleep",self.sleep_rst['info'])
                self.my_edge['network_manager'].send_event_to_server(self.sleep_rst)
            

            self.prev_data[2] = self.sleep_rst['info'][2]

    def start_data(self):
        """
        Start collecting sensor data.
        """
        print("Starting sensor data...")
        self.collect_data()
        
