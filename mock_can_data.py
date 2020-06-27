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
db = cantools.database.load_file('system_can.dbc')

# This can be edited depending on the CAN interface
can_bus = can.interface.Bus('vcan0', bustype='socketcan')

def send_message(msg,msg_data):
    new_data = msg.encode(msg_data)
    message = can.Message(arbitration_id=msg.frame_id, data=new_data)
    can_bus.send(message)

def iterate_message_and_signal():
    for msg in db.messages:
        data = {}
        print(msg.name)
        for signal in msg.signals:
            # Send random data for each signal
            data[str(signal.name)]=random.randint(0, 5)
        print(data)
        send_message(msg,data)
        time.sleep(sleep_time_s)

def main():
    iterate_message_and_signal()

if __name__ == "__main__":
    main()

