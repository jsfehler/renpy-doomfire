init -998 python in py_doomfire:
    import pygame_sdl2.gfxdraw as gfxdraw

    from renpy import store

    from store.py_fire import DoomFireBackend


    class DoomFire(store.DoomFireDisplayable):
        def __init__(self, palette, pixel_distance, width, height, **kwargs):
            super(DoomFire, self).__init__(palette, pixel_distance, width, height, **kwargs)

            self.backend = DoomFireBackend()

            # Setup lists that records each pixel's colour height.
            self.backend.setup_height_map(self.width, self.height)

        def draw_pixels(self, surface):
            """Draw all the pixels to a surface.

            Arguments:
                surface: Pygame surface to draw on.
            """
            # Make local namespaces to speed up the for loop.
            palette = self.palette
            pixel = gfxdraw.pixel

            colour_heights = self.backend.colour_heights

            for colour_index, xpos, ypos in self.pixel_screen_positions:
                # Get colour height of current pixel
                height_index = colour_heights[colour_index]

                # Don't draw the pixel if it's the highest colour.
                if height_index:
                    pixel(surface, xpos, ypos, palette[height_index])
