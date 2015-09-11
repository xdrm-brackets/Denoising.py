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

	# Parsing
	img.parse( binFile );

	# détection des formes
	noise = Noise();

	pixelsDone = []
	for y in range(0,len(img.content.map)):
		for x in range(0, len(img.content.map[0])):
			# on traite si on a pas déjà
			already = False
			for i in pixelsDone:
				if i == img.content.map[y][x]:
					already = True
					break


			if not already:
				pixelList = []

				randomRGB = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

				noise.getShape([x, y, x, y], img.content.map, pixelList)

				for pixel in pixelList:
					pixel.setRGB(randomRGB[0], randomRGB[1], randomRGB[2]);

				pixelsDone = pixelsDone + pixelList;
			


	#inct = 50; # incertitude

	# MODIFICATIONS des pixels
	#for line in img.content.map:
	#	for pixel in line:
	#		pixel.setRGB(
	#			(230-25) + (2*25*pixel.r/256), # 230 ± 25
	#			(170-inct) + (2*inct*pixel.g/256), # 170 ± 50
	#			(100-inct) + (2*inct*pixel.b/256), # 100 ± 50
	#			bpp=24
	#		)


	# Unparsing
	img.unparse()


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