"""
BeagleSat Example
Copyright 2015 - Niko Visnjic <self@nvisnjic.com>

A test function showing how to utilize the BeagleSat library

"""

from beaglesat import *


Laika = BeagleSat()


Laika.registerSensor( "MPU_1", "MPU9250", SPI0)


# Read and correct magnetometer data
magX, magY, magZ = Laika.getCorrectedMagData( "MPU_1", 0)

print "Corrected magnetometer data:" 
print "\n MagX: %.3f uT \t | MagY: %.3f uT\t | MagZ: %.3f uT" % (magX, magY, magZ )
