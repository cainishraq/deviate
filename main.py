import os
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


print("\n\nDeviate Editor v0.3a\nBy cainishraq\n\n")
pygame.init()
screen = pygame.display.set_mode((600, 900), pygame.RESIZABLE)
done = False
clock = pygame.time.Clock()

numkeys = range(48, 58)
master = 0
speed = 2
markers = []
clips = []
actions = []
video_length = 30
clicked = None

y = PAD
fn = "saves%s.json"%(os.sep+FILE)

pl.player.play("videos"+os.sep+FILE)


def export(iclips):
    fn, counter = input("Enter name (name_01.mp4, etc): ").replace(" ", "_"), 0
    pad = lambda x: "0"+str(x) if x < 10 else str(x)
    time = lambda x: ":".join([pad(int(x//3600)), pad(int(x%3600//60)), pad(x%60)])
    with VideoFileClip("videos"+os.sep+FILE) as vid:
        for clip in iclips:
            counter = pad(int(counter)+1)
            new = vid.subclip(time(max(markers, key=lambda x: x if x < clip else 0)),
                        time(min(markers, key=lambda x: x if x > clip else max(markers)+1)))
            new.write_videofile("export"+os.sep+fn+"_"+counter+".mp4")
            print("EXPORTED CLIP "+counter)
    print("EXPORTED ALL CLIPS, DONE")


def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    target.blit(temp, location)


def draw_marker(n, c, i):
    _x = PAD+(screen.get_width()-PAD*2)*(n%ROW/ROW)
    _y = y+i*(HEIGHT+PAD*2)
    if n//ROW==i:
        pygame.draw.rect(screen, pygame.Color(c), pygame.Rect(_x, _y, 1, HEIGHT))
        pygame.draw.circle(screen, pygame.Color(c), (_x, _y-3.0/2), 3)


while not done:
    y = PAD - (master // ROW - 2) * (HEIGHT + PAD * 2)
    if pl.player.duration != None:
        video_length = pl.player.duration
    
    pressed = pygame.key.get_pressed()
    ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
    alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
    
    while pl.markers:
        markers.append(pl.markers.pop(0))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                clicked = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key in numkeys:
                speed = 10
                if (newspd := numkeys.index(event.key)) != 0:
                    speed = newspd
            if event.key == pygame.K_TAB:
                if pins := markers + actions:
                    master = min(pins, key=lambda x: x if x > master else max(pins)+1)
            if event.key == pygame.K_SPACE:
                if markers:
                    pl.player.time_pos = max(markers, key=lambda x: x if x < master else 0)
            if event.key == pygame.K_w:
                master -= ROW
            if event.key == pygame.K_s and not ctrl_held:
                master += ROW
            if event.key == pygame.K_q:
                if markers:
                    marker = min(markers, key=lambda x: abs(master-x))
                    if abs(master-marker) > THRESHOLD:
                        markers.append(master*100//1/100)
                        #print("Marked.")
                    else:
                        markers.remove(marker)
                        #print("Removed marker.")
                else:
                    markers.append(master*100//1/100)
            if event.key == pygame.K_k:
                if ctrl_held:
                    print("Finding killframes.")
                    actions = kd.main(kd.circle_coors(P1, P2))
                    print("All frames scanned.")
            if event.key == pygame.K_s and ctrl_held:
                with open(fn, "w") as save:
                    save.write(json.dumps([markers, clips, actions]))
                    print("Saved.")
            if event.key == pygame.K_o and ctrl_held:
                if os.path.exists(fn):
                    with open(fn) as save:
                        markers, clips, actions = json.loads(save.read())
                    print("Loaded.")
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
                    print("Marked for export.")
    if pressed[pygame.K_a]:
        master -= MULTIPLIER*speed/FPS
    if pressed[pygame.K_d]:
        master += MULTIPLIER*speed/FPS

    screen.fill(pygame.Color("#212121"))
    for i in range(max(int(master//ROW-2), 0), min(int(master//ROW+ROWS+1), ceil(video_length//ROW))+1):
        width = min(max(video_length - i*ROW, 0), ROW)/ROW
        pygame.draw.rect(screen, pygame.Color("#616161"),
                pygame.Rect(PAD, y+i*(HEIGHT+PAD*2), width*(screen.get_width()-PAD*2), HEIGHT))
        if clicked != None and PAD < clicked[0] and clicked[0] < screen.get_width() - PAD:
            if y+i*(HEIGHT+PAD*2) < clicked[1] and clicked[1] < y+i*(HEIGHT+PAD*2)+HEIGHT:
                master = i*ROW + ROW*((clicked[0]-PAD)/(screen.get_width()-PAD*2))
                clicked = None
                print("Moved master to Row "+str(i+1))
        screen.blit(pygame.font.SysFont("comicsansms", 40).render(str(i+1), True, pygame.Color("#212121")), (PAD*2, y+i*(HEIGHT+PAD*2)))
        for action in actions:
            draw_marker(action, "#9b59b6", i)
        draw_marker(master, "#e74c3c", i)
        if pl.rn != None:
            draw_marker(pl.rn, "#3498db", i)
        for marker in markers:
            draw_marker(marker, "#f1c40f", i)
        for clip in clips:
            color = "#e74c3c"
            if (markers and min(markers) < clip and clip < max(markers)):
                color = "#27ae60"
            if clip//ROW == i:
                pygame.draw.circle(screen, pygame.Color(color), (PAD+(screen.get_width()-PAD*2)*(clip%ROW/ROW), y+i*(HEIGHT+PAD*2)+HEIGHT/2), RADIUS)

    master = min(max(master, 0), video_length)
    pygame.display.flip()
    clock.tick(FPS)
