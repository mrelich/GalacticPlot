
from math import pi
import ephem
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

    # Plot Hemisphere line
    hp = hemPoints()
    
    # Convert to range [180,-180]
    hp_lat = hp[:,0]
    hp_lat_shift = convertPoints(hp_lat,origin)

    # Now reform and sort
    remade = np.zeros((360,2))
    for i in range(len(hp_lat_shift)):
        remade[i] = (hp_lat_shift[i],hp[i][1])
    remade = remade[remade[:,0].argsort()]

    # Plot Hemisphere divide
    plot.plot(remade[:,0],remade[:,1],'r-')


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

    # Plot Galactic plane
    gal = galPoints()
    
    # Convert to range [180,-180]
    gal_RA = gal[:,0]
    gal_RA_shift = convertPoints(gal_RA,origin)

    # Now reform and sort
    remade = np.zeros((360,2))
    for i in range(len(gal_RA_shift)):
        remade[i] = (gal_RA_shift[i],gal[i][1])
    remade = remade[remade[:,0].argsort()]

    # Plot Hemisphere divide
    plot.plot(remade[:,0],remade[:,1],'r-')
    
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
def hemPoints():
    
    dec = 0
    RA_array = np.arange(0,360)
    gal_array = np.zeros((360,2))
    for RA in RA_array:
        eq = ephem.Equatorial(np.radians(RA),np.radians(dec))
        ga = ephem.Galactic(eq)
        gal_array[RA] = ga.get()
    
    return gal_array


#------------------------------------#
# Get equator in galactic coords
#------------------------------------#
def galPoints():
    
    lat = 0
    lon_array = np.arange(0,360)
    eq_array = np.zeros((360,2))
    for lon in lon_array:
        ga = ephem.Galactic(np.radians(lon),np.radians(lat))
        eq = ephem.Equatorial(ga)
        eq_array[lon] = eq.get()
    
    return eq_array
