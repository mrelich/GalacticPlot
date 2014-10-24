
from math import pi
import ephem
import numpy as np
import matplotlib.pyplot as plt
from IPython.core.display import HTML
import sys

from tools import *
from ROOT import TTree, TFile

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
    l_lat = []
    l_lon = []
    l_RA  = []
    l_dec = []
    for ent in range(nEntries):
        tree.GetEvent(ent)
        l_lat.append(lat[0])
        l_lon.append(lon[0])
        l_RA.append(ra[0])
        l_dec.append(dec[0])

    # Now plot galactic
    v_lat = np.array(l_lat)
    v_lon = np.array(l_lon)
    galPlot(v_lat, v_lon)

    # Now plot RA and dec
    v_RA  = np.array(l_RA)
    v_dec = np.array(l_dec)
    eqPlot(v_RA,v_dec)
    



