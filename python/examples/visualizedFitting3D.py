from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from cal_lib import *

import numpy as np
import random

import argparse

import bbio
from beaglesat import beagleSat

parser = argparse.ArgumentParser(description='Process a dataset and plot the data before and after')
parser.add_argument('readFile', metavar='readFile', type=int,
                   help='Specifier for reading acc.txt (1) or generating \
                        simulated dataset (0)')
args = parser.parse_args()


fig = plt.figure(figsize=plt.figaspect(1))  # Square figure
ax = fig.add_subplot(111, projection="3d", aspect="equal")




# Make a sphere dataset for comparison
# Set of all spherical angles:
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)

Bh = 1
# Cartesian coordinates that correspond to the spherical angles:
# (this is the equation of an ellipsoid):
x_surf = Bh * np.outer(np.cos(u), np.sin(v))    
y_surf = Bh * np.outer(np.sin(u), np.sin(v))   
z_surf = Bh * np.outer(np.ones_like(u), np.cos(v))


# Temporary for testing
read_file = args.readFile
if(read_file): 
    """
  	acc_f = open("acc.txt", 'r')                          
    acc_x = []
    acc_y = []    
    acc_z = []         
    
    #Add offset for visibility                                   
    ox = -1.8
    oy = -1.2
    oz = -1.5
    
    for line in acc_f:                  
        reading = line.split()             
        acc_x.append(int(reading[0]) / 16384.0 * 2 + ox)    
        acc_y.append(int(reading[1]) / 16384.0 * 3 + oy)    
        acc_z.append(int(reading[2]) / 16384.0 * 1 + oz)    
    """
  
    Laika = BeagleSat()
    
    XYZdata = Laika.loadData('./data/tempStore')

    x = XYZdata[0]
    y = XYZdata[1]
    z = XYZdata[2]
else:
    # Generate simulated dataset from sphere dataset
    # Distort radii (scale)
    a = 1.8
    b = 3.2
    c = 2.7

    # Distort center (offset)
    ox = 1.8
    oy = -1.2
    oz = -1.5

    # Random noise max range = +/- noise
    noise = 0.1

    rx = a / 2.0
    ry = b / 2.0
    rz = c / 2.0

    x = x_surf.flatten()
    y = y_surf.flatten()
    z = z_surf.flatten()

    # Reduce number of points
    x = x[1::85] 
    y = y[1::85]
    z = z[1::85]

    # distort radii
    x = x * rx
    y = y * ry
    z = z * rz

    # Offset points
    x = x + np.ones(np.size(x)) * ox
    y = y + np.ones(np.size(y)) * oy
    z = z + np.ones(np.size(z)) * oz

    # Add noise
    x += x * random.uniform(-1*noise,noise)
    y += y * random.uniform(-1*noise,noise)
    z += z * random.uniform(-1*noise,noise)


# Fit data
(offsets, scale) = Beaglesat.correction.computeInvariantFactors(x, y, z)

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
Bh = 1
# fix scale
fixed_x = fixed_x / scale[0] * Bh
fixed_y = fixed_y / scale[1] * Bh
fixed_z = fixed_z / scale[2] * Bh

# scale the point a bit out to print nicely outside the sphere
plot_fixed_x = fixed_x * 1.02
plot_fixed_y = fixed_y * 1.02
plot_fixed_z = fixed_z * 1.02



if(np.size(x) > 1000 ): # That's too much points
    # Centimate (is that a word?) points for plotting
    # (too much points makes the graph slow)
    plot_x = plot_x[0::100]
    plot_y = plot_y[0::100]
    plot_z = plot_z[0::100]

    plot_fixed_x = plot_fixed_x[0::100]
    plot_fixed_y = plot_fixed_y[0::100]
    plot_fixed_z = plot_fixed_z[0::100]




# Plot sphere with radius Bh
ax.plot_wireframe(x_surf, y_surf, z_surf,  rstride=4, cstride=4, color="blue", alpha=0.4)
        

# plot simulated read data
ax.scatter(plot_x, plot_y, plot_z, color="magenta")

# plot corrected data
ax.scatter(plot_fixed_x, plot_fixed_y, plot_fixed_z, c="red")

# Adjustment of the axes, so that they all have the same span:
max_radius = max(scale[0], scale[1], scale[2]) * 1.5
for axis in 'xyz':
    getattr(ax, 'set_{}lim'.format(axis))((-max_radius, max_radius))

plt.show()
