
from setuptools import Extension, setup


module1 = Extension('_example', sources=['example.c'])


setup(name='c-math',
      version='1.0',
      description='This is a demo package',
      ext_modules=[module1]
)
