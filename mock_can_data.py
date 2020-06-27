# This script automatically generates and sends CAN messages based off of the DBC file
# Ensure that you have can and cantools installed, which can be accomplished by running
# pip install -r requirements.txt
# Alternatively you could also just run
# pip install can && pip install cantools

# If you are running this script with virtual CAN ensure that it is set up first
# You can run the below commands
# sudo modprobe vcan
# sudo ip link add dev vcan0 type vcan
# sudo ip link set up vcan0

import cantools
import can
import time
import random

sleep_time_s = 1
can_messages = []

try:
    db = cantools.database.load_file('system_can.dbc')
except:
    print("Must generate DBC file first")
    print("Run make gen && make gen-dbc")

# This can be edited depending on the CAN interface
can_bus = can.interface.Bus('vcan0', bustype='socketcan')

def main():
    num_messages_to_send = int(input("Please enter the number of random CAN messages you would like to send: "))
    get_messages()
    iterate_message_and_signal(num_messages_to_send)

def get_messages():
    for msg in db.messages:
        can_messages.append(msg)

def iterate_message_and_signal(num_messages):
    num_messages_sent = 0
    while num_messages_sent < num_messages:
        msg = random.choice(can_messages)
        num_messages_sent +=1
        data = {}
        for signal in msg.signals:
            if signal.is_multiplexer:
                data[signal.name]=random.randint(0,5)
            else:
                data[signal.name]=random.randint(0, pow(2,signal.length)-1)
        send_message(msg,data)
        time.sleep(sleep_time_s)
    print(str(num_messages_sent) + " CAN messages have been sent")

def send_message(msg, msg_data):
    new_data = msg.encode(msg_data)
    message = can.Message(arbitration_id=msg.frame_id, data=new_data)
    can_bus.send(message)

if __name__ == "__main__":
    main()

