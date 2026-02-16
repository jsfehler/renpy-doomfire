from setuptools import setup, Extension
from Cython.Build import cythonize

ext = Extension(
    "doom_fire_cy_extern_xorshift",
    ["doom_fire_cy_extern_xorshift.pyx", "../c_xorshift/main.c"],
    language="C++",
    extra_compile_args=["-O3", "-flto"],
    extra_link_args=["-flto"],
)

setup(
    ext_modules=cythonize(ext)
)
