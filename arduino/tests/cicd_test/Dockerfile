FROM python:3.10.12-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "main.py"]

docker build -t your_image .
docker run -it --device /dev/video0 --device=/dev/ttyACM0 your_image