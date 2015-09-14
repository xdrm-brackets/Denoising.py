# ~*~ encoding: utf-8 ~*~ #
###########################
#   TRAITEMENT D'IMAGES   #
###########################

# classes
from BMPFile import *
from Noise import *
import random
import sys











def testFileIntegrity():
	# lecture du fichier
	with open( sys.argv[1] ) as file:
		binFile = file.read()

	# Instanciation du BMPFile
	img = BMPFile()
	# Instanciation du NoiseObject
	noise = Noise();

	# Parsing
	img.parse( binFile );

	noise.SaltAndPepper_set(10, img.content.map)


	# Unparsing
	img.unparse(newBpp=24)

	print img.binData





def testManualCreation():
	img = BMPFile()
	for y in range(0, 100):
		img.content.map.append( [] )
		for x in range(0, 100):
			img.content.map[y].append( RGBPixel(
				random.randint(0, 255),
				random.randint(0, 255),
				random.randint(0, 255),
				bpp=24
			) );

	img.unparse();

	print img.binData

# MAIN
#testManualCreation()
testFileIntegrity()