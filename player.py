import os
import mpv
from config import THRESHOLD

player = mpv.MPV(input_default_bindings=True, input_vo_keyboard=True, osc=True)
player.fullscreen = False
player.loop_playlist = 'inf'
player['vo'] = 'gpu'

markers = []
rn = 0

@player.property_observer('time-pos')
def time_observer(_name, value):
    global rn
    rn = value


@player.on_key_press('q')
def my_q_binding():
    global markers
    trunc = rn*100//1/100
    if markers:
        marker = min(markers, key=lambda x: abs(trunc-x))
        if abs(trunc-marker) > THRESHOLD:
            markers.append(trunc)
        else:
            markers.remove(marker)
    else:
        markers.append(trunc)
    print("Marked.")

@player.on_key_press('a')
def my_a_binding():
    player.seek(-30)


@player.on_key_press('d')
def my_d_binding():
    player.seek(30)
