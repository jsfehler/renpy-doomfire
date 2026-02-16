"""renpy
init -999 python in py_fire:
"""

import itertools
import random


class DoomFireBackend:
    """Backend for the fire simulation.

    Attributes:
        colour_heights: Current value for every pixel's colour height.
        fire_positions: Indexes for every pixel in colour_heights.
    """
    def __init__(self) -> None:
        self.colour_heights: list[int] = []
        self.fire_positions: tuple[int, ...] = ()

    def setup_height_map(self, width: int, height: int) -> None:
        """Populate the colour_heights and fire_positions attributes.

        colour_heights: Zero-filled list of length(width * height).
          Represents the current height of every pixel.

        fire_positions: Tuple of the index for every pixel, except the bottom row.
        """
        self.colour_heights = [0 for i in range(width * height)]

        # Set bottom row to last colour in palette.
        for i in range(width):
            self.colour_heights[((height - 1) * width) + i] = 36

        self.fire_positions = tuple(
            (y * width + x for x, y in itertools.product(range(width), range(1, height))),
        )

    def spread_fire(self, width: int) -> None:
        """Advance the fire simulation by one frame."""
        # Make local namespace to speed up attribute access.
        colour_heights = self.colour_heights

        for source in self.fire_positions:
            pixel = colour_heights[source]

            if pixel == 0:
                colour_heights[source - width] = 0
            else:
                # Get a random number between 0 and 3
                r_index = int(random.random() * 4.0)

                dst = source - r_index + 1

                colour_heights[dst - width] = pixel - (r_index & 1)
