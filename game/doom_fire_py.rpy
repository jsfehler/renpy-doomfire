init -1000 python in py_doomfire:
    import itertools
    import random

    import pygame_sdl2.gfxdraw as gfxdraw


    class DoomFire(renpy.Displayable):
        def __init__(self, palette, pixel_distance, width, height, **kwargs):
            """Generate an upwards fire animation by shifting pixel colours.
            
            Arguments:
                palette (tuple): Every colour to cycle through.
                pixel_distance (int): Distance on screen between each pixel.
            """
            super(DoomFire, self).__init__(**kwargs)

            self.palette = palette
            self.pixel_distance = pixel_distance

            # Size of the render
            self.width = width * self.pixel_distance
            self.height = height * self.pixel_distance

            self.fire_width = width
            self.fire_height = height

            # Setup lists that record the pixel colour data
            self.setup_fire()

            # We already know where every pixel will be placed on screen, so record that ahead of time
            self.pixel_positions = []
            for y, x in itertools.product(range(height), range(width)):
                index = y * width + x
                self.pixel_positions.append(
                    (index, x * self.pixel_distance, y * self.pixel_distance)
                )

            # Vain attempt to get a bit more speed
            self.pixel_positions = tuple(self.pixel_positions)

        def setup_fire(self):
            """Build two lists:
                - Hold the current colour height value of every pixel
                - 
            """
            # Values for every pixel's color height
            self.pixel_list = []

            # Set whole area to 0
            for i in range(self.fire_width * self.fire_height):
               self.pixel_list.append(0)
                
            # Set bottom line to 37
            for i in range(self.fire_width):
                self.pixel_list[((self.fire_height - 1) * self.fire_width) + i] = 36

            self.fire_positions = []
            for x, y in itertools.product(range(self.fire_width), range(1, self.fire_height)):
                self.fire_positions.append(y * self.fire_width + x)

        def spread_fire(self):
            """Move color height"""
            for source in self.fire_positions:
                pixel = self.pixel_list[source]
               
                if pixel == 0:
                    self.pixel_list[source - self.fire_width] = 0
                else:
                    r_index = int(round((random.random() * 3.0))) & 3
                   
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

            for colour_index, xpos, ypos in self.pixel_positions:
                # Get colour height of current pixel
                height_index = pixel_list[colour_index]

                # Don't draw the pixel if it's the highest colour.
                if height_index:
                    pixel(surface, xpos, ypos, palette[height_index])

        def render(self, width, height, st, at):
            render = renpy.Render(self.width, self.height)

            # For every pixel, move color height
            self.spread_fire()

            self.draw_pixels(render.canvas().surf)

            renpy.redraw(self, 0.05)
            
            return render
