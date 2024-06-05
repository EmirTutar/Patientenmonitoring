FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y python3-pip

WORKDIR /usr/src/app


COPY  requirements.txt .
RUN pip install -r requirements.txt


COPY main.py .


COPY config.yaml .


CMD ["python3","-u", "main.py"]