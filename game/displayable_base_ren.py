"""renpy
init -999 python:
"""

import itertools

class DoomFireDisplayable(renpy.Displayable):
    """Generate an upwards fire animation by shifting pixel colours.

    Arguments:
        palette (tuple): Every colour to cycle through.
        pixel_distance (int): Distance on screen between each pixel.
        width (int): Width, in pixels, of the fire.
        height (int): Height, in pixels, of the fire.
    """
    def __init__(
        self,
        palette: tuple[tuple[int, int, int]],
        pixel_distance: int,
        width: int,
        height: int,
        **kwargs,
    ) -> None:
        super(DoomFireDisplayable, self).__init__(**kwargs)

        self.palette = palette
        self.pixel_distance = pixel_distance
        self.width = width * self.pixel_distance
        self.height = height * self.pixel_distance

        # Number of pixels, across and wide
        self.fire_width = width
        self.fire_height = height

        # We already know where every pixel will be drawn on screen, so record that ahead of time
        # The three attributes for each pixel are:
        #   colour_index: Index for the list that stores the current height of every pixel
        #   xpos: physical x position of the pixel
        #   ypos: physical y position of the pixel
        self.pixel_screen_positions = tuple(
            ((y * width + x, x * self.pixel_distance, y * self.pixel_distance) for y, x in itertools.product(range(height), range(width)))
        )

    def render(self, width: int, height: int, st: float, at: float) -> renpy.Render:
        render = renpy.Render(self.width, self.height)

        # For every pixel, move colour height
        self.backend.spread_fire(self.fire_width)

        self.draw_pixels(render.canvas().surf)

        renpy.redraw(self, 0.01667)

        return render
