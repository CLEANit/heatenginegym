from setuptools import setup, find_packages
import sys

setup(name='carnotgym',
      py_modules=['cleangym'],
      install_requires=[
          'gym',
          'scipy',
          'progressbar2',
          'tensorflow>=1.4.0',
          'matplotlib',
          'numpy',
      ],
      description='CLEAN implementation of Carnot (and various other thermodynamic engine) gym environments.',
      author='CLEAN',
      url='https://github.com/CLEANit/carnot',
      version='0.4')
