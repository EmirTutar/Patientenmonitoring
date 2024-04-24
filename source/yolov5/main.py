import torch
import paho.mqtt.client as mqtt
import numpy as np
import random
import cv2
import os
import time

# MQTT Broker Information
broker_address =  os.environ['MQTT_DOMAIN']  # Replace with your MQTT broker's address
port = int(os.environ['MQTT_PORT']) 
username = os.environ['MQTT_USERNAME']
password = os.environ['MQTT_PASSWORD']


threshold = 0.5 
fall_counter = 0
fall_threshold = 1
publish_time = 2 # 2 fps


# Callback function when connection is established
def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connected with result code "+str(reason_code))
    # Subscribe to topics if needed
    # client.subscribe("topic/to/subscribe")

# Callback function when a message is published
def on_publish(client, userdata, mid, reason_code, properties=None):
    print("Message Published")


# Create MQTT client instance
client = mqtt.Client(client_id=f'python-mqtt-{random.randint(0, 1000)}', protocol=mqtt.MQTTv5, transport="tcp", callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
# Set the callbacks
client.on_connect = on_connect
client.on_publish = on_publish


# If authentication is needed
client.username_pw_set(username, password)

# Connect to broker
client.connect(broker_address, port)


client.loop_start()

# Load model
model = torch.hub.load("ultralytics/yolov5", "custom", path="model.pt", device='cpu', trust_repo=True)

# Open videostream
cap = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)

# Specify image size
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)



topic_name = "fall_detected"
# Loop through videoframes
while cap.isOpened():
    # Read frame
    success, frame = cap.read()
    # Convert to rgb color

    if success:
        start_time = time.time()

        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Do inference
        results = model(rgb_image)
        message = "0"

        made_fall_detection = False
        df = results.pandas().xyxy[0]
        for index, row in df.iterrows():
            confidence = row['confidence']
            if confidence > threshold:
                if(row['name'] == "fall detected"):
                    made_fall_detection = True

        if made_fall_detection:
            fall_counter += 1
        else:
            fall_counter = 0
        
        if fall_counter >= fall_threshold:
             message = "1"

        client.publish("fall_detected", payload=message, qos=1)


        results.print()
        elapsed_time = time.time() - start_time
        time_to_sleep = max(0, publish_time - elapsed_time)  
        time.sleep(time_to_sleep)
        
        # Print inference result
        results.print()
    else:
        # Break after Videostream closes
        break

# Free videostream
cap.release()
