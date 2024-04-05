
import requests
# from my_sensor import MySensor

class NetworkManager:
    def __init__(self, ip, port, baby_id):
        self.ip = ip
        self.port = port
        self.baby_id = baby_id
        self.url = f'http://{self.ip}:{self.port}/event/{self.baby_id}'
        
    def connect_to_server(self):
        print("Connecting to server...")
        # Add logic to connect to the server
        self.request_data()

    def send_data_to_server(self, data):
         # Send POST request to the server
        try:
            response = requests.post(self.url, files={'image': data['image_data']}, data={**data['form_data'], **data['time_data']})

        except requests.exceptions.RequestException as e:
            print(e)

    def request_data(self):
        print("Requesting data...")
        return True
    
