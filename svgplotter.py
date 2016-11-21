#!/usr/bin/python

# A class for taking a set of 2-element tuples, and plotting them as
# circles in an SVG file for inspection (or conversion to DXF for CNC
# fun times, or...)

# This was initially created for fiddling with Penrose-tiling-based
# sheet metal art.

import svgwrite

class SvgPlotter(object):

  def __init__(self, filename, vertices, plotrad):
    minx = float('inf')
    miny = float('inf')
    maxx = float('-inf')
    maxy = float('-inf')
    for vertex in vertices:
      x, y = vertex
      minx = min(x, minx)
      maxx = max(x, maxx)
      miny = min(y, miny)
      maxy = max(y, maxy)
      xspan = 2*plotrad + maxx-minx
      yspan = 2*plotrad + maxy-miny
      dsize = (str(xspan), str(yspan))
    xbottom = minx - plotrad
    ybottom = miny - plotrad
    trVertices = set()
    for vertex in vertices:
      x, y = vertex
      trVertices.add((x-xbottom, y-ybottom))
    print str(minx) + " " + str(maxx) + " " + str(miny) + " " + str(maxy)
    print dsize
    self.drawing = svgwrite.Drawing(filename, size=dsize, profile="tiny")
    for vertex in trVertices:
      self.drawing.add(self.drawing.circle(vertex, plotrad, fill='black'))

