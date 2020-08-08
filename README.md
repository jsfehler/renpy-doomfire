![Screenshot](/screenshot.png?raw=true "Screenshot")

# renpy-doomfire
Doom's fire effect, in Ren'py

Source article: https://fabiensanglard.net/doom_fire_psx/index.html

There are two versions, one written entirely in python, another that moves parts of the logic to C and consumes it via the ctypes library.

The pure python version is intended as an example of the math involved, but running it may melt your computer.

The C version is compiled as a Windows DLL. The source code is available in the c_fire directory if you want to compile it for MacOS/Linux.
This version uses roughly half as much CPU as the python version.

Both versions hard-code a redraw every 0.05 seconds. Pixel shifting occurs every redraw.
A potential improvement would be redraw immediately and shift pixels based on a speed value. Might melt your computer, though.