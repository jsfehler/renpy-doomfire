label start:
    call screen doom_fire
    return

screen doom_fire:
    add Solid('#000')
    add doom_fire xalign 0.5 yalign 1.0


init python:
    doom_fire = py_doomfire.DoomFire(palette, pixel_distance=2, width=128, height=128)
