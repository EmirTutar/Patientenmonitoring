from gpiozero import LED, Button
from signal import pause
import paho.mqtt.client as mqtt
import random

# Pin-Definitionen
green_led = LED(20)
yellow_led = LED(21)
red_led = LED(22)
buzzer = LED(23)  # Buzzer als LED behandelt, da beide ähnlich gesteuert werden
button = Button(24, pull_up=True)  # Pull-up-Widerstand ist standardmäßig aktiviert

state = 0  # Zustandsvariable
button_pressed = False

broker_address = "atomicpisysadmin.dynv6.net"  # Replace with your MQTT broker's address
port = 1883
username = "mosquitouser"
password = "safepassword123"

# Callback function when connection is established
def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connected with result code " + str(reason_code))
    # Subscribe to topics within the on_connect callback
    client.subscribe("fall_detected")

# Callback function when a message is received
def on_message(client, userdata, message):
    global state
    global button_pressed
    print("Received message: ", str(message.payload.decode("utf-8")))
    msg = int(message.payload.decode("utf-8"))
    if msg == 0:
        state = 0
        button_pressed = False
    elif msg == 1:
        state = 1
    elif msg == 2:
        state = 2
    elif msg == 3:
        state = 3
    update_outputs()

def toggle_buzzer():
    global button_pressed
    button_pressed = not button_pressed
    buzzer_toggle()

def buzzer_toggle():
    if button_pressed:
        buzzer.off()
    else:
        if state == 1:
            buzzer.on()

def update_outputs():
    if state == 0:
        # Alles in Ordnung: Grün leuchtet
        green_led.on()
        yellow_led.off()
        red_led.off()
        buzzer.off()
    elif state == 1:
        # Alarm: Rote LED und Buzzer aktiv
        green_led.off()
        yellow_led.off()
        red_led.on()
        if not button_pressed:
            buzzer.on()
    elif state == 2:
        # Warnung: Gelbe LED
        green_led.off()
        yellow_led.on()
        red_led.off()
        buzzer.off()
    elif state == 3:
        # Exit: Alle LEDs und Buzzer ausschalten und Programm beenden
        green_led.off()
        yellow_led.off()
        red_led.off()
        buzzer.off()
        print("Exiting...")
        client.disconnect()
        exit(0)

button.when_pressed = toggle_buzzer

# Create MQTT client instance
client = mqtt.Client(client_id=f'python-mqtt-{random.randint(0, 1000)}', protocol=mqtt.MQTTv5, transport="tcp", callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

# Set the callbacks
client.on_connect = on_connect
client.on_message = on_message

# If authentication is needed
client.username_pw_set(username, password)

# Connect to broker
client.connect(broker_address, port)
update_outputs()

try:
    client.loop_forever()
except KeyboardInterrupt:
    pass
finally:
    green_led.off()
    yellow_led.off()
    red_led.off()
    buzzer.off()
