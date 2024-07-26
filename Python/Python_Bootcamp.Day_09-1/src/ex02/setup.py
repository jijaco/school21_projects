from setuptools import setup, Extension

module = Extension("matrix_multiply", ["multiply.pyx"])

setup(name='matrix_multiply',
      ext_modules=[module])
