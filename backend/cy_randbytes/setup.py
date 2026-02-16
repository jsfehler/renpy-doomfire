from setuptools import setup
from Cython.Build import cythonize


setup(
    ext_modules=cythonize("doom_fire_cy_rand_bytes.pyx", language_level="2")
)
