# ~*~ encoding: utf-8 ~*~ #
###########################
#   TRAITEMENT D'IMAGES   #
###########################

# classes
from headerClass import *

import dep
import sys

fileData = ""
with open(sys.argv[1]) as f:
	for byte in f.read():
		fileData += byte

headerSize = 54

header = BMPHeader( fileData[0:headerSize] )
content = fileData[headerSize:]	

print header.offset
print
print content