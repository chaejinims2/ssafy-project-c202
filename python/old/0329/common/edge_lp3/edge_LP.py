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
    def __init__(self, ip, port, baby_id):
        self.ip = ip
        self.port = port
        self.baby_id = baby_id
        self.url_data = f'http://{self.ip}:{self.port}/data'
        self.url_event = f'http://{self.ip}:{self.port}/event'
        self.session = requests.Session()
        self.file = None
        self.body = {
            'baby_id':  self.baby_id,
            'ip': None,
            'latlng': None,
            'index':0,
            'datetime': '2021-03-25 12:00:00.000000',
            'timestamp': 1711873161.4333634,
            'event_type': 0,
            'device_model': None,
            'device_id': None,
            'TH' : [0., 0.],
            'url_s3' : None,
            'detail': ''
        }
        self.connect_to_server()
        
    def connect_to_server(self):
        """Connect to the server and update the body with the connection details."""
        print("Connecting to server...")
        g = geocoder.ip('me')
        self.body.update({
            'index': 0,
            'ip': g.ip,
            'latlng': g.latlng,
            'time_data': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
            'timestamp': time.time(),
            'device_model': 'Edge_LP',
            'device_id': 'LP_01'
        })
        self.send_post_request(self.url_event)

    def send_post_request(self, url):
        """Send a POST request to the given URL."""
        try:
            response = self.session.post(url, files=self.file, data=self.body)
        except requests.exceptions.RequestException as e:
            print(e)

    def send_event_to_server(self, data):
        """Send an event to the server."""
        self.update_body_and_file(data)
        self.send_post_request(self.url_event)

    def send_data_to_server(self, data):
        """Send data to the server."""
        print("Sending data to server...")
        self.update_body_and_file(data)
        self.send_post_request(self.url_data)

    def update_body_and_file(self, data):
        """Update the body and file with the given data."""
        self.body.update({ 
            'index':data['index'],
            'time_data': data['time_data'],
            'timestamp': data['timestamp'], 
            'event_type': data['event_type'], 
            'detail': data['detail'],
            'TH': data['th'],
            'url_s3': upload_image_to_s3(data['image_data'])
        })
        self.file.update(data['frame'])

def upload_image_to_s3(data):
    """Upload an image to S3 and return the URL."""
    try:
        with open('./image.jpg', 'rb') as file:
            file_data = data
        uploaded_file_url = upload_to_s3('2_pro_2024_03_31.jpg', file_data)
        return json.dumps({'uploaded_file_url': uploaded_file_url}), 200
    except Exception as e:
        return json.dumps({'error': str(e)}), 500

def upload_to_s3(file_name, file_data):
    """Upload a file to S3 and return the URL."""
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    s3.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=file_data)
    url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{file_name}"
    print("Uploaded file URL:", url)
    return url