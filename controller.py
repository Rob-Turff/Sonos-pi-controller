import soco
from soco import SoCo
from soco.data_structures import DidlAudioBroadcast
import ui

main_group = None
main_player: SoCo = None

paradise_radio = "aac://https://stream.radioparadise.com/mellow-320"

# ip = "192.168.1.178"
ip = "192.168.1.50"

def start():
    global main_group, main_player
    for zone in soco.discover(interface_addr=ip):
        info = zone.get_speaker_info()
        if info["zone_name"] == "South":
            main_group = zone.group

    main_player = main_group.coordinator

    stations = main_player.music_library.get_favorite_radio_stations()
    station_dict = {"BBC Radio 4" : "", "Radio Paradise Direct" : "", "Radio Paradise Mellow" : "", "Radio Paradise Rock" : "", "Radio Paradise World" : "", "Exmouth AiR" : ""}
    station: DidlAudioBroadcast
    for station in stations:
        if station.title in station_dict:
            station_dict[station.title] = station.get_uri()

    ui.start(station_dict)

def change_station(uri):
        print(main_player.get_current_track_info())
        # main_player.play_uri(uri)