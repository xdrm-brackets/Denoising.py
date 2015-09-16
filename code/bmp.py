# ~*~ encoding: utf-8 ~*~ #
###########################
#   TRAITEMENT D'IMAGES   #
###########################

# classes
from BMPFile import *
from Noise import *
import random
import sys
import time


class Timer:
	def __init__(self):
		self.timer = time.time();

	def reset(self):
		self.timer = time.time();

	def get(self):
		return float(int(100*(time.time()-self.timer)))/100



def testFileIntegrity():

	t = Timer();
	total = Timer(); total.reset();
	

	# lecture du fichier
	print "Reading Image         -",; t.reset();
	with open( sys.argv[1] ) as file:
		binFile = file.read()
	print "Done in %s s" % (t.get())


	img = BMPFile(); # Instanciation du BMPFile
	noise = Noise(); # Instanciation du NoiseObject


	# Parsing
	print "Parsing file          -",; t.reset();
	img.parse( binFile );
	print "Done in %s s" % (t.get())



	# print "Creating Salt&Pepper  -",; t.reset();
	# noise.SaltAndPepper_set(10, img.content.map)
	# print "Done in %s s" % (t.get())

	# # Unparsing
	# print "Unparsing file        -",; t.reset();
	# img.unparse(newBpp=24)
	# print "Done in %s s" % (t.get())

	# # image to stdout
	# print "Writing file          -",; t.reset();
	# img.write( "SaltAndPepper.bmp" )
	# print "Done in %s s" % (t.get())




	# print "Removing Salt&Pepper  -",; t.reset();
	# noise.SaltAndPepper_unset(img.content.map)
	# print "Done in %s s" % (t.get())

	# # Unparsing
	# print "Unparsing file        -",; t.reset();
	# img.unparse(newBpp=24)
	# print "Done in %s s" % (t.get())

	# # image to stdout
	# print "Writing file          -",; t.reset();
	# img.write( sys.argv[2] )
	# print "Done in %s s" % (t.get())




	print "Getting Shape         -",; t.reset();

	pixelList = [];

	try:
		noise.getShapeRecursive([0,0,0,0], img.content.map, pixelList);
	except RuntimeError as e:
		noise.getShapeRecursive([0,0,0,0], img.content.map, pixelList);



	print "Done in %s s" % (t.get())

	# Unparsing
	print "Unparsing file        -",; t.reset();
	img.unparse(newBpp=24)
	print "Done in %s s" % (t.get())

	# image to stdout
	print "Writing file          -",; t.reset();
	img.write( "shape.bmp" )
	print "Done in %s s" % (t.get())


















	print "\nExecution Time: %s seconds" % total.get()




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







if len(sys.argv) < 3:
	print "Require 2 args : \n* input image\n* output image"
	exit()






# MAIN
#testManualCreation()
testFileIntegrity()