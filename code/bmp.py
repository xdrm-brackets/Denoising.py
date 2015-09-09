# ~*~ encoding: utf-8 ~*~ #
###########################
#   TRAITEMENT D'IMAGES   #
###########################

# classes
from BMPFile import *
import random
import sys


def testFileIntegrity():
	# lecture du fichier
	with open( sys.argv[1] ) as file:
		binFile = file.read()

	# Instanciation du BMPFile
	img = BMPFile()

	# Parsing
	img.parse( binFile );

	for line in img.content.map:
		for pixel in line:
			print "rgb(%s, %s, %s)" % (pixel.r, pixel.g, pixel.b)
		print

	# # MODIFICATIONS des pixels
	# for line in img.content.map:
	# 	for pixel in line:
	# 		pixel.r = 255
	# 		pixel.g = 75
	# 		pixel.b = 255


	# # Unparsing
	# img.unparse()


	# print img.binData





def testManualCreation():
	img = BMPFile()
	for y in range(0, 100):
		img.content.map.append( [] )
		for x in range(0, 1000):
			img.content.map[y].append( PixelColor(
				random.randint(0, 255),
				random.randint(0, 255),
				random.randint(0, 255)
			) );

	img.unparse();

	print img.binData

# MAIN
#testManualCreation()
testFileIntegrity()