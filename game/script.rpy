label start:
    call screen select_doomfire
    return


init python:
    WIDTH = 212
    HEIGHT = 128

    c_doomfire_impl = c_doomfire.DoomFire(palette, pixel_distance=1, width=WIDTH, height=HEIGHT)

    py_doomfire_impl = py_doomfire.DoomFire(palette, pixel_distance=1, width=WIDTH, height=HEIGHT)

    cy_doomfire_impl = cy_doomfire.DoomFire(palette, pixel_distance=1, width=WIDTH, height=HEIGHT)

    cy_extern_doomfire_impl = cy_extern_doomfire.DoomFire(palette, pixel_distance=1, width=WIDTH, height=HEIGHT)

    rust_doomfire_impl = rust_doomfire.DoomFire(palette, pixel_distance=1, width=WIDTH, height=HEIGHT)


screen select_doomfire():
    vbox:
        textbutton "Pure Python." action Show("doomfire", displayable=py_doomfire_impl)
        textbutton "C backend. Loaded using ctypes." action Show("doomfire", displayable=c_doomfire_impl)
        textbutton "Cython." action Show("doomfire", displayable=cy_doomfire_impl)
        textbutton "Cython Extern." action Show("doomfire", displayable=cy_extern_doomfire_impl)
        textbutton "Rust Backend. Built using PyO3 + Maturin." action Show("doomfire", displayable=rust_doomfire_impl)


# Using a zoom transform is a cheap way to cover more of the screen.
screen doomfire(displayable):
    tag doomfire

    add Solid('#000')
    add "doom.png" at move_logo
    add displayable xalign 0.5 yalign 1.0 zoom 3.0


transform move_logo:
    xalign 0.5
    yalign 1.5
    linear 7.0 yalign 0.5
