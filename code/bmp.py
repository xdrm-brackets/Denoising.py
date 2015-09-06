# ~*~ encoding: utf-8 ~*~ #
###########################
#   TRAITEMENT D'IMAGES   #
###########################

import dep
import sys

tmp = ""
header = ""
content = ""


with open(sys.argv[1]) as f:
	for byte in f.read():
		tmp += str( hex( ord(byte) ) )[2:] + ","

headerSize = ( 2 + 4 + 2 + 2 + 4 + 4 + 4 + 4 + 2 + 2 + 4 + 4 + 4 + 4 + 4 + 4 )
header = tmp[:headerSize]
content = tmp[headerSize:]	

print header
print
print content