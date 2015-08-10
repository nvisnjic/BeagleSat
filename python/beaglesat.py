"""
BeagleSat
Copyright 2015 - Niko Visnjic <self@nvisnjic.com>

A library for controlling the BeagleSat CubeSat platform

"""

# We'll be using the bbio MPU9250 library for communication with the sensors
from bbio import *
# Import the MPU9250 class from the MPU9250 library:
from bbio.libraries.MPU9250 import MPU9250

#We're gonna need the data correction libraries as well 
from beaglesatCorrection import *

class BeagleSat(object):

  #sensorList = []  
  def __init__(self):
    """ Initialize BeagleSat object for further usage """

  def registerSensor(self, sensorID, sensorType, sensorConnection):
    """ Registers new sensor and adds it to the list of sensors registered 
        on the BeagleSat platform, doing appropriate checks
    """

    if (sensorType == "MPU9250"):
      self.mpu = MPU9250(sensorConnection) # sensorConnection should be SPI0
      if (self.mpu.sensorOnline == 1):
        print "MPU9250 sensor initialized via SPI0, sensor registered on ID = %d" % sensorID

  def unRegisterSensor(self, sensorID):
    """ Remove sensor with sensorID ID from list of sensors """      

  def saveConfiguration(self, file):
    """ save current setup to file """
  
  def restoreConfiguration(self, file):
    """ restore setup from file """

  def getRawMagData(self,  sensorID = 0):
    """ Read magnetometer data from sensor registered on ID sensorID
        and return data without processing it with error correction
    """

  def getCorrectedMagData(self, sensorID = 0, algorithmType = 0):
    """ Read magnetometer data from sensor registered on ID sensorID
        and return data which was processed for error correction using
        algorithm defined with algorithmType
        algorithmType == 0 uses time invariant correction algorithm
        algorithmType == 1 uses time   variant correction algorithm; which 
        requires additional input parameters
    """	
  
    # Test if we got a correct sensorID

    # Read single triplet of X Y Z magnetometer datag()
    magX, magY, magZ = self.mpu.getMag()
 
    if (algorithmType == 0):
       corrX, corrY, corrZ = invariantCorrection(magX, magY, magZ)



    return corrX, corrY, corrZ 

