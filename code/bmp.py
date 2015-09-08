# ~*~ encoding: utf-8 ~*~ #
###########################
#   TRAITEMENT D'IMAGES   #
###########################

# classes
from classes import *

import sys

# lecture du fichier
with open( sys.argv[1] ) as file:
	binFile = file.read()

# Instanciation du BMPFile
img = BMPFile()

# Parsing
img.parse( binFile );


# MODIFICATIONS des pixels
for line in img.content.map:
	for pixel in line:
		pixel.r = 255
		pixel.g = 75
		pixel.b = 255


# Unparsing
img.unparse()


print img.binData

# for line in img.content.map:
# 	for pixel in line:
# 		print "rgb(%s, %s, %s)" % (pixel.r, pixel.g, pixel.b)
# 	print