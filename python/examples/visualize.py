from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from cal_lib import *

import numpy as np
import random

import argparse
import csv


def visualize3D():
    """ Helper function to visualize corrected data points """


    fig = plt.figure(figsize=plt.figaspect(1))  # Square figure
    ax = fig.add_subplot(111, projection="3d", aspect="equal")

      
    XYZdata = loadData("./testReads")
   
    print(XYZdata)

    x = XYZdata[0]
    y = XYZdata[1]
    z = XYZdata[2]


    # Fit data
    (offsets, scale) = calibrate(x, y, z)

    print(offsets)
    print(scale)

    # For printing
    plot_x = x
    plot_y = y
    plot_z = z

    # fix offset
    fixed_x = x - numpy.ones(len(x)) * offsets[0] 
    fixed_y = y - numpy.ones(len(y)) * offsets[1] 
    fixed_z = z - numpy.ones(len(z)) * offsets[2] 

    #Bh IGRF, magnitude of magnetic field to fit to
    Bh = max(numpy.mean(abs(x)), numpy.mean(abs(y)), numpy.mean(abs(z)))
    print(Bh)
    # fix scale
    fixed_x = fixed_x / scale[0] * Bh
    fixed_y = fixed_y / scale[1] * Bh
    fixed_z = fixed_z / scale[2] * Bh

    # scale the point a bit out to print nicely outside the sphere
    plot_fixed_x = fixed_x * 1.02
    plot_fixed_y = fixed_y * 1.02
    plot_fixed_z = fixed_z * 1.02



    if(np.size(x) > 1000 ): # That's too much points
    #if(0 ): # That's too much points
        # Centimate (is that a word?) points for plotting
        # (too much points makes the graph slow)
        plot_x = plot_x[0::100]
        plot_y = plot_y[0::100]
        plot_z = plot_z[0::100]

        plot_fixed_x = plot_fixed_x[0::100]
        plot_fixed_y = plot_fixed_y[0::100]
        plot_fixed_z = plot_fixed_z[0::100]



    # Make a sphere dataset for comparison
    # Set of all spherical angles:
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)

    # Cartesian coordinates that correspond to the spherical angles:
    # (this is the equation of an ellipsoid):
    x_surf = Bh * np.outer(np.cos(u), np.sin(v))    
    y_surf = Bh * np.outer(np.sin(u), np.sin(v))   
    z_surf = Bh * np.outer(np.ones_like(u), np.cos(v))



    # Plot sphere with radius Bh
    ax.plot_wireframe(x_surf, y_surf, z_surf,  rstride=4, cstride=4, color="blue", alpha=0.4)
            

    # plot simulated or read data
    ax.scatter(plot_x, plot_y, plot_z, color="magenta")

    # plot corrected data
    ax.scatter(plot_fixed_x, plot_fixed_y, plot_fixed_z, c="red")

    # Adjustment of the axes, so that they all have the same span:
    max_radius = max(max(plot_x), max(plot_y), max(plot_z)) * 1.2
    for axis in 'xyz':
        getattr(ax, 'set_{}lim'.format(axis))((-max_radius, max_radius))

    plt.show()




def loadData(file):
  """ Read data from a CSV file """

  """
  data = numpy.genfromtxt(file, dtype=float, delimiter=' ', names=True)

  # Reshape back to previous format of numpy.array (list of lists)
  Ldata = [list(elem) for elem in data]
  XYZdata = numpy.reshape(Ldata, [3, len(Ldata)])
  """
  
  dataX = [] 
  dataY = [] 
  dataZ = [] 
  with open(file, "r") as f:
    reader = csv.reader(f, delimiter=" ")
    names = reader.next()
    for row in reader:
      print ', '.join(row)
      (x, y, z) = row
      dataX.append(float(x)) 
      dataY.append(float(y)) 
      dataZ.append(float(z))

  XYZdata = numpy.array([dataX, dataY, dataZ]) 
  return XYZdata



if __name__ == "__main__": visualize3D()
