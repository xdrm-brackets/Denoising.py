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
print img.header.info()

### print file human-readable data ###
#print img.readableData

### print header human-readable data ###
#print img.header.readableData

### print content human-readable data ###
#print img.content.readableData




#for line in img.content.map:
#	for pixel in line:
#		print "rgb(%s, %s, %s)" % (pixel.r, pixel.g, pixel.b)
#	print

for byte in img.content.bin:
	print ord(byte),
print

img.content.unparse( img.content.map )

for byte in img.content.bin:
	print ord(byte),