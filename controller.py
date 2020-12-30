import logging

import soco
from soco import SoCo
from soco.data_structures import DidlAudioBroadcast
import ui
import json
import time


def get_logger(
        LOG_FORMAT="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        LOG_NAME="controller",
        LOG_FILE_INFO="var/controller.log",
        LOG_FILE_ERROR="var/controller.err"):
    log = logging.getLogger(LOG_NAME)
    log_formatter = logging.Formatter(LOG_FORMAT)

    # comment this to suppress console output
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_formatter)
    log.addHandler(stream_handler)

    file_handler_info = logging.FileHandler(LOG_FILE_INFO, mode='a')
    file_handler_info.setFormatter(log_formatter)
    file_handler_info.setLevel(logging.INFO)
    log.addHandler(file_handler_info)

    file_handler_error = logging.FileHandler(LOG_FILE_ERROR, mode='a')
    file_handler_error.setFormatter(log_formatter)
    file_handler_error.setLevel(logging.ERROR)
    log.addHandler(file_handler_error)

    log.setLevel(logging.DEBUG)

    return log

class Controller:
    def __init__(self):
        self.station_dict = self.get_stations()
        self.ip = "192.168.1.50"
        self.last_station = "Unknown"
        self.last_playing_state = False
        self.logger = get_logger()

        for zone in soco.discover(interface_addr=self.ip):
            info = zone.get_speaker_info()
            if info["zone_name"] == "South":
                self.main_group = zone.group

        self.main_player: SoCo = self.main_group.coordinator

        my_ui = ui.UI(self, self.station_dict)
        my_ui.start()

    def get_stations(self):
        with open("stations.json") as file:
            data = json.load(file)
            return data

    def change_station(self, uri, force_radio, title):
        try:
            cur_info = self.main_player.get_current_track_info()
            is_playing = self.get_playing_state()
            if cur_info["uri"] in uri and is_playing:
                self.main_player.pause()
            else:
                self.main_player.play_uri(uri=uri[0], force_radio=force_radio, title=title)
        except Exception:
            self.logger.error(Exception)
            self.change_station(uri, force_radio, title)

    def get_current_station_name(self):
        try:
            cur_info = self.main_player.get_current_track_info()
            for station in self.station_dict:
                if cur_info["uri"] in self.station_dict[station]:
                    self.last_station = station
                else:
                    self.logger.debug("Unrecognized station name:")
                    self.logger.debug(station)
                    self.last_station = "Unknown"
        except Exception:
            self.logger.error(Exception)
        return self.last_station

    def get_playing_state(self):
        try:
            is_stopped = self.main_player.get_current_transport_info()["current_transport_state"]
            if is_stopped == "PLAYING":
                self.last_playing_state = True
            else:
                self.last_playing_state = False
        except Exception:
            self.logger.error(Exception)
        return self.last_playing_state

    def change_volume(self, amount):
        print("Changed volume by: %d" % amount)
        self.main_player.set_relative_volume(amount)
