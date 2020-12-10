from soco import SoCo
import soco

main_group = None
main_player = None

for zone in soco.discover(interface_addr="192.168.1.178"):
    info = zone.get_speaker_info()
    if info["zone_name"] == "South":
        main_group = zone.group

main_player = main_group.coordinator

print(main_player.get_current_track_info())
print(main_player.get_current_transport_info())
print(main_player.music_library.get_favorite_radio_stations(start=0, max_items=100))
