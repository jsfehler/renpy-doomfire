import itertools
import random

import pygame_sdl2.gfxdraw as gfxdraw

import renpy.exports as renpy


cdef class BaseDoomFire:
    cdef tuple palette
    cdef int pixel_distance, width, height, fire_width, fire_height

    cdef tuple pixel_screen_positions
    cdef list pixel_list
    cdef tuple fire_positions

    def __init__(self, tuple palette, int pixel_distance, int width, int height, **kwargs):
        """Generate an upwards fire animation by shifting pixel colours.

        Arguments:
            palette (tuple): Every colour to cycle through.
            pixel_distance (int): Distance on screen between each pixel.
        """
        super(BaseDoomFire, self).__init__(**kwargs)

        self.palette = palette
        self.pixel_distance = pixel_distance

        # Size of the render
        self.width = width * self.pixel_distance
        self.height = height * self.pixel_distance

        # Number of pixels, across and wide
        self.fire_width = width
        self.fire_height = height

        # Setup lists that records each pixel's colour height
        self.setup_height_map()

        # We already know where every pixel will be drawn on screen, so record that ahead of time
        # The three attributes for each pixel are:
        #   colour_index: Index for the list that stores the current height of every pixel
        #   xpos: physical x position of the pixel
        #   ypos: physical y position of the pixel
        self.pixel_screen_positions = tuple(
            ((y * width + x, x * self.pixel_distance, y * self.pixel_distance) for y, x in itertools.product(range(height), range(width)))
        )

    def setup_height_map(self):
        """Build two lists:
            - pixel_list: Values for every pixel's current color height
            - fire_positions: Indexes for every pixel in pixel_list
        """
        cdef int i

        # Set heights for entire drawable area to 0
        self.pixel_list = [0 for i in range(self.fire_width * self.fire_height)]

        # Set bottom line to last colour in palette
        for i in range(self.fire_width):
            self.pixel_list[((self.fire_height - 1) * self.fire_width) + i] = len(self.palette) - 1

        self.fire_positions = tuple(
            (y * self.fire_width + x for x, y in itertools.product(range(self.fire_width), range(1, self.fire_height)))
        )

    def spread_fire(self):
        """Move each pixel's color height."""
        cdef int source, pixel, r_index, dst

        for source in self.fire_positions:
            pixel = self.pixel_list[source]

            if pixel == 0:
                self.pixel_list[source - self.fire_width] = 0
            else:
                # Get a random number between 0 and 3
                r_index = int((random.random() * 4.0))

                dst = source - r_index + 1

                self.pixel_list[dst - self.fire_width] = pixel - (r_index & 1)

    def draw_pixels(self, surface):
        """Draw all the pixels to a surface.

        Arguments:
            surface: Pygame surface to draw on.
        """
        # Make local namespaces to speed up the for loop
        palette = self.palette
        pixel = gfxdraw.pixel

        pixel_list = self.pixel_list

        cdef int colour_index, xpos, ypos, height_index

        for colour_index, xpos, ypos in self.pixel_screen_positions:
            # Get colour height of current pixel
            height_index = pixel_list[colour_index]

            # Don't draw the pixel if it's the highest colour.
            if height_index:
                pixel(surface, xpos, ypos, palette[height_index])

    def render(self, int width, int height, float st, float at):
        render = renpy.Render(self.width, self.height)

        # For every pixel, move color height
        self.spread_fire()

        self.draw_pixels(render.canvas().surf)

        renpy.redraw(self, 0.05)

        return render


class DoomFire(BaseDoomFire, renpy.Displayable):
    pass
