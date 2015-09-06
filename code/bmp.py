# ~*~ encoding: utf-8 ~*~ #
###########################
#   TRAITEMENT D'IMAGES   #
###########################

# classes
from classes import *

import sys

img = BMPFile( sys.argv[1] )

print img.header.info()

print img.readableData

for line in img.map:
	for pixel in line:
		print "rgb(%s, %s, %s)" % (pixel.r, pixel.g, pixel.b)
	print	