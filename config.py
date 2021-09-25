FILE = "apex.mp4"

# TIMELINE
FPS = 144 # preferred framerate of timeline program
PAD = 20 # border padding in pixels
HEIGHT = 25 # height of lines/markers in pixels
MULTIPLIER = 5 # master speed multiplier
ROW = 120 # length of each line in seconds
ROWS = 9 # number of rows shown
THRESHOLD = 1 # distance from marker/clip to delete in seconds
RADIUS = 5 # clip circle radius in pixels

# KILL DETECT
ADHD = 3 # seconds of no killframes before another action indicator
WT = 230 # white rgb component threshold
PT = 0.275 # pixel percent threshold
P1 = (604, 540) # top-left pixel of kill circle bounding box
P2 = (675, 611) # bottom-right coordinate
