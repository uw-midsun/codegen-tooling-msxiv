import cantools
import can
import time
import random

sleep_time_s = 1
db = cantools.database.load_file('system_can.dbc')
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
            data[str(signal.name)]=random.randint(0, 64)
        print(data)
        send_message(msg,data)
        time.sleep(sleep_time_s)

def main():
    iterate_message_and_signal()

if __name__ == "__main__":
    main()

