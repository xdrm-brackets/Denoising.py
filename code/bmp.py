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
	noise.SaltAndPepper_set(img.content.map, seuil=10)
	print "Done in %s s" % (t.get())

	# Unparsing
	print "Unparsing file        -",; t.reset();
	img.unparse()
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
	img.unparse()
	print "Done in %s s" % (t.get())

	# image to stdout
	print "Writing file          -",; t.reset();
	img.write( sys.argv[2] )
	print "Done in %s s" % (t.get())

	print "\nExecution Time: %s seconds" % total.get()








def testAdditiveNoise():

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



	print "Creating Additive     -",; t.reset();
	noise.AdditiveNoise_set(img.content.map, seuil=50)
	print "Done in %s s" % (t.get())

	# Unparsing
	print "Unparsing file        -",; t.reset();
	img.unparse()
	print "Done in %s s" % (t.get())

	# image to stdout
	print "Writing file          -",; t.reset();
	img.write( "AdditiveNoise.bmp" )
	print "Done in %s s" % (t.get())




	print "Removing Additive     -",; t.reset();
	noise.AdditiveNoise_unset(img.content.map)
	print "Done in %s s" % (t.get())

	# Unparsing
	print "Unparsing file        -",; t.reset();
	img.unparse()
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



def printImageQuality():
	t = Timer();
	total = Timer(); total.reset();
	imageFile, modelFile = "", ""


	# lecture des fichiers
	print "Reading files        -",; t.reset();
	with open( sys.argv[1] ) as f:
		imageFile = f.read();
	with open( sys.argv[2] ) as f:
		modelFile = f.read();
	print "Done in %s s" % (t.get())

	# parsage
	print "Parsing images       -",; t.reset();
	image = BMPFile(); image.parse( imageFile );
	model = BMPFile(); model.parse( modelFile );
	print "Done in %s s" % (t.get())

	# condition
	imagePixelCount = image.header.width * image.header.height
	modelPixelCount = model.header.width * model.header.height 
	
	if imagePixelCount != modelPixelCount:
		print "*** Taille de matrices différentes"
		exit()


	# comparaison
	print "Comparaison          -",; t.reset();
	count, totalCount = [0,0,0], imagePixelCount*256*3
	for y in range(0, image.header.height):
		for x in range(0, image.header.width):
			count[0] += abs( image.content.map[y][x].r - model.content.map[y][x].r )
			count[1] += abs( image.content.map[y][x].g - model.content.map[y][x].g )
			count[2] += abs( image.content.map[y][x].b - model.content.map[y][x].b )

	differenceCount = count[0] + count[1] + count[2]
	percentage = 100.0 * (totalCount-differenceCount) / totalCount
	percentage = int(100*percentage)/100.0
	print "Done in %s s" % (t.get())
	print
	print "Qualité    = %s %s" % (percentage, "%")
	print "Différence = %s %s" % (100-percentage, "%")
 
	print "\nExecution Time: %s seconds" % total.get()



def imageForImageQuality():
	t = Timer();
	total = Timer(); total.reset();
	imageFile, modelFile = "", ""
	image, model, newImg = BMPFile(), BMPFile(), BMPFile()


	# lecture des fichiers
	print "Reading files        -",; t.reset();
	with open( sys.argv[1] ) as f:
		imageFile = f.read();
	with open( sys.argv[2] ) as f:
		modelFile = f.read();
	print "Done in %s s" % (t.get())

	# parsage
	print "Parsing images       -",; t.reset();
	image.parse( imageFile );
	model.parse( modelFile );
	print "Done in %s s" % (t.get())

	# condition
	imagePixelCount = image.header.width * image.header.height
	modelPixelCount = model.header.width * model.header.height 
	
	if imagePixelCount != modelPixelCount:
		print "*** Taille de images différentes"
		exit()


	# comparaison
	print "Comparaison          -",; t.reset();
	count, totalCount = [0,0,0], imagePixelCount*256*3
	for y in range(0, image.header.height):
		newImg.content.map.append( [] );
		for x in range(0, image.header.width):
			newImg.content.map[y].append( RGBPixel(
				255 - abs( image.content.map[y][x].r - model.content.map[y][x].r ),
				255 - abs( image.content.map[y][x].g - model.content.map[y][x].g ),
				255 - abs( image.content.map[y][x].b - model.content.map[y][x].b )
			) )

	
	print "Unparsing            -",; t.reset();
	newImg.unparse();
	print "Done in %s s" % (t.get())

	print "Writing File         -",; t.reset();
	with open("compare.bmp", "w") as f:
		f.write( newImg.binData );
	print "Done in %s s" % (t.get())

 
	print "\nExecution Time: %s seconds" % total.get()







def mergeImages():
	t = Timer();
	total = Timer(); total.reset();
	imageFile, modelFile = "", ""
	image, model, newImg = BMPFile(), BMPFile(), BMPFile()


	# lecture des fichiers
	print "Reading files        -",; t.reset();
	with open( sys.argv[1] ) as f:
		imageFile = f.read();
	with open( sys.argv[2] ) as f:
		modelFile = f.read();
	print "Done in %s s" % (t.get())

	# parsage
	print "Parsing images       -",; t.reset();
	image.parse( imageFile );
	model.parse( modelFile );
	print "Done in %s s" % (t.get())

	
	# condition
	imagePixelCount = image.header.width * image.header.height
	modelPixelCount = model.header.width * model.header.height 

	if imagePixelCount != modelPixelCount:
		print "*** Taille de images différentes"
		exit()


	# comparaison
	print "Merging              -",; t.reset();
	for y in range(0, image.header.height):
		newImg.content.map.append( [] );
		for x in range(0, image.header.width):
			newImg.content.map[y].append( RGBPixel(
				( image.content.map[y][x].r + model.content.map[y][x].r ) % 256,
				( image.content.map[y][x].g + model.content.map[y][x].g ) % 256,
				( image.content.map[y][x].b + model.content.map[y][x].b ) % 256
			) )

	print "Done in %s s" % (t.get())
	
	print "Unparsing            -",; t.reset();
	newImg.unparse(newBpp=24);
	print "Done in %s s" % (t.get())

	print "Writing File         -",; t.reset();
	with open("merge.bmp", "w") as f:
		f.write( newImg.binData );
	print "Done in %s s" % (t.get())

 
	print "\nExecution Time: %s seconds" % total.get()


############ TESTS ############
# testManualCreation()
testSaltAndPepper()
# testAdditiveNoise()
# testFileIntegrity()
# printIntPalette()
printImageQuality()

# imageForImageQuality()
# mergeImages()

















# dure environ 4min 13s
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


	for seuil in range(0,100,10):
		for borne in range(0,30,10):

			img.parse( binFile );

			print "SaltAndPepper (%s) (%s) -" % (seuil, borne),; t.reset();
			noise.SaltAndPepper_unset(img.content.map, seuil=seuil, borne=borne)
			img.unparse(newBpp=8)
			img.write( "SaltAndPepper/%s_%s.bmp" % (seuil, borne) )
			print "Done in %s s" % (t.get())


	print "\nExecution Time: %s seconds" % total.get()






############ CALIBRATE ############
#calSaltAndPepper()