# ~*~ encoding: utf-8 ~*~ #
###########################
#   TRAITEMENT D'IMAGES   #
###########################

# classes
from classes import *

import dep
import sys

fileData = ""
with open(sys.argv[1]) as f:
	for byte in f.read():
		fileData += byte

headerSize = 54

header = BMPHeader(   fileData[:headerSize]    )
content = BMPContent( fileData[header.offset:], header )	

print header.bpp
print
print content.map