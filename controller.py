import soco
from soco import SoCo
from soco.data_structures import DidlAudioBroadcast
import ui
import json

class Controller:
    def __init__(self):
        self.station_dict = self.get_stations()
        # self.ip = "192.168.1.178"
        self.ip = "192.168.1.50"

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

    def start(self):
        for zone in soco.discover(interface_addr=self.ip):
            info = zone.get_speaker_info()
            if info["zone_name"] == "South":
                self.main_group = zone.group

        self.main_player = self.main_group.coordinator

        my_ui = ui.UI(self, self.station_dict)
        my_ui.start()

    def change_station(self, uri, force_radio, title):
        cur_info = self.main_player.get_current_track_info()
        is_playing = self.get_playing_state()
        print(cur_info["uri"])
        if cur_info["uri"] in uri and is_playing:
            print("Pausing: " + uri[0])
            # self.main_player.pause()
        else:
            print("Playing: " + uri[0])
            # self.main_player.play_uri(uri=uri[0], force_radio=force_radio, title=title)

    def get_current_station_name(self):
        cur_info = self.main_player.get_current_track_info()
        for station in self.station_dict:
            if cur_info["uri"] in self.station_dict[station]:
                return station
        return "Unknown"

    def get_playing_state(self):
        is_stopped = self.main_player.get_current_transport_info()["current_transport_state"]
        if is_stopped == "PLAYING":
            return True
        else:
            return False

    def change_volume(self, amount):
        print("Changed volume by: %d" % amount)
        self.main_player.set_relative_volume(amount)