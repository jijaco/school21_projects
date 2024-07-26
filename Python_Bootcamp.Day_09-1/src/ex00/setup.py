from setuptools import setup, Extension

module = Extension('calculator',
                   sources=['calculator.c'])

setup(name='calculator',
      version='1.0',
      description='Python/C API calculator',
      ext_modules=[module])
# from setuptools import setup, Extension

# module = Extension('calculator', sources=['calculator.c'])

# setup(
#     name='calculator',
#     version='1.0',
#     description='Simple calculator module',
#     ext_modules=[module]
# )
