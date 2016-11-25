#!/usr/bin/python

from penrosetiling import *
from penrosespeckler import *
from svgplotter import *
from math import sin, cos, radians

tradius = 20
sradius = 0.0625

print "creating initial pinwheel"
testPinwheel = pinwheelTiling(tradius)
#print testPinwheel
#print testPinwheel.largeForm
#print testPinwheel.triangles
#for triangle in testPinwheel.triangles:
#  print "  " + triangle.form + " " + str(triangle.vertices)
#print testPinwheel.vertexSet()
print "iterating on subdivisions"
for i in range(0,10):
  testPinwheel = testPinwheel.divideTriangles()
  print "iteration " + str(i) + " done"
print ""

print "setting up an enveloping pentagon"
pentvertices = []
for i in range(0,5):
  angle = radians(72*i)
  pentvertices.append([(tradius+0.07)*cos(angle), (tradius+0.07)*sin(angle)])
# pentagon lines will be stored as
# the reciprocal of the slope in the first coordinate, and
# the x intercept as the second coordinate
pentlines = []
for i in range(0,4):
  sloper = (pentvertices[i+1][0] - pentvertices[i][0]) / (pentvertices[i+1][1] - pentvertices[i][1])
  xint = pentvertices[i][0] - pentvertices[i][1] * sloper
  pentlines.append([sloper, xint])
sloper = (pentvertices[0][0] - pentvertices[4][0]) / (pentvertices[0][1] - pentvertices[4][1])
xint = pentvertices[4][0] - pentvertices[4][1] * sloper
pentlines.append([sloper, xint])

print "creating speckler triangles for test tiling"
specklecount = 0
speckles = set()
speckledPinwheel = specklingTiling(testPinwheel)
for speckle in speckledPinwheel.vertexSet():
  if ( speckle[0] <= pentlines[0][0]*speckle[1] + pentlines[0][1] and
       speckle[0] >= pentlines[1][0]*speckle[1] + pentlines[1][1] and
       speckle[0] >= pentlines[2][0]*speckle[1] + pentlines[2][1] and
       speckle[0] >= pentlines[3][0]*speckle[1] + pentlines[3][1] and
       speckle[0] <= pentlines[4][0]*speckle[1] + pentlines[4][1] ):
    speckles.add(speckle)
    specklecount = specklecount + 1
print "plotting " + str(specklecount) + " points in pentwheel.svg"
plotter = SvgPlotter('pentwheel.svg', speckles, sradius)
print "file prepared"
plotter.drawing.save()
print "file saved"

print ""
