#!/usr/bin/python

from penrosetiling import *
from penrosespeckler import *
from svgplotter import *

#print "establishing height for starter triangle"
#h = (GoldenRatio ** 2 - 0.5 ** 2) ** 0.5
#print h
#print ""

#print "creating first triangle"
#coords = [[0,h],[-0.5,0],[0.5,0]]
#firstTriangle = PenroseTriangle("acute", coords)
#print firstTriangle.form + str(firstTriangle.vertices)
#print ""

#print "subdividing first triangle"
#newTriangles = firstTriangle.subdivide()
#print newTriangles[0].form + str(newTriangles[0].vertices)
#print newTriangles[1].form + str(newTriangles[1].vertices)
#print ""

#print "creating initial penrose tiling"
#initialTiling = PenroseTiling("acute")
#print initialTiling.largeForm
#print initialTiling.triangles
#print ""

#print "adding first triangle to initial penrose tiling"
#initialTiling.addTriangles([firstTriangle])
#print initialTiling.triangles
#for triangle in initialTiling.triangles:
#  print triangle.vertices
#print ""

#print "running first subdividision on penrose tiling"
#firstIteration = initialTiling.divideTriangles()
#print firstIteration
#print firstIteration.largeForm
#print firstIteration.triangles
#for triangle in firstIteration.triangles:
#  print "  " + triangle.form + " " + str(triangle.vertices)
#print ""

#print "running second iteration on penrose tiling"
#secondIteration = firstIteration.divideTriangles()
#print secondIteration
#print secondIteration.largeForm
#print secondIteration.triangles
#for triangle in secondIteration.triangles:
#  print "  " + triangle.form + " " + str(triangle.vertices)
#print secondIteration.vertexSet()
#print ""

print "creating initial test pinwheel"
testPinwheel = pinwheelTiling(20)
print testPinwheel
print testPinwheel.largeForm
print testPinwheel.triangles
#for triangle in testPinwheel.triangles:
#  print "  " + triangle.form + " " + str(triangle.vertices)
#print testPinwheel.vertexSet()
print "iterating on subdivisions"
#for i in range(0,2):
#for i in range(0,4):
#for i in range(0,6):
for i in range(0,10):
  testPinwheel = testPinwheel.divideTriangles()
  print "iteration " + str(i) + " done"
print ""

print "creating speckler triangles for test tiling"
specklers = set()
speckledPinwheel = specklingTiling(testPinwheel)
speckles = speckledPinwheel.vertexSet()
print "testing plot of speckled pinwheel vertices in pinwheelsp.svg"
plotter = SvgPlotter('pinwheelsp.svg', speckles, 0.0625)
print "file prepared"
plotter.drawing.save()
print "file saved"

print ""
