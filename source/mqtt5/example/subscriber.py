import paho.mqtt.client as mqtt
import random
import os 

# MQTT Broker Information
broker_address =  os.environ['MQTT_DOMAIN']  # Replace with your MQTT broker's address
port = int(os.environ['MQTT_PORT']) 
username = os.environ['MQTT_USERNAME']
password = os.environ['MQTT_PASSWORD']

# Callback function when connection is established
def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connected with result code "+str(reason_code))
    # Subscribe to topics
    client.subscribe("topic/to/publish")

# Callback function when a message is received
def on_message(client, userdata, message):
    print("Received message: ", str(message.payload.decode("utf-8")))

# Create MQTT client instance
client = mqtt.Client(client_id=f'python-mqtt-{random.randint(0, 1000)}', protocol=mqtt.MQTTv5, transport="tcp", callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
# Set the callbacks
client.on_connect = on_connect
client.on_message = on_message

# If authentication is needed
client.username_pw_set(username, password)

# Connect to broker
client.connect(broker_address, port)

# Start the loop
client.loop_forever()

