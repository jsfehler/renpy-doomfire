from ctypes import cdll
import timeit
import pathlib

from doom_fire_py_ren import DoomFireBackend as PyDoomFireBackend
from doom_fire_py_randbytes_ren import DoomFireBackend as PyDoomFireBackendRandBytes

from doom_fire_cy import DoomFireBackend as CythonDoomFireBackend
from doom_fire_cy_rand_bytes import DoomFireBackend as CythonDoomFireBackendRandBytes
from doom_fire_rust import DoomFireBackend as RustDoomFireBackend

import doom_fire_cy_extern
import doom_fire_cy_extern_xorshift

WIDTH = 212
HEIGHT = 128
NUM_ITERATIONS = 1000

report_header = f"""
| Size: {WIDTH} x {HEIGHT} | Iterations: {NUM_ITERATIONS} |
| Backend                 | Time (s) | Relative Speed |
|-------------------------|----------|----------------|
"""

def calculate_relative_speed(speeds: dict[str, float]) -> float:
    """Calculate the relative speed of the backends.

    Whichever backend is the fastest is set to 1.0.
    """
    fastest = min(speeds.values())

    results = {}

    for k, v in speeds.items():
        multiplier = v / fastest
        results[k] = multiplier

    return results


def run() -> str:  # NOQA: C901 PLR0915
    """Run the performance test."""
    # Initialize the backends.
    c_lib_path = pathlib.Path(__file__).parent / 'doom_fire_c.so'
    c_backend = cdll.LoadLibrary(str(c_lib_path))
    c_xorshift_lib_path = pathlib.Path(__file__).parent / 'doom_fire_c_xorshift.so'
    c_xorshift_backend = cdll.LoadLibrary(str(c_xorshift_lib_path))
    cy_backend = CythonDoomFireBackend()
    cy_rand_bytes_backend = CythonDoomFireBackendRandBytes()
    rust_backend = RustDoomFireBackend()
    py_backend = PyDoomFireBackend()
    py_rand_bytes_backend = PyDoomFireBackendRandBytes()

    c_backend.setup_height_map(WIDTH, HEIGHT)
    c_xorshift_backend.setup_height_map(WIDTH, HEIGHT)
    cy_backend.setup_height_map(WIDTH, HEIGHT)
    cy_rand_bytes_backend.setup_height_map(WIDTH, HEIGHT)
    doom_fire_cy_extern.setup_height_map(WIDTH, HEIGHT)
    doom_fire_cy_extern_xorshift.setup_height_map(WIDTH, HEIGHT)
    py_backend.setup_height_map(WIDTH, HEIGHT)
    py_rand_bytes_backend.setup_height_map(WIDTH, HEIGHT)
    rust_backend.setup_height_map(WIDTH, HEIGHT)


    def c_render() -> None:
        c_backend.spread_fire(WIDTH)


    def c_xorshift_render() -> None:
        c_xorshift_backend.spread_fire(WIDTH)


    def cy_render() -> None:
        cy_backend.spread_fire(WIDTH)


    def cy_rand_bytes_render() -> None:
        cy_rand_bytes_backend.spread_fire(WIDTH)


    def cy_extern_render() -> None:
        doom_fire_cy_extern.spread_fire(WIDTH)


    def cy_extern_xorshift_render() -> None:
        doom_fire_cy_extern_xorshift.spread_fire(WIDTH)


    def py_render() -> None:
        py_backend.spread_fire(WIDTH)


    def py_rand_bytes_render() -> None:
        py_rand_bytes_backend.spread_fire(WIDTH)

    def rust_render() -> None:
        rust_backend.spread_fire(WIDTH)

    # Run simulation.
    c_result = timeit.timeit(c_render, number=NUM_ITERATIONS)
    c_xorshift_result = timeit.timeit(c_xorshift_render, number=NUM_ITERATIONS)
    cy_result = timeit.timeit(cy_render, number=NUM_ITERATIONS)
    cy_rand_bytes_result = timeit.timeit(cy_rand_bytes_render, number=NUM_ITERATIONS)
    cy_extern_result = timeit.timeit(cy_extern_render, number=NUM_ITERATIONS)
    cy_extern_xorshift_result = timeit.timeit(cy_extern_xorshift_render, number=NUM_ITERATIONS)
    py_result = timeit.timeit(py_render, number=NUM_ITERATIONS)
    py_rand_bytes_result = timeit.timeit(py_rand_bytes_render, number=NUM_ITERATIONS)
    rust_result = timeit.timeit(rust_render, number=NUM_ITERATIONS)

    # Process results.
    speeds = {
        "C": c_result,
        "C (xorshift)": c_xorshift_result,
        "Cython": cy_result,
        "Cython (randbytes)": cy_rand_bytes_result,
        "Cython Extern": cy_extern_result,
        "Cython Extern (xorshift)": cy_extern_xorshift_result,
        "Python": py_result,
        "Python (randbytes)": py_rand_bytes_result,
        "Rust": rust_result,
    }

    relative_speeds = calculate_relative_speed(speeds)

    report_results_string = ""

    for k, v in speeds.items():
        rel_speed = f"{relative_speeds[k]:.2f}x".ljust(14)
        report_results_string += f"| {k.ljust(24)}| {v:.3f}    | {rel_speed} |\n"

    final_report = report_header + report_results_string

    return final_report

if __name__ == "__main__":
    final_report = run()
    print(final_report)  # NOQA: T201
