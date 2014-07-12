i3-shiftworkspace
=================
command line tool to push your workspaces to the left (or the right) in i3 wm.

When using i3 you often open new workspaces to do new stuff, and eventually end up only using workspaces from 6 to 8. Manually bringing them to 0-2 can be quite a pain. This script will automatically move workspaces to the left as long as empty workspaces are available.
Optional arguments are available to shift to the right or define exact number of shifts allowed. 
See `./i3-shiftworkspaces -h` for complete list

Get Started
=================
Retrieve
    
    $ git clone https://github.com/emilecaron/i3-shiftworkspace.git

Run

    $ cd i3-shiftworkspace && ./i3shiftworkspaces.py

Done. 

Dependencies
=================
[i3-py](http://github.com/ziberna/i3-py) (can retrieve with pip)

The rest is python3, using argparse and logging modules.
