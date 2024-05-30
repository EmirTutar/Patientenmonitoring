import cv2
import numpy as np
import paho.mqtt.client as mqtt
import random
import os
import threading
import yaml


# MQTT Broker Information
broker_address =  os.environ['MQTT_DOMAIN']  # Replace with your MQTT broker's address
port = int(os.environ['MQTT_PORT']) 
username = os.environ['MQTT_USERNAME']
password = os.environ['MQTT_PASSWORD']

yaml_path = "./config.yaml"
with open(yaml_path, 'r') as file:
    config = yaml.safe_load(file)

client_id_prefix = config["client_id_prefix"]
mqtt_prtocol = config["mqtt_prtocol"]
mqtt_connection_sucess_msg = config["mqtt_connection_sucess_msg"]
video_topic_name = config["video_topic_name"]

def on_message(client, userdata, message):
        
        nparr = np.frombuffer(message.payload, np.uint8)
        frame = cv2.imdecode(nparr,  cv2.IMREAD_COLOR)

        cv2.imshow('recv', frame)
        cv2.waitKey(1)



# Create MQTT client instance
client = mqtt.Client(client_id=client_id_prefix+str({random.randint(0, 1000)}), protocol=mqtt.MQTTv5, transport=mqtt_prtocol, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
# Set the callbacks
on_connect = lambda client, userdata, flags, rc: print(mqtt_connection_sucess_msg+str(rc))
client.on_message = on_message


# If authentication is needed
client.username_pw_set(username, password)

# Connect to broker
client.connect(broker_address, port)

client.subscribe(video_topic_name)

target=client.loop_forever()


