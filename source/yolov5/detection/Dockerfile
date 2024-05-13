FROM arm64v8/ubuntu:22.04

RUN apt-get update && \
    apt-get install -y python3-pip libgl1-mesa-glx libglib2.0-0 

WORKDIR /usr/src/app

COPY  requirements.txt .

RUN pip install -r requirements.txt


COPY main.py .


COPY model.pt .

COPY config.yaml .

CMD ["python3", "main.py"]
