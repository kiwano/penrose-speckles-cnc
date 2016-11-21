#!/usr/bin/python

# Some useful classes for constructing a nd manipulating Penrose tilings.
# Each tiling is stored as a collection of triangles, with a small amount
# of metadats, and each triangle is in turn, stored as a triple of
# vertices, along with a small amount of its own metadata.
#
# A few simple patterns are included as derived classes, in order to
# provide some constructors to help generate certain nice tilngs quickly.

# There is very little robustness in this class to prevent people from
# definind malformed tilings; this may turn out in the long run to be a
# good thing.


from math import sin, cos, radians

# Before we get to any classes, let's just get ourselves a handy copy of
# golden ratio, since it shows up everyhere in Penrose tilings

GoldenRatio = (1 + 5 ** 0.5) / 2

# Likewise, let's add a function that finds the point between two given
# points which lies on the line segment between them, and whose distance
# from the second point is the golden ratio times its distance from the
# first point

def goldenSect(closepoint, farpoint):
  # print "computing point between " + str(closepoint) + " (close) and " + str(farpoint) + " (far)"
  x = (farpoint[0] * (GoldenRatio - 1) + closepoint[0]) / GoldenRatio
  y = (farpoint[1] * (GoldenRatio - 1) + closepoint[1]) / GoldenRatio
  # print "point is " + str([x,y])
  return [x, y]


# First the class of triangles for the tilings
#
# The penrose triangle class contains a string (form) indicating whether
# it is acute or obtuse, and a list of vertices (vertices).
#
# The vertices are a 3 element list, each element of which is a 2 element
# list of floating point numbers. These numbers represent the x and y
# coordinates of the apex, the base vertex with the same colouring as the
# apex, and the other base vertes, in that order.
#
# (The colouring is the same colouring described in the Penrose tiling
# appendix of Noncommutative Geometry, and is used to identify where to
# add a new vertex when splitting the triangle)

class PenroseTriangle(object):

  def __init__(self, cform, cvertices):
    self.form = cform
    self.vertices = cvertices


  # Here's a general function for splitting up a triangle

  def subdivide(self):
    if self.form == "obtuse":
      newpoint = goldenSect(self.vertices[2], self.vertices[1])
      newObtuse = PenroseTriangle("obtuse",
	[newpoint, self.vertices[2], self.vertices[0]])
      newAcute = PenroseTriangle("acute",
	[self.vertices[1], self.vertices[0], newpoint])
      return [newObtuse, newAcute]
    elif self.form == "acute":
      # print "splitting an acute triangle"
      newpoint = goldenSect(self.vertices[1], self.vertices[0])
      # print "by adding point " + str(newpoint) + " between " + str(self.vertices[1]) + " and " + str(self.vertices[0])
      newObtuse = PenroseTriangle("obtuse",
	[newpoint, self.vertices[2], self.vertices[0]])
      newAcute = PenroseTriangle("acute",
	[self.vertices[2], newpoint, self.vertices[1]])
      return [newObtuse, newAcute]
    else:
      print "There's a broken triangle here."
      return [self]


  # To make life a little easier in the tiling class, here are a pair of
  # functions that split the triangle only if it has the correct form, 
  # and returns self (unsplit) otherwise

  def obtuseDivide(self):
    if self.form == "obtuse":
      return self.subdivide()
    else:
      return [self]

  def acuteDivide(self):
    if self.form == "acute":
      return self.subdivide()
    else:
      return [self]


  # Finally, to help check adjacency for the purposes of drawing and
  # decorating tilings, here's a function that checks of a given point
  # is a vertex of this triangle

  def isVertex(self, point):
    if ((point[0] == self.vertices[0][0]) and
	(point[1] == self.vertices[0][1]) ):
      return True
    if ((point[0] == self.vertices[1][0]) and
	(point[1] == self.vertices[1][1])):
      return True
    if ((point[0] == self.vertices[2][0]) and
	(point[1] == self.vertices[2][1])):
      return True
    return False



# Now that we have triangles, we can construct the class for the Penrose
# tilings. This class contains a list of PenroseTriengles (triangles) making
# up the tiling, and a string (largeForm) indicating which of the forms of
# triangle is the larger triangle

class PenroseTiling(object):

  def __init__(self, lform):
    self.largeForm = lform
    self.triangles = []

  def addTriangles(self, newTriangles):
    for triangle in newTriangles:
      self.triangles.append(triangle)

  def divideTriangles(self):
    if self.largeForm == "acute":
      newTiling = PenroseTiling("obtuse")
      for triangle in self.triangles:
        newTiling.addTriangles(triangle.acuteDivide())
    else:
      newTiling = PenroseTiling("acute")
      for triangle in self.triangles:
         newTiling.addTriangles(triangle.obtuseDivide())
    return newTiling

  def vertexSet(self):
    out = set()
    for triangle in self.triangles:
      for vertex in triangle.vertices:
        out.add((vertex[0], vertex[1]))
    return out


# Now the derived classes for simple patterns

class pinwheelTiling(PenroseTiling):

  centre = [0,0]
  ring = []
  for i in range(0, 10):
    angle = radians(36*i)
    ring.append([cos(angle), sin(angle)])
  

  def __init__(self, radius):
    self.largeForm = "acute"
    self.triangles = []
    ringr = []
    for i in range(0, 10):
      ringr.append([radius*self.ring[i][0], radius*self.ring[i][1]])
    for i in range(0, 4):
      triangle1 = PenroseTriangle("acute", [self.centre, ringr[2*i], ringr[2*i+1]])
      triangle2 = PenroseTriangle("acute", [self.centre, ringr[2*i+2], ringr[2*i+1]])
      self.triangles.append(triangle1)
      self.triangles.append(triangle2)
    triangle1 = PenroseTriangle("acute", [self.centre, ringr[8], ringr[9]])
    triangle2 = PenroseTriangle("acute", [self.centre, ringr[0], ringr[9]])
    self.triangles.append(triangle1)
    self.triangles.append(triangle2)
