import os
import time
from datetime import datetime

import controller


def connect(host='http://google.com'):
    return True
    # response = os.system("ping -c 1 192.168.1.50")
    # if response == 0:
    #     return True
    # else:
    #     return False


def start():
    while not connect():
        print("Failed To Connect at: ")
        print(datetime.now())
        time.sleep(10)

    os.chdir("/usr/share/Sonos-pi-controller")
    my_controller = controller.Controller()


time.sleep(1)
start()
