FROM arm64v8/ubuntu:22.04

RUN apt-get update && \
    apt-get install -y python3-pip

WORKDIR /usr/src/app


COPY  requirements.txt .
RUN pip install -r requirements.txt


COPY main.py .


CMD ["python3", "main.py"]