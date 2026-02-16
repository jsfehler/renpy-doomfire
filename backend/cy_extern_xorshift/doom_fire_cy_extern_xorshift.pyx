cdef extern from "../c_xorshift/main.h":
    void c_setup_height_map "setup_height_map"(size_t width, size_t height)
    void c_spread_fire "spread_fire"(int width)
    int c_get_colour_heights "get_colour_heights"(int index)

def setup_height_map(size_t width, size_t height):
    c_setup_height_map(width, height)

def spread_fire(int width):
    c_spread_fire(width)

def get_colour_heights(int index):
    return c_get_colour_heights(index)
