from nio import AsyncClient, MatrixRoom, RoomMessageText
import paho.mqtt.client as mqtt
import os
import random
import yaml
import asyncio




mqtt_broker_address = os.environ['MQTT_DOMAIN']
mqtt_port = int(os.environ['MQTT_PORT'])
mqtt_username = os.environ['MQTT_USERNAME']
mqtt_password = os.environ['MQTT_PASSWORD']

yaml_path = "./config.yaml"
with open(yaml_path, 'r') as file:
    config = yaml.safe_load(file)

client_id_prefix = config["client_id_prefix"]
mqtt_protocol = config["mqtt_protocol"]
mqtt_connection_success_msg = config["mqtt_connection_sucess_msg"]
fall_detected_topic_name = config['fall_detected_topic_name']
fall_detected_msg = config['fall_detected_msg']
matrix_msg_success = config['matrix_msg_success']
matrix_msg_failed = config['matrix_msg_failed']

matrix_homeserver_url = os.environ.get("MATRIX_HOMESERVER_URL")
matrix_user_id = os.environ.get("MATRIX_USER_ID")
matrix_password = os.environ.get("MATRIX_PASSWORD")
matrix_room_id = os.environ.get("MATRIX_ROOM_ID")




state = 0
# Callback function when connection is established
def on_connect(client, userdata, flags, reason_code, properties=None):
    print(mqtt_connection_success_msg +str(reason_code))
    # Subscribe to topics within the on_connect callback
    client.subscribe(fall_detected_topic_name)

# Callback function when a message is received
def on_message(client, userdata, message):
    print("Received message: ", str(message.payload.decode("utf-8")))
    global state
    if int(message.payload.decode("utf-8")) == 1:
        if state == 0:
            asyncio.run(send_matrix_message(fall_detected_msg))
        state = 1
    else: 
        state = 0



async def send_matrix_message(message):
    client = AsyncClient(matrix_homeserver_url, matrix_user_id)
    try:
        # Login to Matrix
        await client.login(matrix_password)

        # Send message
        await client.room_send(
            room_id=matrix_room_id,
            message_type="m.room.message",
            content={
        "msgtype": "m.text",
        "format": "org.matrix.custom.html",
        "body": message,
        "formatted_body": message
    },
            
        )
        print(matrix_msg_success)
    except Exception as e:
        print(matrix_msg_failed + str(e))
    finally:
        # Close the client connection
        await client.close()

# Create MQTT client instance
client = mqtt.Client(client_id=f'python-mqtt-{random.randint(0, 1000)}', protocol=mqtt.MQTTv5, transport="tcp", callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(mqtt_username, mqtt_password)

client.connect(mqtt_broker_address, mqtt_port)

client.loop_forever()




