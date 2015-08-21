"""
BeagleSat - Read single magnetometer data example
Copyright 2015 - Niko Visnjic <self@nvisnjic.com>

A test function showing how to utilize the BeagleSat library

"""

# Will be using bbio for input/output, so we'll need it's definitions
import bbio

# We need our BeagleSat API
from beaglesat import BeagleSat


Laika = BeagleSat()


Laika.registerSensor( "MPU_1", "MPU9250", bbio.SPI0)


# Read and correct magnetometer datai
magX, magY, magZ = Laika.getRawMagData( "MPU_1", nrSamples = 1)


print ("Corrected magnetometer data:")
print ("\n MagX: %.3f uT \t | MagY: %.3f uT\t | MagZ: %.3f uT") %  \
        (magX, magY, magZ ) 

