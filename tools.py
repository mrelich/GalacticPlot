
from math import pi
#import ephem
import numpy as np
import matplotlib.pyplot as plt

#------------------------------------#
# Plot Galactic Coordinates
#------------------------------------#
def galPlot(lat, lon, origin=0, title="Galactic",projection="mollweide"):
    
    # The latitude needs to be shifted into the range
    # from [-180,180] degrees from [0,360)
    lat_shift = convertPoints(lat,origin)

    # Now update the lables on the x-axis to run
    # from 180 to -180, which is convention
    tick_labels = np.array([150,120,90,60,30,0,-30,-60,-90,-120,-150])
    
    # Create the figure
    fig = plt.figure(figsize=(10,5))
    plot = fig.add_subplot(111,projection=projection,axisbg='LightCyan')
    plot.set_title(title)
    plot.set_xticklabels(tick_labels)
    
    # Now plot the data
    plot.scatter(lat_shift,lon,marker="x")

    # Draw a grid
    plot.grid(True)

    # Plot equator
    eq = loadEquator()

    # Plot Hemisphere divide
    plot.plot(eq[:,0],eq[:,1],'r-')
    
    # Save the plot
    fig.savefig("galacticplot.png")

#------------------------------------#
# Plot Galactic Coordinates
#------------------------------------#
def eqPlot(RA, dec, origin=0, title="Equatorial",projection="mollweide"):
    
    # The right ascension needs to be shifted into the range
    # from [-180,180] degrees from [0,360)
    RA_shift = convertPoints(RA,origin)

    # Now update the lables on the x-axis to run
    # from 180 to -180, which is convention
    tick_labels = np.array([150,120,90,60,30,0,-30,-60,-90,-120,-150])
    
    # Create the figure
    fig = plt.figure(figsize=(10,5))
    plot = fig.add_subplot(111,projection=projection,axisbg='LightCyan')
    plot.set_title(title)
    plot.set_xticklabels(tick_labels)
    
    # Now plot the data
    plot.scatter(RA_shift,dec,marker="x")

    # Draw a grid
    plot.grid(True)

    # Get galactic plane points
    gal = loadGalactic()
    
    # Plot Hemisphere divide
    plot.plot(gal[:,0],gal[:,1],'r-')

#------------------------------------#
# Load equator for galactic plot
# this is to reduce dependence on
# the ephem package
#------------------------------------#
def loadEquator():
    points = []
    infile = open("equator.txt","r")
    for line in infile:
        lat = float(line.split()[0])
        lon = float(line.split()[1])
        points.append([lat,lon])
    return np.array(points)

#------------------------------------#
# Load galactic plane for equatorial plot
# this is to reduce dependence on
# the ephem package
#------------------------------------#
def loadGalactic():
    points = []
    infile = open("galacticPlane.txt","r")
    for line in infile:
        RA  = float(line.split()[0])
        dec = float(line.split()[1])
        points.append([RA,dec])
    return np.array(points)

#------------------------------------#
# Convert points to [180,-180]
#------------------------------------#
def convertPoints(points,origin):
    shifted = np.remainder(points+2*pi-origin,2*pi)
    indices   = shifted > pi
    shifted[indices] -= 2*pi
    shifted = -shifted
    return shifted

#------------------------------------#
# Get equator in galactic coords
#------------------------------------#
#def hemPoints():
#    
#    dec = 0
#    RA_array = np.arange(0,360)
#    gal_array = np.zeros((360,2))
#    for RA in RA_array:
#        eq = ephem.Equatorial(np.radians(RA),np.radians(dec))
#        ga = ephem.Galactic(eq)
#        gal_array[RA] = ga.get()
#    
#    return gal_array


#------------------------------------#
# Get equator in galactic coords
#------------------------------------#
#def galPoints():
#    
#    lat = 0
#    lon_array = np.arange(0,360)
#    eq_array = np.zeros((360,2))
#    for lon in lon_array:
#        ga = ephem.Galactic(np.radians(lon),np.radians(lat))
#        eq = ephem.Equatorial(ga)
#        eq_array[lon] = eq.get()
#    
#    return eq_array
