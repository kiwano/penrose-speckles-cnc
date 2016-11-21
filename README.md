# penrose-speckles-cnc
Makes SVGs of dots based on a Penrose tiling.

A while back, looking at some metal art consisting of intricate dimpling of
silverware with many small hammer/punch strikes, I thought it'd be kinda neat
to make something similar where the dimpling is based on a Penrose tiling.

After doing some sketches by hand, I came up with a rough idea of a speckle
layout that I'd like, and then started writing this bit of code to prepare a
tiling and then create a set of speckles for it.

The pattern of speckles is output as an SVG file because I have access to
some CNC tooling that can put these patterns in actual metal, and some CAM
software which can import SVG files to prepare toolpaths from.
