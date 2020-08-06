init -1000 python in c_doomfire:
    from ctypes import *
    import itertools

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

            # Load C++ library. 
            path = renpy.loader.transfn('fire.dll')
            self.c_lib = cdll.LoadLibrary(path)

            # Setup lists that record the pixel colour data
            self.c_lib.setup_fire(width, height)

            # We already know where every pixel will be placed on screen, so record that ahead of time
            self.pixel_positions = []
            for y, x in itertools.product(range(height), range(width)):
                index = y * width + x
                self.pixel_positions.append(
                    (index, x * self.pixel_distance, y * self.pixel_distance)
                )

            # Vain attempt to get a bit more speed
            self.pixel_positions = tuple(self.pixel_positions)

        def draw_pixels(self, surface):
            """Draw all the pixels to a surface.

            Arguments:
                surface: Pygame surface to draw on.
            """
            # Make local namespaces to speed up the for loop
            palette = self.palette
            pixel = gfxdraw.pixel
            
            get_at = self.c_lib.get_at

            for colour_index, xpos, ypos in self.pixel_positions:
                # Get colour height of current pixel
                height_index = get_at(colour_index)

                # Don't draw the pixel if it's the highest colour.
                if height_index:
                    pixel(surface, xpos, ypos, palette[height_index])

        def render(self, width, height, st, at):
            render = renpy.Render(self.width, self.height)

            # For every pixel, move color height
            self.c_lib.spread_fire(self.fire_width)
            
            self.draw_pixels(render.canvas().surf)

            renpy.redraw(self, 0.05)
            
            return render
