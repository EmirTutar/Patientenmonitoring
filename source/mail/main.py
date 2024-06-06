import paho.mqtt.client as mqtt
import os
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
smtp_server = "atomicpisysadmin.dynv6.net"
smtp_port = 587 
smtp_username = "patmonsys@atomicpisysadmin.dynv6.net"
smtp_password = "PatientMonitoringSystem"
from_email = "patmonsys@atomicpisysadmin.dynv6.net"
to_email = "patmonsys@atomicpisysadmin.dynv6.net"
subject = "Fall Detected Alert"


state = 0
# Callback function when connection is established
def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connected with result code " + str(reason_code))
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
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(smtp_username, smtp_password)
            print("Logged in successfully")

            # Send the email
            server.sendmail(from_email, to_email, msg.as_string())
            print("Email sent successfully")

    except Exception as e:
        print("Failed to send email: " + str(e))

# MQTT configuration
mqtt_broker_address =  "atomicpisysadmin.dynv6.net"
mqtt_port = 1883
mqtt_username = "mosquitouser"
mqtt_password = "safepassword123"
fall_detected_topic_name = "fall_detected"
fall_detected_msg = "Fall detected! Please check immediately."

# Create MQTT client instances
client = mqtt.Client(client_id=f'python-mqtt-{random.randint(0, 1000)}', protocol=mqtt.MQTTv5, transport="tcp", callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(mqtt_username, mqtt_password)

client.connect(mqtt_broker_address, mqtt_port)

client.loop_forever()
