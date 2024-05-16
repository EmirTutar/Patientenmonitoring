import torch
import paho.mqtt.client as mqtt
import numpy as np
import random
import cv2
import os
import time
import yaml


# MQTT Broker Information
broker_address =  os.environ['MQTT_DOMAIN']  # Replace with your MQTT broker's address
port = int(os.environ['MQTT_PORT']) 
username = os.environ['MQTT_USERNAME']
password = os.environ['MQTT_PASSWORD']

yaml_path = "./config.yaml"
with open(yaml_path, 'r') as file:
    config = yaml.safe_load(file)


cap_prop_frame_width = config["cap_prop_frame_width"]
cap_prop_frame_height = config["cap_prop_frame_height"]
cap_prop_buffersize = config["cap_prop_buffersize"]
confidence_threshold = config['confidence_threshold']
fall_counter = config['fall_counter']
fall_threshold = config['fall_threshold']
fall_detected_topic_name = config['fall_detected_topic_name']
video_topic_name = config["video_topic_name"]
detection_class_name =  config['detection_class_name']
message_detected = config["message_detected"]
message_not_detected = config["message_not_detected"]
camera_path=  config["camera_path"]
model_name = config["model_name"]
model_type = config["model_type"]
model_device = config["model_device"]
custom_model_name = config["custom_model_name"]
client_id_prefix = config["client_id_prefix"]
mqtt_prtocol = config["mqtt_prtocol"]
mqtt_connection_sucess_msg = config["mqtt_connection_sucess_msg"]
result_confidence_column = config["result_confidence_column"]
result_name_column = config["result_name_column"]

# Create MQTT client instance
client = mqtt.Client(client_id=client_id_prefix+str({random.randint(0, 1000)}), protocol=mqtt.MQTTv5, transport=mqtt_prtocol, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
# Set the callbacks
on_connect = lambda client, userdata, flags, rc: print(mqtt_connection_sucess_msg+str(rc))


# If authentication is needed
client.username_pw_set(username, password)

# Connect to broker
client.connect(broker_address, port)


client.loop_start()

# Load model
model = torch.hub.load(model_name, model_type, path=custom_model_name, device=model_device, trust_repo=True)

# Open videostream
cap = cv2.VideoCapture(camera_path)

# Specify image size
cap.set(cv2.CAP_PROP_FRAME_WIDTH, cap_prop_frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, cap_prop_frame_height)
cap.set(cv2.CAP_PROP_BUFFERSIZE, cap_prop_buffersize)




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
        message = message_not_detected

        made_fall_detection = False
        df = results.pandas().xyxy[0]
        for index, row in df.iterrows():
            confidence = row[result_confidence_column]
            if confidence > confidence_threshold:
                if(row[result_name_column] == detection_class_name):
                    made_fall_detection = True

        if made_fall_detection:
            fall_counter += 1
        else:
            fall_counter = 0
        
        if fall_counter >= fall_threshold:
             message = message_detected

        client.publish(fall_detected_topic_name, payload=message, qos=1)
        
         

        img_str = cv2.imencode('.jpg', cv2.cvtColor(np.squeeze(results.render()), cv2.COLOR_RGB2BGR))[1].tobytes() # publish current detection as image
        client.publish(video_topic_name, payload=img_str, qos=1)

        results.print()
    else:
        # Break after Videostream closes
        break

# Free videostream
cap.release()
