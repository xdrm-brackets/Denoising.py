# ~*~ encoding: utf-8 ~*~ #
###########################
#   TRAITEMENT D'IMAGES   #
###########################

# classes
from classes import *

import sys

fileData = ""
with open(sys.argv[1]) as f:
	for byte in f.read():
		fileData += byte

headerSize = 54

header = BMPHeader(   fileData[:headerSize]    )
content = BMPContent( fileData[header.offset:], header )	

for line in content.map:
	for pixel in line:
		print "rgb(%s, %s, %s)" % (pixel.r, pixel.g, pixel.b)
	print	