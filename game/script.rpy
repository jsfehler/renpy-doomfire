label start:
    call screen doom_fire
    return

screen doom_fire():
    add Solid('#000')
    add "doom.png" at move_logo
    add doom_fire xalign 0.5 yalign 1.0 zoom 3.0

transform move_logo:
    xalign 0.5
    yalign 1.5
    linear 7.0 yalign 0.5

init python:
    # doom_fire = c_doomfire.DoomFire(palette, pixel_distance=2, width=212, height=128)
    doom_fire = py_doomfire.DoomFire(palette, pixel_distance=2, width=212, height=128)
