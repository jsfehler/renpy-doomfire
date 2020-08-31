![Screenshot](/screenshot.png?raw=true "Screenshot")

# renpy-doomfire
Doom's fire effect, in Ren'py

Source article: https://fabiensanglard.net/doom_fire_psx/index.html

There are three versions, one written entirely in Ren'Py flavoured Python, another that moves parts of the logic to C and consumes it via the ctypes library, and yet another that uses Cython.

The ctypes version is compiled as a Windows DLL. The source code is available in the `c_fire` directory if you want to compile it for MacOS/Linux. The compiled file should be placed in the `game` directory.

The Cython source is available in the `cy_fire` directory. The compiled file should be placed above the `game` directory.

All versions hard-code a redraw every 0.05 seconds. Pixel shifting occurs every redraw.
A potential improvement would be redraw immediately and shift pixels based on a speed value. Might melt your computer, though.

### How to run the demo

A built game is available in the build directory.

You can also create a new Ren'Py project and drop the files in there.

### Notes
  - Using a zoom transform is a cheap way to cover more of the screen. 

  - Why not numpy? Not compatible without customising Ren'py.

  - Ren'Py currently uses Python2.7. Your Cython has to build for 2.7 as well.

  - Ren'Py doesn't use Pygame, it uses https://github.com/renpy/pygame_sdl2. You could adapt the logic here to vanilla Pygame, but it's not a drop-in solution.

  - My C skills are beginner level. If you're stupid enough to use that code in a real game without testing it first that's your fault, not mine.

Python
------
| Pros | Cons |
|------|------|
| Easy to read | It'll melt your computer |
| Easy to modify |

Ctypes
------
| Pros | Cons |
|------|------|
| Fast | Logic is now split in two files |
| Writing C makes me feel like a big man | Has to be compiled |

Cython
------
| Pros | Cons |
|------|------|
| Not too difficult to read | Has to be compiled |
| Fast | Can't write it inside Ren'Py, has to be imported |
