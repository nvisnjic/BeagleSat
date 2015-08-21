"""
Niko Visnjic, updated Aug 2015

Based on code from:
http://www.varesano.net/blog/fabio/ellipsoid-sphere-optimization-using-numpy-and-linalg
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
along with this program.  If not, see
http://www.gnu.org/licenses/gpl-3.0.en.html.

"""

import numpy
from numpy import linalg

def compute(x, y, z):
  H = numpy.array([x, y, z, -y**2, -z**2, numpy.ones(len(x))])
  H = numpy.transpose(H)
  w = x**2
  
	# Least square solution to the fitting
  (X, residues, rank, shape) = linalg.lstsq(H, w)
  
	# Offset values (center)
  OSx = X[0] / 2
  OSy = X[1] / (2 * X[3])
  OSz = X[2] / (2 * X[4])
  
  A = X[5] + OSx**2 + X[3] * OSy**2 + X[4] * OSz**2
  B = A / X[3]
  C = A / X[4]

  #print(A, B, C)

	# Scaling values 
  SCx = numpy.sqrt(A)
  SCy = numpy.sqrt(B)
  SCz = numpy.sqrt(C)
  
  return ([OSx, OSy, OSz], [SCx, SCy, SCz])

