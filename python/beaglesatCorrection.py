"""
BeagleSat Correction
Copyright 2015 - Niko Visnjic <self@nvisnjic.com>

A data compensation library for the BeagleSat project

"""


def invariantCorrection(xRaw, yRaw, zRaw):
  """ Time invariant correction algorithm for incoming magnetometer data 
      Returns a time invariant corrected triplet of X, Y and Z axis data
  """

  # For testing just passthrough
  return xRaw, yRaw, zRaw


def variantCorrection():
  """ Time variant correction algorithm for incoming magnetometer data """


def computeInvariantFactors(XYZdata):
  """ Compute time invariant correction factors from a body of collected data  
  """

def computeVariantFactors(): 
  """ Compute time invariant correction factors from a body of collected data  
  """

