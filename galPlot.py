
from math import pi
import ephem
import numpy as np
import matplotlib.pyplot as plt
from IPython.core.display import HTML
import sys

from ROOT import TTree, TFile

#------------------------------------#
# Method to plot set of points
#------------------------------------#
def plot(points):

    # When Plotting it is useful to have a 
    # common range with others.  I have 
    # seen most plots go from 180,-180
    # for galactic coordinates.  So I 
    # will do the same.
    x = np.remainder(points[:,0]+2*pi,2*pi)
    ind = x > pi
    x[ind] -=2*pi  # scale conversiont to [-180,180]
    x=-x          # reverse scalea
    tick_labels = np.array([150,120,90,60,30,0,330,300,270,240,210])
    tick_labels = np.remainder(tick_labels+360,360)

    # make the main graph
    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111,projection="mollweide",axisbg="LightCyan")
    ax.grid(True)

    # Add decorations -- TODO

    # Plot the points
    #for pt in points:
    #    print "Plotting point: ", pt[0], pt[1]
    #    #ax.scatter(pt[0],pt[1])
    #    ax.scatter(pt[0],pt[1])
    ax.scatter(x,points[:,1])

def plotEq():

    # Draw northern/southern hemisphere divide
    ra = 0
    dec_array = np.arange(-90,90)
    ga_array  = np.zeros((360,2))
    for i in range(len(dec_array)):
        dec = dec_array[i]
        eq = ephem.Equatorial(np.radians(ra),np.radians(dec))
        ga = ephem.Galactic(eq)
        ga_array[i] = ga.get()
    
    plot(ga_array)


#------------------------------------#
# Method to read stuff in from tree
#------------------------------------#
def plotTree(name):
    #infile = TFile("test.root")
    infile = TFile(name)
    tree   = infile.Get("tree")
    nEntries = tree.GetEntries();

    # Set vars
    ra = np.zeros(1,dtype=float)
    dec = np.zeros(1,dtype=float)
    lat = np.zeros(1,dtype=float)
    lon = np.zeros(1,dtype=float)
    tree.SetBranchAddress("ra",ra)
    tree.SetBranchAddress("dec",dec)
    tree.SetBranchAddress("lon",lon)
    tree.SetBranchAddress("lat",lat)


    # Loop and get points
    points = []
    for ent in range(nEntries):
        tree.GetEvent(ent)
        #points.append((ra[0],dec[0]))
        points.append((lat[0],lon[0]))
        #if len(points) > 2 : break

    # Now plot
    v_points = np.array(points)
    plot(v_points)
    



