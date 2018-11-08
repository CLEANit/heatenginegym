from setuptools import setup, find_packages
import sys

setup(name='heatenginegym',
      py_modules=['heatenginegym'],
      install_requires=[
          'gym',
          'scipy',
          'tensorflow>=1.4.0',
          'matplotlib',
          'numpy',
      ],
      description='Implementation of heat engine simulations in the OpenAI Gym environment framework.',
      author='CLEAN',
      url='https://github.com/CLEANit/heatenginegym',
      version='1.0')
