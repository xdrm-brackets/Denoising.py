# ~*~ encoding: utf-8 ~*~ #
###########################
#   TRAITEMENT D'IMAGES   #
###########################

# classes
from classes import *

import sys

# lecture du fichier
binFile = ""
with open( sys.argv[1] ) as file:
	for byte in file.read():
		binFile += byte;

img = BMPFile()
img.parse( binFile );


### print header human-readable data ###
#print img.header.info()

### print file human-readable data ###
#print img.readableData

### print header human-readable data ###
#print img.header.readableData

### print content human-readable data ###
#print img.content.readableData


#print img.header.binData + img.content.binData

img.content.unparse( img.content.map )
img.header.unparse()


print img.header.binData + img.content.binData



#print img.hexData


#for line in img.content.map:
#	for pixel in line:
#		print "rgb(%s, %s, %s)" % (pixel.r, pixel.g, pixel.b)
#	print