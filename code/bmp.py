# ~*~ encoding: utf-8 ~*~ #
###########################
#   TRAITEMENT D'IMAGES   #
###########################

# classes
from headerClass import *

import dep
import sys

tmp = ""
content = ""


with open(sys.argv[1]) as f:
	for byte in f.read():
		content += byte
		tmp += str( hex( ord(byte) ) )[2:] + ","

headerSize = 54

header = BMPHeader(content[0:headerSize])
content = tmp[headerSize:]	

print header.offset
print
print content