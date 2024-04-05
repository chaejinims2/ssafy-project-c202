import requests
import geocoder
import time
import datetime
import boto3
import json

# AWS S3 bucket configuration
BUCKET_NAME = ''
AWS_REGION = ''
ACCESS_KEY = ''
SECRET_KEY = ''

class NetworkManager:
    """
    The NetworkManager class is responsible for managing the network connections and sending data to the server.
    """

    def __init__(self, ip, port, baby_id):
        """
        Initialize the NetworkManager with server IP, port, and baby ID.
        """
        self.ip = ip    
        self.port = port
        self.baby_id = baby_id

        # 개발용
        self.url_data = f'http://{self.ip}:{self.port}/data'
        self.url_event = f'http://{self.ip}:{self.port}/event'
        self.url_check = f'http://{self.ip}:{self.port}/check'

        # 배포용
        # self.url_data = f'http://{self.ip}:{self.port}/ai/data'
        # self.url_event = f'http://{self.ip}:{self.port}/ai/event'
        # self.url_check = f'http://{self.ip}:{self.port}/ai/check'
        
        self.last_upload_time = datetime.datetime.now()

        self.session = requests.Session()
        self.file = {}
        self.body = self._init_body()
        self.connect_to_server()

    def _init_body(self):
        """
        Initialize the body of the request with default values.
        """
        return {
            'baby_id':  self.baby_id,
            'ip': None,
            'latlng': None,
            'info': [0, 0, 0],
            'datetime': '2021-03-25 12:00:00.000000',
            'timestamp': 1711873161.4333634,
            'device_model': None,
            'device_id': None,
            'TH' : [0., 0.],
            'url_s3' : None,
            'status': None,
        }
    def is_requested(self):
        """Check if the server is running."""
        try:
            # Create a timestamp
            timestamp = datetime.datetime.now().isoformat()

            # Send a POST request with the timestamp in the body
            response = self.session.post(self.url_check, data=json.dumps({'timestamp': timestamp}), headers={'Content-Type': 'application/json'})
            # print(response.status_code)
            if response.status_code == 200:
                # Parse the response body as JSON
                data = response.json()

                # Get the currentStatus value
                currentStatus = data

                if currentStatus:
                    # print("Server is running and currentStatus is True.")
                    return True
                else:
                    # print("Server is running but currentStatus is False.")
                    return False
            else:
                print("Server is not running.")
        except requests.exceptions.RequestException as e:
            print(e)

    def connect_to_server(self):
        """
        Connect to the server and send the initial event.
        """
        g = geocoder.ip('me')
        self.body.update({
            'info': [0, 0, 0],
            'ip': g.ip,
            'latlng': g.latlng,
            'time_data': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
            'timestamp': time.time(),
            'device_model': 'Edge_LP',
            'device_id': 'LP_01'
        })
        self._send_post_request(self.url_data)

    def _send_post_request(self, url):
        """
        Send a POST request to the given URL.
        """
        try:
            if url == self.url_event:
                response = self.session.post(url, data=self.body)
            else:
                response = self.session.post(url, files=self.file, data=self.body)
        except requests.exceptions.RequestException as e:
            print(e)

    def send_event_to_server(self, data):
        """
        Send an event to the server.
        """
        self._update_body_and_file(data)
        self._send_post_request(self.url_event)
        
    def send_data_to_server(self, data):
        """
        Send data to the server.
        """
        self._update_body_and_file(data)
        
        print(2)
        print("file : ", self.file)
        print("body : ", self.body)
        self._send_post_request(self.url_data)

    def _update_body_and_file(self, data):
        """
        Update the body and file of the request with the given data.
        """
        self.body.update({ 
            'info' : data['info'],
            'time_data': datetime.datetime.fromtimestamp(data['timestamp']),
            'timestamp': data['timestamp'], 
            'TH': data['th'],
            'url_s3': upload_image_to_s3(data['frame'][1], data['info'], self.last_upload_time, self.baby_id)
        })
        self.file['frame'] = data['frame']
        
        print(1)
        print("file : ", self.file)
        print("body : ", self.body)

def upload_image_to_s3(data, info, last_upload_time, baby_id):
    """
    Upload an image to AWS S3 and return the URL of the uploaded image.
    """
    try:
        # info가 2 2 0이고, 당일 업로드한 적이 없다면 업로드 
        # 파일 이름 :  {baby_id}_stop_{timestamp}.jpg
        if info[0] == 2 and info[1] == 2 and info[2] == 0: # and not has_uploaded_today(last_upload_time):
            file_name = f"{baby_id}_stop_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
            uploaded_file_url, upload_time = upload_to_s3(file_name, data)
            last_upload_time = upload_time
            return json.dumps({'uploaded_file_url': uploaded_file_url}), 200
        # info가 2 2 *이면 업로드
        # 파일 이름 :  {baby_id}_stamp_*_{timestamp}.jpg
        elif info[0] == 2 and info[1] == 2:
            file_name = f"{baby_id}_stamp_{info[2]}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
            uploaded_file_url, upload_time = upload_to_s3(file_name, data)
            last_upload_time = upload_time
            return json.dumps({'uploaded_file_url': uploaded_file_url}), 200
    except Exception as e:
        return json.dumps({'error': str(e)}), 500
    
    
def has_uploaded_today(last_upload_time):
    """
    Check if an upload has been made today.
    """
    now = datetime.datetime.now()
    if last_upload_time.date() == now.date():
        return True
    return False

def upload_to_s3(file_name, file_data):
    """
    Upload a file to AWS S3 and return the URL of the uploaded file and the upload time.
    """
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    s3.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=file_data)
    url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{file_name}"
    upload_time = datetime.datetime.now()
    return url, upload_time