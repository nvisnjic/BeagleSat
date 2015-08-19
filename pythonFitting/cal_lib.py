"""
cal_lib.py - Ellipsoid into Sphere calibration library based upon numpy and linalg
Copyright (C) 2012 Fabio Varesano 

Development of this code has been supported by the Department of Computer Science,
Universita' degli Studi di Torino, Italy within the Piemonte Project
http://www.piemonte.di.unito.it/


This program is free software: you can redistribute it and/or modify
it under the terms of the version 3 GNU General Public License as
published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see .

"""

import numpy
from numpy import linalg

def calibrate(x, y, z):
  H = numpy.array([x, y, z, -y**2, -z**2, numpy.ones(len(x))])
  H = numpy.transpose(H)
  w = x**2
  
  (X, residues, rank, shape) = linalg.lstsq(H, w)
  
  OSx = X[0] / 2
  OSy = X[1] / (2 * X[3])
  OSz = X[2] / (2 * X[4])
  
  A = X[5] + OSx**2 + X[3] * OSy**2 + X[4] * OSz**2
  B = A / X[3]
  C = A / X[4]
  
  SCx = numpy.sqrt(A)
  SCy = numpy.sqrt(B)
  SCz = numpy.sqrt(C)
  
  return ([OSx, OSy, OSz], [SCx, SCy, SCz])


if __name__ == "__main__":
  acc_f = open("acc.txt", 'r')
  acc_x = []
  acc_y = []
  acc_z = []
  for line in acc_f:
    reading = line.split()
    acc_x.append(int(reading[0]))
    acc_y.append(int(reading[1]))
    acc_z.append(int(reading[2]))

  (offsets, scale) = calibrate(numpy.array(acc_x), numpy.array(acc_y), numpy.array(acc_z))
  print (offsets)
  print (scale)
