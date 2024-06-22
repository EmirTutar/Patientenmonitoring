import paho.mqtt.client as mqtt
import os
import yaml
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
smtp_server = os.environ['SMTP_SERVER']
smtp_port = int(os.environ['SMTP_PORT'])
smtp_username = os.environ['SMTP_USERNAME']
smtp_password = os.environ['SMTP_PASSWORD']
from_email = os.environ['FROM_EMAIL']
to_email = os.environ['TO_EMAIL']

mqtt_broker_address = os.environ['MQTT_DOMAIN']
mqtt_port = int(os.environ['MQTT_PORT'])
mqtt_username = os.environ['MQTT_USERNAME']
mqtt_password = os.environ['MQTT_PASSWORD']





# MQTT configuration
yaml_path = "./config.yaml"
with open(yaml_path, 'r') as file:
    config = yaml.safe_load(file)

client_id_prefix = config["client_id_prefix"]
mqtt_protocol = config["mqtt_protocol"]
mqtt_connection_success_msg = config["mqtt_connection_sucess_msg"]
fall_detected_topic_name = config['fall_detected_topic_name']
fall_detected_msg = config['fall_detected_msg']
mail_msg_success = config['mail_msg_success']
mail_msg_failed = config['mail_msg_failed']
fall_detected_msg_subject = config['fall_detected_msg_subject']

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
            send_email(fall_detected_msg)
        state = 1
    else: 
        state = 0

def send_email(message):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = fall_detected_msg_subject

    msg.attach(MIMEText(message, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(smtp_username, smtp_password)
            server.sendmail(from_email, to_email, msg.as_string())
            print(mail_msg_success)

    except Exception as e:
        print(mail_msg_failed + str(e))




# Create MQTT client instances
client = mqtt.Client(client_id=f'python-mqtt-{random.randint(0, 1000)}', protocol=mqtt.MQTTv5, transport=mqtt_protocol, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(mqtt_username, mqtt_password)

client.connect(mqtt_broker_address, mqtt_port)

client.loop_forever()
