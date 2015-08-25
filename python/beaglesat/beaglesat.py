"""
BeagleSat
Copyright 2015 - Niko Visnjic <self@nvisnjic.com>

A library for controlling the BeagleSat CubeSat platform.

    This file is part of BeagleSat.

    BeagleSat is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    BeagleSat is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with BeagleSat.  If not, see <http://www.gnu.org/licenses/>.

"""

# We'll be using the bbio MPU9250 library for communication with the sensors
import bbio
# Import the MPU9250 class from the MPU9250 library:
from bbio.libraries.MPU9250 import MPU9250

# We're gonna need the data correction libraries as well 
import correction

# Some arrays may be needed
import numpy
# Want to write a file
import os, csv
# Delay is good
import time
# timestamps are also nice
import datetime

class BeagleSat(object):

  
  def __init__(self):
    """ Initialize BeagleSat object for further usage """

    self.sensorList = {} # Create empty dictionary to track registered sensors
    self.currentIGRF = None   # Holds the current IGRF value for correction 
                              # factor computation
    # done with init()
  
  def saveConfiguration(self, file):
    """ save current setup to file """
    pass
  
  def restoreConfiguration(self, file):
    """ restore setup from file """
    pass

  def setIGRF(self, valIGRF):
    """ set IGRF value for BeagleSat and all registered sensors """
    self.currentIGRF = valIGRF

    # Update all registered sensors
    for sensorID in self.sensorList:
      self.sensorList[sensorID].IGRF = valIGRF


  def registerSensor(self, sensorID, sensorType, sensorConnection):
    """ Registers new sensor and adds it to the list of sensors registered 
        on the BeagleSat platform, doing appropriate checks
    """
    if sensorID in self.sensorList: # Check if ID already taken
      print("Sensor ID = %s already taken, please choose another\n") % sensorID
      return -1

    if (sensorType == "MPU9250"):
      mpu = MPU9250(sensorConnection) # sensorConnection should be SPI0
      if (mpu.sensorOnline == 1):
        print("MPU9250 sensor initialized via SPI0, sensor registered on ID = %s\n") % sensorID
      
      # Construct sensor object
      new_sensor = sensor()
      new_sensor.device = mpu

      # Add sensor to list of sensors
      self.sensorList[sensorID] = new_sensor

  def unRegisterSensor(self, sensorID):
    """ Remove sensor with sensorID ID from list of sensors """      
    # Test if we got a correct sensorID
    if not (sensorID in self.sensorList):
      print("Invalid sensor ID for unregister, please provide a valid sensor ID\n")
      return -1

    del self.sensorList[sensorID]

  def computeCorrectionFactors(self, sensorID, XYZdata):
    """ Compute correction factors for the time invariant algorithm """
    
    # Test if we got a correct sensorID
    if not (sensorID in self.sensorList):
      print("Invalid sensor ID, please provide a valid sensor ID for invariant correction factor computation\n")
      return -1

    corrFactors = correction.computeInvariantFactors(XYZdata)
    
    # Get sensor object
    sensor = self.sensorList[sensorID]
    
    #Store factors in sensor data
    sensor.corrFactors = corrFactors
    
  
  def computeCorrectionFactorsVariant(self, sensorID, params):
    """ Compute correction factors for the time variant algorithm """
    pass

  def getRawMagData(self,  sensorID = 0, nrSamples = 1, sampleDelay = 0.25):
    """ Read magnetometer data from sensor registered on ID sensorID
        and return data without processing it with error correction
        
    """
    # Test if we got a correct sensorID
    if not (sensorID in self.sensorList):
      print("Invalid sensor ID, please provide a valid sensor ID for data correction\n")
      return -1
    # Select
    sensor = self.sensorList[sensorID]

    XYZdata = []
    magX = []
    magY = []
    magZ = []
    for i in range(nrSamples):
      # Read single triplet of X Y Z magnetometer datag()
      (x, y, z) = sensor.device.getMag()
      magX.append(x)
      magY.append(y)
      magZ.append(z)
      # Delay between reads
      time.sleep(sampleDelay)

   
    # Format as a numpy array of X,Y,Z data 
    XYZdata = numpy.array([magX, magY, magZ])
    
    return XYZdata

  def correctData(self, XYZdata, sensorID = 0, algorithmType = 0):
    """ Read magnetometer data from sensor registered on ID sensorID
        and return data which was processed for error correction using
        algorithm defined with algorithmType
        algorithmType == 0 uses time invariant correction algorithm
        algorithmType == 1 uses time   variant correction algorithm; which 
        requires additional input parameters (not complete yet)
    """	 
    # Test if we got a correct sensorID
    if not (sensorID in self.sensorList):
      print("Invalid sensor ID, please provide a valid sensor ID for data correction\n")
      return -1

    sensor = self.sensorList[sensorID]

    # Get correction factors from sensor object
    factors = sensor.corrFactors

    if not factors:
      print("Correction factors not saved in sensor.corrFactors. Did you run computeCorrectionFactors() ?")

    # Reference magnitude of magnetic field
    IGRF = sensor.IGRF

    if (algorithmType == 0):
       (corrX, corrY, corrZ) = correction.invariantCorrection(XYZdata, factors, IGRF)
    
    # pack corrected data
    corrected = numpy.array([corrX, corrY, corrZ])

    return corrected


  # Convenience functions for storing/reading data
  def storeData(self, XYZdata, file = './data/readouts', stampTime = 1):
    """ Store collected data in a default format """
      
    # Construct filename; add date/time + other markers
    if(stampTime):
      filename =  file + timeStamp()
    else:
      filename =  file

    # Does the file exist?
    if not os.path.exists(os.path.dirname(filename)):
      os.makedirs(os.path.dirname(filename))
    # Write
    with open(filename, 'w') as outcsv:
      #configure writer to write a csv file
      writer = csv.writer(outcsv, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
      writer.writerow(['x_axis', 'y_axis', 'z_axis'])
      for i in range(numpy.size(XYZdata, 1)):
        #Write item to outcsv
        writer.writerow([XYZdata[0, i], XYZdata[1, i], XYZdata[2, i]])

    print(("\nData stored in %s\n") % filename)
    return 0

  def loadData(self, file):
    """ Read data from a CSV file """
    
    dataX = []
    dataY = []
    dataZ = []
    with open(file, "r") as f:
      reader = csv.reader(f, delimiter=" ")
      names = reader.next()
      for row in reader:
        (x, y, z) = row
        dataX.append(float(x))
        dataY.append(float(y))
        dataZ.append(float(z))

    # Reshape back to previous format of numpy.array (list of lists)
    XYZdata = numpy.array([dataX, dataY, dataZ])
    return XYZdata

def timeStamp(fmt='%Y-%m-%d-%H-%M-%S'):
  """ Get timestamp and patch it to the filename """
  return datetime.datetime.now().strftime(fmt)

class sensor(object):
  """ Class that holds sensor object and its data """ 
 
  def __init__(self): 
    self.IGRF     = None      # Currenyly set IGRF value for comuptation, 
                              # should be equal to global IGRF
    self.corrFactors  = []    # 6 correction factors for offset and scaling
    self.device   = None 




