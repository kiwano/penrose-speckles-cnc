#!/usr/bin/python

# A class for taking a PenroseTiling, and adding an assortment of points
# to it, that if plotted would resemble various forms of metal art.
# (If exported to a format that a CNC toolchain can use, then the result
# can be applied to metal art).

from penrosetiling import *
from math import *

# For reference:
#
# PenroseTriangle has the following API
# form (string): should be either "acute" or "obtuse"
# vertices ((float[2])[3]): a triple of x,y coodrinates with the apex of
#    the triangle as vertices[0], the base vertex coloured the same as the
#    the apex as vertices[1], and the other base vertex as vertices[2]
# PenroseTriangle[] subdivide(): a method to split the triangle, into two
#    smaller triangles, by the algorithm from Connes (returns both
#    triangles in a list)
# PenroseTriangle[] obtuseDivide(): returns the output of subdivide() if
#    form is "obtuse", otherwise returns [self]
# PenroseTriangle[] acuteDivide(): returns the output of subdivide() if
#    form is "acute", otherwise returns [self]
# boolean isVertex(point): tests whether a given point [x,y] is a vertex
#    of the triangle
#
# PenroseTiling has the following API
# largeForm (string): should be either "acute" or "obtuse"
# triangles (PenroseTriangle[]): the triangles that make up the tiling
# addTriangles(newTriangles): adds new PenroseTriangles to the tiling
# PenroseTiling divideTriangles(): divides the larger triangles to create a
#    new tiling
# set vertexSet(): returns the set of all vertices in the tiling as (x,y)
#    tuples

# Now we can define our classes; first an extension of a PenroseTriangle
# that stores the form of adjacent triangles in adjacentTriangles[], with
# the form at each index being the form for the triangle sharing the edge
# opposite the vertex with the same index. If the edge in question has no
# adjacent triangle, then "none" is stored.
# FIXME: add/document baselen, esidelen, angles

