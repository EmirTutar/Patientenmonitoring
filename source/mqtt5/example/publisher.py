import paho.mqtt.client as mqtt
import time
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

# Start the loop
client.loop_start()

try:
    while True:
        # Publish a message
        message = "Hello, MQTT!"
        client.publish("topic/to/publish", payload=message, qos=1)
        print("Publishing message: ", message)
        time.sleep(2)  # Publish message every 2 seconds
except KeyboardInterrupt:
    # Disconnect gracefully on KeyboardInterrupt
    client.disconnect()
    print("Disconnected")

