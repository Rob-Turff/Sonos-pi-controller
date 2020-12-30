import controller
import os
import time
import urllib.request
from datetime import datetime

def connect(host='http://google.com'):
	response = os.system("ping -c 1 192.168.1.50" )
	if response == 0:
		return True
	else:
		return False


def start(self):
	while not connect():
		time.sleep(10)
		print("Failed To Connect at: ")
		print(datetime.now())

	os.chdir("/usr/share/Sonos-pi-controller")
	my_controller = controller.Controller()


time.sleep(10)
start()
