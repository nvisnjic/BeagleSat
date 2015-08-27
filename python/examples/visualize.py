from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.patches as mpatches

import numpy 
import random

import argparse
import csv

import beaglesat.correction.algorithms as BeagleCorrection


def visualize3D(rawDataFile, correctedDataFile): 
    """ Helper function to visualize corrected data points """


    fig = plt.figure(figsize=plt.figaspect(1))  # Square figure
    ax = fig.add_subplot(111, projection="3d", aspect="equal")

      
    XYZdata = loadData(rawDataFile)
    #XYZdata = loadData("../data/referenceData")
    #XYZdata = loadData("../data/magData2015-08-21-13-36-23")
   
    #print(XYZdata)

    x = XYZdata[0]
    y = XYZdata[1]
    z = XYZdata[2]

    #Bh IGRF, magnitude of magnetic field to fit to
    Bh = max(numpy.mean(abs(x)), numpy.mean(abs(y)), numpy.mean(abs(z)))

    if correctedDataFile is None:
      # Corrected data file not set on input, then compute corrected data 
      # using raw data from input file -f filename

      # Fit data, same algorithm used in the computeCorrectedData() method
      (offsets, scale) = BeagleCorrection.invariantFitting.compute(x, y, z)

      print("Offsets: %s" % (offsets))
      print("Scaling: %s" % (scale))


      # fix offset
      fixed_x = x - numpy.ones(len(x)) * offsets[0] 
      fixed_y = y - numpy.ones(len(y)) * offsets[1] 
      fixed_z = z - numpy.ones(len(z)) * offsets[2] 

      # fix scale
      fixed_x = fixed_x / scale[0] * Bh
      fixed_y = fixed_y / scale[1] * Bh
      fixed_z = fixed_z / scale[2] * Bh

    else:
      # Corrected data file set, use that data for plotting
      corrected = loadData(correctedDataFile)
  
      fixed_x = corrected[0]
      fixed_y = corrected[1]
      fixed_z = corrected[2]

    # scale the point a bit out to print nicely outside the sphere
    plot_fixed_x = fixed_x * 1.02
    plot_fixed_y = fixed_y * 1.02
    plot_fixed_z = fixed_z * 1.02

    # Print some points, not all
    if(numpy.size(x) > 1000 ): # That's too much points
        # Centimate (is that a word?) points for plotting
        # (too much points makes the graph slow)
        plot_x = x[0::100]
        plot_y = y[0::100]
        plot_z = z[0::100]

        plot_fixed_x = plot_fixed_x[0::100]
        plot_fixed_y = plot_fixed_y[0::100]
        plot_fixed_z = plot_fixed_z[0::100]
    else: 
      # For printing, original values stay in x, y & z
      plot_x = x
      plot_y = y
      plot_z = z


    print("IGRF set based on mean value of measurements: Bh = %f" % (Bh)) 
    
    # Make a sphere dataset for comparison
    # Set of all spherical angles:
    u = numpy.linspace(0, 2 * numpy.pi, 100)
    v = numpy.linspace(0, numpy.pi, 100)

    # Cartesian coordinates that correspond to the spherical angles:
    # (this is the equation of an ellipsoid):
    x_surf = Bh * numpy.outer(numpy.cos(u), numpy.sin(v))    
    y_surf = Bh * numpy.outer(numpy.sin(u), numpy.sin(v))   
    z_surf = Bh * numpy.outer(numpy.ones_like(u), numpy.cos(v))


    # Plot sphere with radius Bh
    ref = ax.plot_wireframe(x_surf, y_surf, z_surf,  rstride=4, cstride=4, color="blue", alpha=0.4)
            

    # plot read data
    orig = ax.scatter(plot_x, plot_y, plot_z, color="magenta")

    # plot corrected data
    corr = ax.scatter(plot_fixed_x, plot_fixed_y, plot_fixed_z, c="blue")

    # Adjustment of the axes, so that they all have the same span:
    max_radius = max(max(plot_x), max(plot_y), max(plot_z)) * 1.2
    for axis in 'xyz':
        getattr(ax, 'set_{}lim'.format(axis))((-max_radius, max_radius))

    # Label axes    
    ax.set_xlabel('X Axis')    
    ax.set_ylabel('Y Axis')    
    ax.set_zlabel('Z Axis')    
   
    # Proxy artist, aka fakes for legend
    orig_proxy = matplotlib.lines.Line2D([0],[0], linestyle="none", c='magenta', marker = '.', markersize = 15)
    corr_proxy = matplotlib.lines.Line2D([0],[0], linestyle="none", c='blue', marker = '.', markersize = 15)
    
    # Add legend    
    ax.legend([orig_proxy, corr_proxy], ['Raw data', 'Corrected data'], numpoints = 1)

    plt.show()



def loadData(file):
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

  XYZdata = numpy.array([dataX, dataY, dataZ]) 
  return XYZdata


if __name__ == "__main__": 
    
  parser = argparse.ArgumentParser(description='Process a dataset and plot the data before and after')
  parser.add_argument('-f', metavar='filename',  required=True,
          help=' Path to file for which to generate 3D plots')
  parser.add_argument('-c', metavar='correctedFile',  required=False,
          help=" Path to corrected data file; if ommited will be generated from raw data given with -f")
  args = parser.parse_args()
    
  visualize3D(args.f, args.c)


