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
        self.url_check = f'http://{self.ip}:{self.port}/check'
        
        self.session = requests.Session()
        self.file = {}
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
            'detail': '',
            'status': None,
        }
        self.connect_to_server()


    def is_requested(self):
        """Check if the server is running."""
        try:
            # Create a timestamp
            timestamp = datetime.datetime.now().isoformat()

            # Send a POST request with the timestamp in the body
            response = self.session.post(self.url_check, data=json.dumps({'timestamp': timestamp}), headers={'Content-Type': 'application/json'})

            if response.status_code == 200:
                # Parse the response body as JSON
                data = response.json()

                # Get the currentStatus value
                currentStatus = data

                if currentStatus:
                    print("Server is running and currentStatus is True.")
                    return True
                else:
                    print("Server is running but currentStatus is False.")
                    return False
            else:
                print("Server is not running.")
        except requests.exceptions.RequestException as e:
            print(e)

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

    def send_post_without_request(self, url):
        """Send a POST request to the given URL."""
        try:
            print("Body before sending request: ", self.body)
            response = self.session.post(url, files=self.file, data=self.body)
        except requests.exceptions.RequestException as e:
            print(e)


    def send_post_request(self, url):
        """Send a POST request to the given URL."""
        try:
            # print("Body before sending request: ", self.body)
            response = self.session.post(url, files=self.file, data=self.body)
        except requests.exceptions.RequestException as e:
            print(e)


    def send_event_to_server(self, data):
        """Send an event to the server."""
        self.update_body_and_file(data)
        print("Sending event to server...")
        self.send_post_without_request(self.url_event)
        
    def send_data_to_server(self, data):
        """Send data to the server."""
        print("Sending data to server...")
        self.update_body_and_file(data)
        self.send_post_request(self.url_data)

    def update_body_and_file(self, data):
        """Update the body and file with the given data."""
        
        # print(data)
        self.body.update({ 
            'index':data['index'],
            'time_data': datetime.datetime.fromtimestamp(data['timestamp']),
            'timestamp': data['timestamp'], 
            'event_type': data['event_type'], 
            'detail': data['detail'],
            'TH': data['th'],
            'url_s3': upload_image_to_s3(data['frame'][1])
        })
        self.file['frame'] = data['frame']
        print(self.file)

def upload_image_to_s3(data):
    """Upload an image to S3 and return the URL."""
    try:
        uploaded_file_url = upload_to_s3('2_pro_2024_03_31.jpg', data)
        return json.dumps({'uploaded_file_url': uploaded_file_url}), 200
    except Exception as e:
        return json.dumps({'error': str(e)}), 500

def upload_to_s3(file_name, file_data):
    """Upload a file to S3 and return the URL."""
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)
    s3.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=file_data)
    url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{file_name}"
    # print("Uploaded file URL:", url)
    return url