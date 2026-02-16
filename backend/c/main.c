#include "main.h"

#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int *data;
    size_t length;
} IntArray;

// Maximum colour index in the palette.
static const int MAX_COLOUR_INDEX = 36;

// colour_heights: Current value for every pixel's colour height.
// fire_positions: Indexes for every pixel in colour_heights.
IntArray colour_heights;
IntArray fire_positions;

void shift_colour_height(int pixel_position, int width) {
    int pixel = colour_heights.data[pixel_position];

    if (pixel == 0) {
        // If the pixel is already dark, just propagate darkness up.
        colour_heights.data[pixel_position - width] = 0;
    } else {
        // Get a random number between 0 and 3
        int r_index = rand() % 4;

        int dst = pixel_position - r_index + 1;
        int target = dst - width;

        if (target >= 0 && target < (int)colour_heights.length) {
            colour_heights.data[target] = pixel - (r_index & 1);
        }
    }
}

// Advance the fire simulation by one frame.
void spread_fire(int width) {
    for (size_t i=0; i < fire_positions.length; i++) {
        shift_colour_height(fire_positions.data[i], width);
    }
}

int get_colour_heights(int index) {
    return colour_heights.data[index];
}

void setup_height_map(size_t width, size_t height) {
    // Populate the colour_heights and fire_positions attributes.
    // colour_heights: Zero-filled list of length(width * height).
    //   Represents the current height of every pixel.
    //
    // fire_positions: Tuple of the index for every pixel, except the bottom row.
    colour_heights.length = width * height;
    colour_heights.data = (int*) realloc(colour_heights.data, colour_heights.length * sizeof(int));

    fire_positions.length = (width * (height - 1));
    fire_positions.data = (int*) realloc(fire_positions.data, fire_positions.length * sizeof(int));

    for (size_t i=0; i < colour_heights.length; i++) {
        colour_heights.data[i] = 0;
    }

    // Set bottom line to last colour in palette.
    for (size_t i=0; i < width; i++) {
        colour_heights.data[((height - 1) * width) + i] = MAX_COLOUR_INDEX;
    }

    int fire_positions_index = 0;
    for (size_t x=0; x < width; x++) {
        for (size_t y=1; y < height; y++) {
            fire_positions.data[fire_positions_index] = y * width + x;
            fire_positions_index++;
        }
    }
}
