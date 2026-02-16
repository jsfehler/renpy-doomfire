![Screenshot](/screenshot.png?raw=true "Screenshot")

# renpy-doomfire
The DOOM fire effect inside the Ren'Py game engine.
Based on Fabien Sanglard's explanation of the DOOM fire effect.

Source article: https://fabiensanglard.net/doom_fire_psx/index.html

The drawing is done in Ren'Py but the number crunching is provided by
a "backend", of which versions written in multiple languages are available:

- C using rand() for random number generation. Accessed by Python via the ctypes library.
- C (xorshift), using xorshift64 for random number generation. Accessed by Python via the ctypes library.
- Cython, using Python's random.random() for random number generation.
- Cython, using Python's random.randbytes() for random number generation.
- Cython used as an external interface for C.
- Cython used as an external interface for C (xorshift).
- Python, using Python's random.random() for random number generation.
- Python, using Python's random.randbytes() for random number generation.
- Rust, built into a Python module using pyO3 and maturin.

The purpose of all these backends is to demonstrate various ways to increase performance.

## Backend Performance Testing Results

| Size: 212 x 128 | Iterations: 1000 |
| Backend                 | Time (s) | Relative Speed |
|-------------------------|----------|----------------|
| C                       | 0.273    | 3.89×          |
| C (xorshift)            | 0.095    | 1.36×          |
| Cython                  | 1.415    | 20.18×         |
| Cython (randbytes)      | 0.631    | 9.01×          |
| Cython Extern           | 0.268    | 3.82×          |
| Cython Extern (xorshift)| 0.090    | 1.28×          |
| Python                  | 3.275    | 46.73×         |
| Python (randbytes)      | 2.358    | 33.65×         |
| Rust                    | 0.070    | 1.00×          |

| Size: 212 x 128 | Iterations: 10000 |
| Backend                 | Time (s) | Relative Speed |
|-------------------------|----------|----------------|
| C                       | 2.903    | 4.03×          |
| C (xorshift)            | 1.003    | 1.39×          |
| Cython                  | 14.761   | 20.51×         |
| Cython (randbytes)      | 6.724    | 9.34×          |
| Cython Extern           | 2.782    | 3.87×          |
| Cython Extern (xorshift)| 0.945    | 1.31×          |
| Python                  | 34.575   | 48.04×         |
| Python (randbytes)      | 24.334   | 33.81×         |
| Rust                    | 0.720    | 1.00×          |

| Size: 848 x 128 | Iterations: 1000 |
| Backend                 | Time (s) | Relative Speed |
|-------------------------|----------|----------------|
| C                       | 1.209    | 3.93×          |
| C (xorshift)            | 0.427    | 1.39×          |
| Cython                  | 6.437    | 20.95×         |
| Cython (randbytes)      | 3.429    | 11.16×         |
| Cython Extern           | 1.185    | 3.86×          |
| Cython Extern (xorshift)| 0.423    | 1.38×          |
| Python                  | 15.923   | 51.82×         |
| Python (randbytes)      | 10.963   | 35.68×         |
| Rust                    | 0.307    | 1.00×          |

## Thoughts

### Compiling Is Hard

Without optimization the compiled C code is much slower.
It may seem obvious but this mistake made Rust look significantly more performant.

`g++ -fPIC -shared -o doom_fire_c.so main.cpp`

VS

`g++ -O3 -flto -fPIC -shared -o doom_fire_c.so main.cpp`

If I'd forgotten the same flags in the Cargo.toml, I imagine I'd have gotten a similar result.

Without optimization flags:

| Backend       | Time (s) | Relative Speed |
|---------------|----------|----------------|
| C             | 0.340    | 4.40×          |
| Rust          | 0.077    | 1.00×          |

### C's rand() Is Slow?

xorshift64 compared to rand() was much faster.
Is it less secure/reliable/deterministic? Maybe?
Do we need perfect randomness for the fire simulation? Nope.

### Python Iteration Is Slow

Cython's speed improvement for minimal changes is powerful but iterating through a massive tuple in Python still clobbers performance.

### Python Lists Can Be Dangerous

foo[-1] is invalid for the simulation but works in Python.
Because C/Rust throw an error, the bug never escaped.

### Think Smarter, Not Harder

Instead of `int(random.random())` called for every pixel, a single call to `random.randbytes()` and
indexing the value brought a massive boost in Python and Cython.

This only works because while iterating we already have an index number to pick an integer from randbytes.
The single random series of bytes generated each time is enough for the simulation.

### Cython As A Bridge Between C and Python

Even in this small project Cython is a better, if heavier, experience for wrapping C than the ctypes module.

### If Rust Compiles, That Means It's Good

Right? ...Right?

### Just Use A Shader

Individual pixel manipulations on the CPU don't scale at large resolutions.
You're going to have a better time using a fragment shader.

## Warning

- My C skills are beginner level. If you're foolish enough to use that code in a real game without testing it first that's your fault, not mine.

- My Rust skills are also beginner level. See above warning.

- The performance test only covers the math, not the drawing of the pixels to the screen.

- The drawing code triggers a redraw ever 0.01667 seconds.
  This is ideally going to get you animation at 60 frames per second but the timestep of the simulation and drawing aren't split.
  If the rendering can't keep up, the fire will slow down.
  A potential improvement is to decouple the physics and drawing but you'd have to build the whole thing from scratch.
  Have fun with that.

## Directory Structure

- `backend`: Contains the source code for the C, Cython, Python, and Rust backends.
- `build`: Contains the compiled code, drop-in ready.
- `game`: Contains the drawing and setup code for a Ren'Py project.
- `performance`: Contains the performance testing script.

## How To Run The Demo

The binary should be placed above the `game` directory in a Ren'Py project.

1. Create a new Ren'Py project.

2. Place the files inside the `game` directory into the project's game directory.

3. Place the files inside the `build` directory into the project's game directory.

## How To Run The Performance Test

1. Place the files inside the `build` into the `performance` directory.

2. From inside the `performance` directory, run `python run.py`.

## How To Compile The Source Code

### Linux

**Warning**: When you compile Cython you must match the version of Python Ren'Py uses. Ren'Py 8.x uses Python `3.12.x`

Run the following console command: `./build.sh all`.
This will compile every backend and place the output in the `build` directory.

`./build.sh <backend>` will compile a single backend.

## FAQ

  - Why not use numpy/numba/nuitka? Answer: Not compatible with Ren'py.

  - Will this run on Windows/MacOS? Answer: If you compile the source code for those platforms.

  - Does this work with Pygame? Answer: Ren'Py doesn't use Pygame, it uses https://github.com/renpy/pygame_sdl2.
    You can, however, use the backends with Pygame or any other Python library and write your own rendering logic.

  - What about Go or Zig? Odin? Julia? How about Fortran? Answer: I'm tired, boss.
