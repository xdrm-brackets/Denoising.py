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


	# Parsing
	print "Parsing file          -",; t.reset();
	img.parse( binFile );
	print "Done in %s s" % (t.get())

	img.header.info();





	# Unparsing
	print "Unparsing file        -",; t.reset();
	img.unparse();
	print "Done in %s s" % (t.get())

	# Writing
	print "Writing file          -",; t.reset();
	img.write( sys.argv[2] )
	print "Done in %s s" % (t.get())

	# lecture du fichier
	print "Reading Image         -",; t.reset();
	with open( sys.argv[2] ) as file:
		binFile = file.read()
	print "Done in %s s" % (t.get())

	# Parsing
	print "Parsing file          -",; t.reset();
	img.parse( binFile );
	print "Done in %s s" % (t.get())

	img.header.info();





def testSaltAndPepper():

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



	print "Creating Salt&Pepper  -",; t.reset();
	noise.SaltAndPepper_set(50, img.content.map)
	print "Done in %s s" % (t.get())

	# Unparsing
	print "Unparsing file        -",; t.reset();
	img.unparse(newBpp=8)
	print "Done in %s s" % (t.get())

	# image to stdout
	print "Writing file          -",; t.reset();
	img.write( "SaltAndPepper.bmp" )
	print "Done in %s s" % (t.get())




	print "Removing Salt&Pepper  -",; t.reset();
	noise.SaltAndPepper_unset(img.content.map)
	print "Done in %s s" % (t.get())

	# Unparsing
	print "Unparsing file        -",; t.reset();
	img.unparse(newBpp=8)
	print "Done in %s s" % (t.get())

	# image to stdout
	print "Writing file          -",; t.reset();
	img.write( sys.argv[2] )
	print "Done in %s s" % (t.get())

	print "\nExecution Time: %s seconds" % total.get()





def printIntPalette():
	img = BMPFile();

	# lecture du fichier
	with open( sys.argv[1] ) as file:
		binFile = file.read()

	img.parse(binFile);

	print img.intPalette;




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







############ TESTS ############
#testManualCreation()
#testSaltAndPepper()
#testFileIntegrity()
#printIntPalette();



















def calSaltAndPepper():

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



	print "Creating Salt&Pepper  -",; t.reset();
	noise.SaltAndPepper_set(50, img.content.map)
	print "Done in %s s" % (t.get())

	# Unparsing
	print "Unparsing file        -",; t.reset();
	img.unparse(newBpp=8)
	print "Done in %s s" % (t.get())

	# image to stdout
	print "Writing file          -",; t.reset();
	img.write( "SaltAndPepper.bmp" )
	print "Done in %s s" % (t.get())




	print "Removing Salt&Pepper  -",; t.reset();
	noise.SaltAndPepper_unset(img.content.map)
	print "Done in %s s" % (t.get())

	# Unparsing
	print "Unparsing file        -",; t.reset();
	img.unparse(newBpp=8)
	print "Done in %s s" % (t.get())

	# image to stdout
	print "Writing file          -",; t.reset();
	img.write( sys.argv[2] )
	print "Done in %s s" % (t.get())

	print "\nExecution Time: %s seconds" % total.get()






############ CALIBRATE ############
calSaltAndPepper()