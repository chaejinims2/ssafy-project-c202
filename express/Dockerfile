## Python 애플리케이션을 위한 기본 이미지를 가져옵니다.
#FROM python:3.9-slim
#
## Python 애플리케이션에 필요한 파일을 복사합니다.
#WORKDIR /app/python-logic/common/edge_lp3
#COPY ./workspace/python-logic/common/edge_lp3/main.py /app/python-logic/common/edge_lp3/main.py
#COPY ./workspace/python-logic/common/edge_lp3/requirements.txt /app/python-logic/common/edge_lp3/requirements.txt
#
## Python 의존성을 설치합니다.
#RUN pip install -r /app/python-logic/common/edge_lp3/requirements.txt
#
#CMD ["python3", "main.py"]

# 베이스 이미지로 node와 python을 포함하는 이미지를 사용합니다.
FROM node:21.7.1-alpine

# Node.js 애플리케이션에 필요한 파일을 복사합니다.
WORKDIR /app/express-network
COPY ./index.js /app/express-network/index.js
COPY ./package.json /app/express-network/package.json

# Node.js 패키지를 설치합니다.
RUN npm install

# 실행할 명령을 지정합니다.
CMD ["node", "index.js"]
# 실행할 명령을 지정합니다.


