DEVIATE EDITOR  
==============  
  
## Concept  
  
This program is meant to be a keyboard-focused clip editor for Windows and Linux. It has a minimal interface and specialized features like Valorant kill detection to help gather clips faster. These can be exported as separate videos and imported into any other video editor until I add compositor features (including stuff like automatic music sync) and a new UI in the next version.  
  
  
## Setup  
  
### Windows  
1) Click the green "Code" button on this page then "Download ZIP" and extract  
2) [Install the latest Python 3](https://www.python.org/downloads/) (enable "Add Python 3.x to PATH" in installer)  
3) Run install.bat once without admin  
4) Create export/ and videos/ folders in the project directory  
  
## Linux  
1) Click the green "Code" button on this page then "Download ZIP" and extract  
2) Install Python with your package manager
3) Run "pip install -r requirements.txt" in the project directory
4) Run "mkdir export && mkdir videos" in the project directory  
  
## Tips  
  
 - [!] This is an early build so save often and send screenshots of error messages  
 - Place input videos in videos/ folder, find exported clips in export/  
 - Edit config.py with any text editor to change settings  
 - Run the editor by double-clicking timeline.py  
 - Make clips by placing markers on start and end points and placing an export pin in between  
 - When video player is focused, all [mpv keyboard/mouse controls](https://mpv.io/manual/master/) work except q/d  
  
  
## Controls
  
Ctrl+K - kill detect: generate action indicators  
  
WASD - control master playhead  
Numbers - set speed of master  
Tab - teleport master to next marker or action indicator  
Space - teleport player to the last marker before the master  
  
Q - place marker at master position (or player position if video focused)  
E - place export pin at master (or player) position  
  
Ctrl+O - load save for current video if exists  
Ctrl+S - create or overwrite save for current video  
Ctrl+E - export clips  
