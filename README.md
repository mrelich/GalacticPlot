GalacticPlot
============

A set of python tools to plot in Equatorial or Galactic Coordinate systems following normal conventions.

To generate the random data, the coordinate-utils package is
needed from icecube software package.  So for now, I will 
generate that on grappa.  

The plotting script is an example which will read in data
from a root tree, put it into a list of points, and then 
plot in galactic and equatorial coordinates.  

To execute:
1.) ipython -pylab
2.) from plot improt *
3.) plotTree() <---- This will be updated