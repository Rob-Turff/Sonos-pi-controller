import soco
from soco import SoCo
from soco.data_structures import DidlAudioBroadcast
import ui

class Controller:
    def __init__(self):
        self.main_group = None
        self.player: SoCo = None

        # self.paradise_radio = "aac://https://stream.radioparadise.com/mellow-320"

        # self.ip = "192.168.1.178"
        self.ip = "192.168.1.50"

    def start(self):
        for zone in soco.discover(interface_addr=self.ip):
            info = zone.get_speaker_info()
            if info["zone_name"] == "South":
                self.main_group = zone.group

        self.main_player = self.main_group.coordinator

        stations = self.main_player.music_library.get_favorite_radio_stations()
        station_dict = {"BBC Radio 4" : "", "Radio Paradise Direct" : "", "Radio Paradise Mellow" : "", "Radio Paradise Rock" : "", "Radio Paradise World" : "", "Exmouth AiR" : ""}
        station: DidlAudioBroadcast
        for station in stations:
            if station.title in station_dict:
                station_dict[station.title] = station.get_uri()

        my_ui = ui.UI(self, station_dict)
        my_ui.start()
        # self.change_station(self.paradise_radio, True)

    def change_station(self, uri, force_radio, title):
        cur_info = self.main_player.get_current_track_info()
        is_stopped = self.main_player.get_current_transport_info()["current_transport_state"]
        print(uri)
        print(cur_info["uri"])
        print(self.main_player.is_playing_radio)
        print(self.main_player.music_source)
        if cur_info["uri"] == uri and is_stopped == "PLAYING":
            print("Pausing: " + uri)
            # self.main_player.pause()
        else:
            print("Playing: " + uri)
            # self.main_player.play_uri(uri=uri, force_radio=force_radio, title=title)

    def toggle_play(self):
        is_playing = self.get_playing_state()
        if is_playing:
            print("Pausing")
            # self.main_player.pause()
        else:
            print("Playing")
            # self.main_player.play()

    def get_playing_state(self):
        is_stopped = self.main_player.get_current_transport_info()["current_transport_state"]
        if is_stopped == "PLAYING":
            return True
        else:
            return False

    def change_volume(self, amount):
        print("Changed volume by: %d" % amount)
        self.main_player.set_relative_volume(amount)