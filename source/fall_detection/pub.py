import paho.mqtt.client as mqtt
import random
import time
import argparse
import threading

# MQTT Broker Konfiguration
broker_address = "atomicpisysadmin.dynv6.net"  # Replace with your MQTT broker's address
port = 1883
username = "mosquitouser"
password = "safepassword123"

# Callback-Funktion für den Verbindungsaufbau
def on_connect(client, userdata, flags, rc, properties=None):
    print("Verbunden mit dem MQTT-Broker mit dem Rückgabewert: " + str(rc))
    client.subscribe("fall_detected")

# Callback-Funktion für empfangene Nachrichten
def on_message(client, userdata, message):
    print("Nachricht empfangen: ", str(message.payload.decode("utf-8")))

# Erstelle einen MQTT-Client
client = mqtt.Client(client_id=f'python-mqtt-{random.randint(0, 1000)}', protocol=mqtt.MQTTv5, transport="tcp", callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

# If authentication is needed
client.username_pw_set(username, password)

# Connect to broker
client.connect(broker_address, port)

parser = argparse.ArgumentParser(description="Fall Detection MQTT Publisher")
parser.add_argument('state', type=int, choices=[0, 1, 2, 3], help='0: Everything okay, 1: Fall detected, 2: Fall maybe detected, 3: Exit')
args = parser.parse_args()

# Nachricht basierend auf dem Argument festlegen
def get_description(state):
    if state == 0:
        return "Everything okay"
    elif state == 1:
        return "Fall detected"
    elif state == 2:
        return "Fall maybe detected"
    elif state == 3:
        return "Exit"

state = args.state
description = get_description(state)

def publish_state(state):
    client.publish("fall_detected", str(state))
    print(f"Nachricht veröffentlicht: {state} - {description}")

publish_state(state)

def user_input_loop():
    global state
    while True:
        try:
            new_state = int(input("Geben Sie 0, 1, 2 oder 3 ein: "))
            if new_state in [0, 1, 2, 3]:
                state = new_state
                description = get_description(new_state)
                publish_state(new_state)
                if new_state == 3:
                    client.disconnect()
                    break
            else:
                print("Ungültige Eingabe, bitte 0, 1, 2 oder 3 eingeben.")
        except ValueError:
            print("Ungültige Eingabe, bitte eine Zahl eingeben.")
        time.sleep(1)

def periodic_publish_loop():
    global state
    while True:
        publish_state(state)
        time.sleep(1)

# Starte eine separate Schleife für Benutzereingaben
input_thread = threading.Thread(target=user_input_loop)
input_thread.start()

# Starte eine separate Schleife für periodische Veröffentlichungen
publish_thread = threading.Thread(target=periodic_publish_loop)
publish_thread.start()

# Starte die MQTT-Schleife
client.loop_forever()
