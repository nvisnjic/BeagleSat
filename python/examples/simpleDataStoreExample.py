"""
BeagleSat - Simple data store Example
Copyright 2015 - Niko Visnjic <self@nvisnjic.com>

A test function showing how to utilize the BeagleSat library

"""

# Will be using bbio for input/output, so we'll need it's definitions
import bbio

# We need our BeagleSat API
from beaglesat import BeagleSat

####################################

# Construct BeagleSat object for handling
Laika = BeagleSat()

# Register MPU9250 on SPI0 (CS=0 default) as MPU_1
Laika.registerSensor( "MPU_1", "MPU9250", bbio.SPI0)

print("Gathering data for data fitting...")
print("You should rotate your sensor around all three axes, without moving its center!")
# Get some raw magnetometer data for processing
sensorData = Laika.getRawMagData( "MPU_1", 2000, 0.02)

print("\n\tFirst 5 readouts from magnetometer: (uT) \n")
print(sensorData[0:3, 0:5]) # it's a numpy array, so we use numpy indexing

# Store data in a file
Laika.storeData(sensorData,'../data/dataStore', 0) # 1 = append timestamp

print("\nDone\n")
