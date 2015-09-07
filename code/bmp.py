# ~*~ encoding: utf-8 ~*~ #
###########################
#   TRAITEMENT D'IMAGES   #
###########################

# classes
from classes import *

import sys

img = BMPFile()
img.parse( sys.argv[1] );


### print header human-readable data ###
#print img.header.info()

### print file human-readable data ###
#print img.intData

### print header human-readable data ###
#print img.header.intData

### print content human-readable data ###
#print img.content.intData


for line in img.content.map:
	for pixel in line:
		print "rgb(%s, %s, %s)" % (pixel.r, pixel.g, pixel.b)
	print