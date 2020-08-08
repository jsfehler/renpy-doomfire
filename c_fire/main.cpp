#include "main.h"

#include <stdio.h>
#include <stdlib.h>

int *colour_height_map;
int *fire_positions;

int fp_length;


void shift_colour_height(int pixel_position, int width) {
    int pixel = colour_height_map[pixel_position];

    if (pixel == 0) {
        colour_height_map[pixel_position - width] = 0;
    } else {
        // Get a random number between 0 and 3
        int r_index = rand() % 4;

        int dst = pixel_position - r_index + 1;

        colour_height_map[dst - width] = pixel - (r_index & 1);
    }

}


void spread_fire(int width) {
    // Move each pixel's color height.
    for (int i=0; i < fp_length; i++) {
        shift_colour_height(fire_positions[i], width);
    }
}


int get_at(int index) {
    return colour_height_map[index];
}


void setup_height_map(int width, int height) {
    //Build two lists:
    //  - colour_height_map: Values for every pixel's current color height
    //  - fire_positions: Indexes for every pixel in pixel_list

    // Set colour_height_map to the correct size
    int array_size = width * height;
    colour_height_map = (int*) realloc(colour_height_map, array_size * sizeof(int));

    // Set fire_positions to the correct size
    fp_length = (width * (height - 1));
    fire_positions = (int*) realloc(fire_positions, fp_length * sizeof(int));

    //  Set heights for entire drawable area to 0
    for (int i=0; i < array_size; i++) {
        colour_height_map[i] = 0;
    }

    // Set bottom line to last colour in palette
    for (int i=0; i < width; i++) {
        colour_height_map[((height - 1) * width) + i] = 36;
    }

    int fire_positions_index = 0;
    for (int x=0; x < width; x++) {
        for (int y=1; y < height; y++) {
            fire_positions[fire_positions_index] = y * width + x;
            fire_positions_index++;
        }
    }
}
