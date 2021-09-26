import os
os.environ["PATH"] += os.pathsep + os.path.dirname(__file__) + os.sep + "mpv"
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import subprocess
from math import ceil
import datetime
import player as pl
from config import *
import json
from moviepy.video.io.VideoFileClip import VideoFileClip
import killdetect as kd
from easygui import fileopenbox as fpop


# initialize pygame
print("\n\nDeviate Editor v0.4a\nBy cainishraq\n\n")
pygame.init()
screen = pygame.display.set_mode((600, 900), pygame.RESIZABLE)
done = False
clock = pygame.time.Clock()

master = 0
speed = 2
markers = []
clips = []
actions = []
video_length = 1
row = 60
clicked = None
y = PAD
SAVEDIR = os.path.expandvars(SAVEDIR)


def load_video():
    file = r"C:\Users\alexa\Videos\apex.mp4" if False else fpop()
    if file == None:
        return
    global markers, clips, actions, video_length, save_f
    pl.player.play(file)
    save_f = SAVEDIR+os.sep+os.path.basename(file)+".json"
    if os.path.exists(save_f):
        with open(save_f) as save:
            markers, clips, actions = json.loads(save.read())
        print("Loaded.")


def export(iclips):
    """Trims export-marked sections into video files.

    Parameters:
        iclips (list): list of ints indicating export marker positions in seconds
    """
    
    fn, counter = input("Enter name (name_01.mp4, etc): ").replace(" ", "_"), 0
    pad = lambda x: "0"+str(x) if x < 10 else str(x)
    time = lambda x: ":".join([pad(int(x//3600)), pad(int(x%3600//60)), pad(x%60)])

    with VideoFileClip(fn) as vid:
        for clip in iclips:
            counter = pad(int(counter)+1)
            new = vid.subclip(time(max(markers, key=lambda x: x if x < clip else 0)),
                        time(min(markers, key=lambda x: x if x > clip else max(markers)+1)))
            new.write_videofile("export"+os.sep+fn+"_"+counter+".mp4")
            print("EXPORTED CLIP "+counter)
    
    print("EXPORTED ALL CLIPS, DONE")


def draw_marker(n, col, i, circle_only=False):
    _x = PAD+(screen.get_width()-PAD*2)*(n%row/row)
    _y = y+i*(HEIGHT+PAD*2)
    if n//row==i:
        if not circle_only:
            pygame.draw.rect(screen, pygame.Color(col), pygame.Rect(_x, _y, 1, HEIGHT))
        pygame.draw.circle(screen, pygame.Color(col), (_x, _y-(3.0/2)+(HEIGHT/2*int(circle_only))), RADIUS)


if not os.path.exists(SAVEDIR):
    os.mkdir(SAVEDIR)
load_video()
while not done:
    y += ((PAD - (master // row) * (HEIGHT + PAD * 2)) - y) * 0.2
    if pl.player.duration != None:
        video_length = pl.player.duration
    
    # get markers from player into timeline
    if pl.markers:
        markers += pl.markers
        pl.markers = []

    # timeline keyboard controls
    pressed = pygame.key.get_pressed()
    ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
    alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
    
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                clicked = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                if pins := markers + actions:
                    master = min(pins, key=lambda x: x if x > master else max(pins)+1)
            if event.key == pygame.K_SPACE:
                if markers:
                    pl.player.time_pos = max(markers, key=lambda x: x if x < master else 0)
            if event.key == pygame.K_w:
                master -= row
            if event.key == pygame.K_s and not ctrl_held:
                master += row
            if event.key == pygame.K_q:
                if markers:
                    marker = min(markers, key=lambda x: abs(master-x))
                    if abs(master-marker) > THRESHOLD:
                        markers.append(master*100//1/100)
                    else:
                        markers.remove(marker)
                else:
                    markers.append(master*100//1/100)
            if event.key == pygame.K_k:
                if ctrl_held:
                    print("Finding killframes.")
                    actions = kd.main(file)
                    print("All frames scanned.")
            if event.key == pygame.K_s and ctrl_held:
                with open(save_f, "w") as save:
                    save.write(json.dumps([markers, clips, actions]))
                    print("Saved.")
            if event.key == pygame.K_o and ctrl_held:
                load_video()
            if event.key == pygame.K_e:
                if ctrl_held:
                    if clips:
                        export(clips)
                else:
                    if clips:
                        clip = min(clips, key=lambda x: abs(master-x))
                        if abs(master-clip) > THRESHOLD:
                            clips.append(master*100//1/100)
                        else:
                            clips.remove(clip)
                    else:
                        clips.append(master*100//1/100)
    if pressed[pygame.K_a]:
        master -= SPEED*speed/FPS
    if pressed[pygame.K_d]:
        master += SPEED*speed/FPS
    row = min(max(1, row - pressed[pygame.K_EQUALS] + pressed[pygame.K_MINUS]), video_length)

    screen.fill(pygame.Color("#212121"))
    for i in range(max(int(master//row-2), 0), min(int(master//row+(screen.get_height()-PAD)//(HEIGHT+PAD*2)+1), ceil(video_length/row))+1):
        width = min(max(video_length - i*row, 0), row)/row
        pygame.draw.rect(screen, pygame.Color("#616161"),
                pygame.Rect(PAD, y+i*(HEIGHT+PAD*2), width*(screen.get_width()-PAD*2), HEIGHT))
        if clicked != None and PAD < clicked[0] and clicked[0] < screen.get_width() - PAD:
            if y+i*(HEIGHT+PAD*2) < clicked[1] and clicked[1] < y+i*(HEIGHT+PAD*2)+HEIGHT:
                master = i*row + row*((clicked[0]-PAD)/(screen.get_width()-PAD*2))
                clicked = None
        for action in actions:
            draw_marker(action, "#9b59b6", i)
        draw_marker(master, "#e74c3c", i)
        if pl.rn != None:
            draw_marker(pl.rn, "#3498db", i)
        for marker in markers:
            draw_marker(marker, "#f1c40f", i)
        for clip in clips:
            draw_marker(clip, "#27ae60" if (markers and min(markers) < clip and clip < max(markers)) else "#e74c3c", i, True)


    master = min(max(master, 0), video_length-1.0/FPS)
    pygame.display.flip()
    clock.tick(FPS)
