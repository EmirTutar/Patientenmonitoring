FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y python3-pip libgl1-mesa-glx libglib2.0-0  libxcb-cursor0 libegl1-mesa libqt6core6 libqt6gui6 libqt6widgets6 libxcb-util1 libsm6

WORKDIR /usr/src/app

COPY  requirements.txt .

RUN pip install -r requirements.txt


COPY video.py .

COPY config.yaml .


CMD ["python3", "video.py"]
