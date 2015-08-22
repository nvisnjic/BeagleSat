"""
BeagleSat - Complete data pipeline(read/store/process) Example
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
Laika.registerSensor( sensorID = "MPU_1", sensorType = "MPU9250", sensorConnection = bbio.SPI0)

# Set a global value for IGRF in uT (reference magnetic field magnitude)
Laika.setIGRF(1000)

print("Gathering data for ellipsoid fitting...")
print("You should rotate your sensor around all three axes, without moving its center!")
# Get some raw magnetometer data for processing
sensorData = Laika.getRawMagData( "MPU_1", nrSamples = 500, sampleDelay = 0.05)

print("\n\tFirst 5 readouts from magnetometer: (uT) \n")
print(sensorData[0:3, 0:5]) # it's a numpy array, so we use numpy indexing

# Store data in a file
Laika.storeData(sensorData,'./data/fittingData' , stampTime = 0)

# Read that data back (you probably use this in some more meaningful way)
XYZdata = Laika.loadData('./data/fittingData')

# Compute correction parameters based on stored fitting data
Laika.computeCorrectionFactors("MPU_1", XYZdata)

print("\n\tComputed correction factors:\n")
# Correction factors get stored in sensor internal data, in this case in MPU_1
print(Laika.sensorList["MPU_1"].corrFactors)

# Read a new independent set of data
newData = Laika.getRawMagData( "MPU_1", nrSamples = 25, sampleDelay = 0.5)

# Store set of new data for later testing
Laika.storeData(newData,'./data/testData', stampTime = 0)

# Correct new data
correctedData = Laika.correctData(newData, "MPU_1", algorithmType = 0)

# and store it in a file
Laika.storeData(correctedData,'./data/correctedTestData', stampTime = 0)


print("\n\tFirst 5 readouts from corrected magnetometer: (uT) \n")
print(correctedData[0:3, 0:5]) # it's a numpy array, so we use numpy indexing


