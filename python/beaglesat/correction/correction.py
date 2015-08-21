"""
BeagleSat Correction
Copyright 2015 - Niko Visnjic <self@nvisnjic.com>

A data compensation library for the BeagleSat project

"""

import algorithms.invariantFitting
import numpy

def invariantCorrection(XYZdata, factors, IGRF):
  """ Time invariant correction algorithm for incoming magnetometer data 
      Returns a time invariant corrected  dataset (X, Y, Z) * len(XYZdata)
  """
 
  # Correction factors (offsetX, oY, oZ, scalingX, sY, sZ)
  offsets = factors[0][0:3] 
  scaling = factors[1][0:3] 

  # Bh IGRF, magnitude of magnetic field to fit to
  Bh = IGRF

  # dataset split
  x = XYZdata[0]
  y = XYZdata[1]
  z = XYZdata[2]

  # fix offset
  fixed_x = x - numpy.ones(numpy.size(x)) * offsets[0] 
  fixed_y = y - numpy.ones(numpy.size(y)) * offsets[1] 
  fixed_z = z - numpy.ones(numpy.size(z)) * offsets[2] 

  # fix scale
  fixed_x = fixed_x / scaling[0] * Bh
  fixed_y = fixed_y / scaling[1] * Bh
  fixed_z = fixed_z / scaling[2] * Bh


  return (fixed_x, fixed_y, fixed_z)


def variantCorrection(XYZdata, factors, IGRF):
  """ Time variant correction algorithm for incoming magnetometer data 
      Returns a time variant corrected  dataset (X, Y, Z) * len(XYZdata)
  """ 

def computeInvariantFactors(XYZdata): 
  """ Compute time invariant correction factors from a body of  
      collected data  
      Returns offset triplet (OX,OY,OZ) and scaling triplet (SX,SY,SZ)
  """
	
  # Split the data
  X = XYZdata[0]
  Y = XYZdata[1]
  Z = XYZdata[2]
  (offset, scaling) = algorithms.invariantFitting.compute(X, Y, Z)
  
  return (offset, scaling)

def computeVariantFactors(): 
  """ Compute time invariant correction factors from a body of collected data  
  """

