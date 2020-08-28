from setuptools import setup
from Cython.Build import cythonize


setup(
    ext_modules=cythonize("cy_fire/doom_fire_cy.pyx", language_level="2")
)
