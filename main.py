import os
import time
from datetime import datetime
import socket

import controller

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def connect(ip):
    response = os.system("ping -c 1 " + ip)
    if response == 0:
        return True
    else:
        return False


def start():
    ip = get_ip()
    while not connect(ip):
        time.sleep(10)
        print("Failed To Connect to: " + ip + " at: ")
        print(datetime.now())
        ip = get_ip()

    # os.chdir("/usr/share/Sonos-pi-controller")
    my_controller = controller.Controller(ip)


time.sleep(1)
start()