class specklingTriangle(PenroseTriangle):

  def checkAdjacent(self, vIndex, pTiling):
    possibleTriangles = pTiling.triangles
    for i in (0,1,2):
      if i != vIndex:
        newPossible = []
        for aCand in possibleTriangles:
          if aCand.isVertex(self.vertices[i]):
            newPossible.append(aCand)
        possibleTriangles = newPossible
    for triangle in possibleTriangles:
      if not triangle.isVertex(self.vertices[vIndex]):
        return triangle.form
    return "none"

  def __init__(self, pTriangle, pTiling):
    #if pTiling.largeForm != "acute":
    #  print "WARNING: speckling pattern is only nice for tilings with acute largeForm"
    self.form = pTriangle.form
    self.vertices = pTriangle.vertices
    self.adjacentTriangles = [0, 0, 0]
    for i in (0,1,2):
      self.adjacentTriangles[i] = self.checkAdjacent(i, pTiling)
    angles = {0: atan2(self.vertices[1][1] - self.vertices[0][1], self.vertices[1][0] - self.vertices[0][0]),
        0.25: 0,
        0.33: 0,
        0.5: 0,
        0.67: 0,
        0.75: 0,
	1: atan2(self.vertices[2][1] - self.vertices[0][1], self.vertices[2][0] - self.vertices[0][0])}
    if angles[1]-angles[0] > pi:
      angles[1] = angles[1] - 2 * pi
    if angles[0]-angles[1] > pi:
      angles[0] = angles[0] - 2 * pi
    angles[0.25] = (3 * angles[0] + angles[1]) / 4
    angles[0.33] = (2 * angles[0] + angles[1]) / 3
    angles[0.5] = (angles[0] + angles[1]) / 2
    angles[0.67] = (angles[0] + 2 * angles[1]) / 3
    angles[0.75] = (angles[0] + 3 * angles[1]) / 4
    self.angles = angles
    self.baselen = hypot(self.vertices[1][1] - self.vertices[2][1], self.vertices[1][0] - self.vertices[2][0])
    self.esidelen = hypot(self.vertices[1][1] - self.vertices[0][1], self.vertices[1][0] - self.vertices[0][0])
    #debugstring = "triangle with vertices: (" + str(self.vertices[0][0]) + "," + str(self.vertices[0][1]) + "), ("
    #debugstring = debugstring + str(self.vertices[1][0]) + "," + str(self.vertices[1][1]) + "), ("
    #debugstring = debugstring + str(self.vertices[1][0]) + "," + str(self.vertices[2][1]) + ") has base length of "
    #debugstring = debugstring + str(self.baselen) + " other edge length of " + str(self.esidelen)
    #debugstring = debugstring + " and and angle set: " + str(self.angles)
    #print debugstring
    #print "0:    " + str(self.angles[0])
    #print "0.25: " + str(self.angles[0.25])
    #print "0.33: " + str(self.angles[0.33])
    #print "0.5:  " + str(self.angles[0.5])
    #print "0.67: " + str(self.angles[0.67])
    #print "0.75: " + str(self.angles[0.75])
    #print "1:    " + str(self.angles[1])

  def getBaseSpeckles(self):
    out = set()
    if self.form == "obtuse":
      if self.adjacentTriangles[0] == "obtuse":
        for i in (2,3,4,5):
          cpoint = ( ( self.vertices[1][0] * i + self.vertices[2][0] * (6-i) ) / 6,
              ( self.vertices[1][1] * i + self.vertices[2][1] * (6-i) ) / 6 )
          out.add(cpoint)
      if self.adjacentTriangles[0] == "acute" or self.adjacentTriangles[0] == "none":
        for i in (2,3,4,5):
          cpoint = ( ( self.vertices[1][0] * i + self.vertices[2][0] * (6-i) ) / 6,
              ( self.vertices[1][1] * i + self.vertices[2][1] * (6-i) ) / 6 )
          out.add(cpoint)
    if self.form == "acute":
      if self.adjacentTriangles[0] == "acute" or self.adjacentTriangles[0] == "none":
        for i in (1,2,3):
          cpoint = ( ( self.vertices[1][0] * i + self.vertices[2][0] * (4-i) ) / 4,
              ( self.vertices[1][1] * i + self.vertices[2][1] * (4-i) ) / 4 )
          out.add(cpoint)
      if self.adjacentTriangles[0] == "obtuse":
        for angle in (0.25, 0.5, 0.75):
          cpoint = ( (self.vertices[0][0] + self.esidelen * cos(self.angles[angle])),
              (self.vertices[0][1] + self.esidelen * sin(self.angles[angle])) )
          out.add(cpoint)
    return out

  def getMatchSpeckles(self):
    out = set()
    if self.form == "obtuse":
      if self.adjacentTriangles[2] == "obtuse" or self.adjacentTriangles[2] == "none":
        #if self.adjacentTriangles[0] == "obtuse":
        #  for i in (1,2,3):
        #    cpoint = ( ( self.vertices[0][0] * i + self.vertices[1][0] * (4-i) ) / 4,
        #        ( self.vertices[0][1] * i + self.vertices[1][1] * (4-i) ) / 4)
        #    out.add(cpoint)
        for i in (2,3):
          cpoint = ( ( self.vertices[0][0] * i + self.vertices[1][0] * (4-i) ) / 4,
              ( self.vertices[0][1] * i + self.vertices[1][1] * (4-i) ) / 4)
          out.add(cpoint)
    if self.form == "acute":
      if self.adjacentTriangles[2] == "acute" or self.adjacentTriangles[2] == "none":
        for i in (1,2,3,4,5):
          cpoint = ( ( self.vertices[0][0] * i + self.vertices[1][0] * (6-i) ) / 6,
              ( self.vertices[0][1] * i + self.vertices[1][1] * (6-i) ) / 6 )
          out.add(cpoint)
    return out

  def getUnmatchSpeckles(self):
    out = set()
    if self.form == "obtuse":
      if self.adjacentTriangles[1] == "obtuse" or self.adjacentTriangles[1] == "none":
        for i in (1,2,3):
          cpoint = ( ( self.vertices[0][0] * i + self.vertices[2][0] * (4-i) ) / 4,
              ( self.vertices[0][1] * i + self.vertices[2][1] * (4-i) ) / 4)
          out.add(cpoint)
    if self.form == "acute":
      if self.adjacentTriangles[1] == "acute" or self.adjacentTriangles[1] == "none":
        for i in (1,2,3,4):
          cpoint = ( ( self.vertices[0][0] * i + self.vertices[2][0] * (6-i) ) / 6,
              ( self.vertices[0][1] * i + self.vertices[2][1] * (6-i) ) / 6 )
          out.add(cpoint)
    return out

  def getCentreSpeckles(self):
    out = set()
    if self.form == "obtuse":
      cpoint = ( (1.5 * self.vertices[0][0] + self.vertices[1][0] + self.vertices[2][0]) / 3.5,
          (1.5 * self.vertices[0][1] + self.vertices[1][1] + self.vertices[2][1]) / 3.5 )
      out.add(cpoint)
    if self.form == "acute":
      #for adist in ( (self.esidelen / 3), (self.esidelen / 2) ):
      #  cpoint = ( (self.vertices[0][0] + adist * cos(self.angles[0.5])),
      #      (self.vertices[0][1] + adist * sin(self.angles[0.5])) )
      #  out.add(cpoint)
      adist = self.esidelen / 2
      cpoint = ( (self.vertices[0][0] + adist * cos(self.angles[0.5])),
          (self.vertices[0][1] + adist * sin(self.angles[0.5])) )
      out.add(cpoint)
      for adist in ( (2 * self.esidelen / 3), (5 * self.esidelen / 6) ):
        for angle in (0.33, 0.67):
          cpoint = ( (self.vertices[0][0] + adist * cos(self.angles[angle])),
              (self.vertices[0][1] + adist * sin(self.angles[angle])) )
          out.add(cpoint)
    return out

  def getSpeckles(self):
    out = set()
    for vertex in self.vertices:
      out.add((vertex[0], vertex[1]))
    for vertex in self.getBaseSpeckles():
      out.add(vertex)
    for vertex in self.getMatchSpeckles():
      out.add(vertex)
    for vertex in self.getUnmatchSpeckles():
      out.add(vertex)
    for vertex in self.getCentreSpeckles():
      out.add(vertex)
    return out


class specklingTiling(object):

  def __init__(self, pTiling):
    if pTiling.largeForm != "acute":
      print "WARNING: speckling pattern is only nice for tilings with acute largeForm"
    self.striangles = []
    for triangle in pTiling.triangles:
      newStriangle = specklingTriangle(triangle, pTiling)
      self.striangles.append(newStriangle)

  def vertexSet(self):
    out = set()
    for triangle in self.striangles:
      for vertex in triangle.getSpeckles():
        out.add(vertex)
    return out
