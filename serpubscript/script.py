import json
from random import random
from time import sleep

import serial
from paho.mqtt import client as mqtt


# 172.17.0.1 is the default IP address for the host running the Docker container
# Change this value if Brewblox is installed on a different computer
HOST = '10.0.0.96'

# 1883 is the default port for MQTT, but this can be changed in brewblox env settings.
MQTT_PORT = 1883

# This is a constant value. You never need to change it.
HISTORY_TOPIC = 'brewcast/history'

# The history service is subscribed to all topics starting with 'brewcast/history'
# We can make our topic more specific to help debugging
TOPIC = HISTORY_TOPIC + '/serpubcript'


# This is the default serial port
SERIAL_PORT = '/dev/ttyACM0'

# Create an MQTT client
client = mqtt.Client()

# You may need to further configure settings
# See the pyserial documentation for more info
# https://pythonhosted.org/pyserial/pyserial_api.html#classes
ser = serial.Serial(port=SERIAL_PORT,
                    baudrate=115200,
                    timeout=1)

try:
    client.connect_async(host=HOST, port=MQTT_PORT)
    client.loop_start()

    while True:
        # https://www.brewblox.com/dev/reference/history_events.html
        value = json.loads(ser.readline().decode().rstrip())
        # value = json.loads(value)
        print(f'recv {value}')

        message = {
            'key': 'serpubscript',
            'data': {
                'sensor_name': value}
        }

        client.publish(TOPIC, json.dumps(message))
        print(f'sent {message}')
        sleep(5)

finally:
    client.loop_stop()
    ser.close()
