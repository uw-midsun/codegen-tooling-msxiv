# This script recieves CAN data and sends it to FRED with MQTT

# If you are running this script with virtual CAN ensure that it is set up first
# You can run the below commands
# sudo modprobe vcan
# sudo ip link add dev vcan0 type vcan
# sudo ip link set up vcan0

import cantools
import can
import os
import paho.mqtt.client as mqtt
import json
from datetime import datetime

can_bus = can.interface.Bus('vcan0', bustype='socketcan')
db = cantools.database.load_file('system_can.dbc')
broker = "broker.hivemq.com"
client = mqtt.Client()

def on_connect(client,userdata,flags,rc):
    if rc==0:
        print("Successfully connected")
    else:
        print("Bad connection returned code=",rc)

def connect():
    client.on_connect=on_connect
    client.connect(broker,1883,60)
    client.loop_start()

def decode_can_message():
    message = can_bus.recv()
    decoded = db.decode_message(message.arbitration_id, message.data)
    decoded['datetime'] = str(datetime.fromtimestamp(message.timestamp))
    decoded['name'] = db.get_message_by_frame_id(message.arbitration_id).name
    decoded['sender'] = db.get_message_by_frame_id(message.arbitration_id).senders[0]
    #print(decoded)
    client.publish("uwmidsun/can/test", payload=json.dumps(decoded))

def main():
    connect()
    while(True):
        decode_can_message()

if __name__ == "__main__":
    main()