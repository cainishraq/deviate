DEVIATE EDITOR  
==============  
  
## Concept  
  
This program is meant to be a keyboard-focused clip editor for Windows and Linux. It has a minimal interface and specialized features like Valorant kill detection to help gather clips faster. These can be exported as separate videos and imported into any other video editor until I add compositor features (including stuff like automatic music sync) and a new UI in the next version.  
  
  
## Setup  
  
### Windows  
1) Click the green "Code" button on this page then "Download ZIP" and extract  
2) [Install the latest Python 3](https://www.python.org/downloads/) (windows users enable "Add Python 3.x to PATH" in installer)  
3) Run install.bat once without admin (linux users run "pip install -r requirements.txt" in directory)  
  
  
## Tips  
  
 - [!] This is an early build so save often and send screenshots of error messages  
 - Place input videos in videos/ folder, find exported clips in export/  
 - Edit config.py with any text editor to change settings  
 - Run the editor by double-clicking timeline.py  
 - Make clips by placing markers on start and end points and placing an export pin in between  
 - When video player is focused, all [mpv keyboard/mouse controls](https://mpv.io/manual/master/) work except q/d  
  
  
## Controls
  
### Timeline
  
Ctrl+k - kill detect: generate action indicators  
  
MINUS/EQUALS - zoom out/in
  
wasd - control master playhead  
Tab - teleport master to next marker or action indicator  
Space - teleport player to the last marker before the master  
  
q - place marker at master position  
e - place export pin at master position  
  
Ctrl+o - load save for current video if exists  
Ctrl+s - create or overwrite save for current video  
Ctrl+e - export clips  
  
### Video Player

a/d - move player playhead left/right by 30 seconds

q - place marker at player position
e - place export pin at player position
