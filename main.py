import soco

main_group = None
main_player = None

paradise_radio = "aac://https://stream.radioparadise.com/mellow-320"

for zone in soco.discover(interface_addr="192.168.1.50"):
    info = zone.get_speaker_info()
    if info["zone_name"] == "South":
        main_group = zone.group

main_player = main_group.coordinator

main_player.play_uri(paradise_radio)
