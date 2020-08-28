label start:
    call screen select_doomfire
    return


init python:
    c_doomfire = c_doomfire.DoomFire(palette, pixel_distance=1, width=212, height=128)

    py_doomfire = py_doomfire.DoomFire(palette, pixel_distance=1, width=212, height=128)

    import doom_fire_cy
    cy_doomfire = doom_fire_cy.DoomFire(palette, pixel_distance=1, width=212, height=128)


screen select_doomfire():
    vbox:
        textbutton "Python" action Show("doomfire", displayable=py_doomfire)
        textbutton "Python + ctypes" action Show("doomfire", displayable=c_doomfire)


screen doomfire(displayable):
    tag doomfire

    add Solid('#000')
    add "doom.png" at move_logo
    add displayable xalign 0.5 yalign 1.0 zoom 3.0


transform move_logo:
    xalign 0.5
    yalign 1.5
    linear 7.0 yalign 0.5
