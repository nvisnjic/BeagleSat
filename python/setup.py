"""A setuptools based CubeSat building module.

See:
http://nvisnjic.com/beaglesat
https://github.com/nvisnjic/BeagleSat
"""

import sys, os, shutil, glob

print ("Installing BeagleSat")

from setuptools import setup, Extension, find_packages

install_requires = [
  'PyBBIO',
  'numpy'
]

setup(name='BeagleSat',
      version='0.1.0',
      description='A Python library for controlling and setting up a CubeSat (miniature satellite) platform based on the BeagleBone Black',
      long_description=open('README.md').read(),
      author='Niko Visnjic',
      author_email='self@nvisnjic.com',
      license='GPLv3+',
      url='https://github.com/nvisnjic/BeagleSat',
      keywords=['BeagleBone Black', 'CubeSat', 'satellite',  
        'Ellipsoid fitting', 'sensordata processing', 'GPIO', 'I2C', 'SPI' ],
      packages=find_packages(),
      install_requires=install_requires,
      platforms=['BeagleBone', 'BeagleBone Black'],
      classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv2+)',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: System :: Hardware'
      ])
