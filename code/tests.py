# ~*~ encoding: utf-8 ~*~ #
###########################
#   TRAITEMENT D'IMAGES   #
###########################

# classes
from BMPFile import *
from Noise import *
from tests import *

import random
import sys
import time





# Chronomètre de traitement
##############################
#
# Permet la calcul de durée des différentes tâches 
#
class Timer:
	# crée et remet à zéro le chrono
	def __init__(self): 
		self.timer = time.time();

	# remise à zéro du chrono
	def reset(self):
		self.timer = time.time();

	# affiche la valeur du chrono
	def get(self):
		return exactLength( str(float(int(100*(time.time()-self.timer)))/100), 7, 0 )



# retourne la chaine complétée d'espaces pour arriver à la taille length #
##########################################################################
# @param text			le texte de base
# @param length			la taille totale à renvoyer
# @param position		position du texte ( <0 = gauche ; 0 = centre ; >0 = droite )
#
# @exception			si le texte est plus grand que la position on renvoie le texte sans exception
def exactLength(text, length, position=0):
	# si texte aussi long ou plus long que la taille, on renvoie le text
	if len(text) >= length:
		return text;

	# initialisation de la variable qui sera retournée
	string = ""

	# texte à gauche
	if position < 0:
		return text + " "*(length-len(text))
	# texte à droite
	elif position > 0:
		return " "*(length-len(text)) + text
	# texte au centre
	else:
		return " "*( (length-len(text))//2 ) + text + " "*( length - (length-len(text))//2 - len(text) )
















# teste les fonctions PARSE et UNPARSE 
##########################################################
# @sysarg	1			l'image de base
# @sysarg	2			l'image de sortie
#
# @history
#				Parse l'image de base [affiche les infos du header]
#				Unparse à partir de la matrice de pixels récupérée dans l'image de sortie
#				Relis l'image crée pour vérifier que les infos sont identiques [affiche les infos du header]
#
def testFileIntegrity():

	t = Timer();
	

	# lecture du fichier
	print "Reading Image         -",; t.reset();
	with open( sys.argv[1] ) as file:
		binFile = file.read()
	print "%s |" % (t.get())


	img = BMPFile(); # Instanciation du BMPFile


	# Parsing
	print "Parsing file          -",; t.reset();
	img.parse( binFile );
	print "%s |" % (t.get())

	img.header.info();





	# Unparsing
	print "Unparsing file        -",; t.reset();
	img.unparse();
	print "%s |" % (t.get())

	# Writing
	print "Writing file          -",; t.reset();
	img.write( sys.argv[2] )
	print "%s |" % (t.get())

	# lecture du fichier
	print "Reading Image         -",; t.reset();
	with open( sys.argv[2] ) as file:
		binFile = file.read()
	print "%s |" % (t.get())

	# Parsing
	print "Parsing file          -",; t.reset();
	img.parse( binFile );
	print "%s |" % (t.get())

	img.header.info();






# teste les fonction de bruitage et débruitage de type "Poivre et Sel" #
########################################################################
# @sysarg		1		le fichier d'origine
# @stsarg		2		le fichier de sortie (bruité PUIS débruité)
#
# @file 		SaltAndPepper.bmp 		le fichier bruité
#
# @history
#			Parse le fichier d'origine
#			Bruite l'image' et l'enregistre dans "SaltAndPepper.bmp"
#			Débruite l'image et l'enregistre dans le fichier de sortie
def testSaltAndPepper():

	t = Timer();
	

	# lecture du fichier
	print "| Reading Image           |",; t.reset();
	with open( sys.argv[1] ) as file:
		binFile = file.read()
	print "%s |" % (t.get())


	img = BMPFile(); # Instanciation du BMPFile
	noise = Noise(); # Instanciation du NoiseObject


	# Parsing
	print "| Parsing file            |",; t.reset();
	img.parse( binFile );
	print "%s |" % (t.get())



	print "| Creating Salt&Pepper    |",; t.reset();
	noise.SaltAndPepper_set(img.content.map, seuil=50)
	print "%s |" % (t.get())

	# Unparsing
	print "| Unparsing file          |",; t.reset();
	img.unparse()
	print "%s |" % (t.get())

	# image to stdout
	print "| Writing file            |",; t.reset();
	img.write( "SaltAndPepper.bmp" )
	print "%s |" % (t.get())




	print "| Removing Salt&Pepper    |",; t.reset();
	noise.SaltAndPepper_unset(img.content.map, seuil=1, borne=1)
	print "%s |" % (t.get())

	# Unparsing
	print "| Unparsing file          |",; t.reset();
	img.unparse()
	print "%s |" % (t.get())

	# image to stdout
	print "| Writing file            |",; t.reset();
	img.write( sys.argv[2] )
	print "%s |" % (t.get())

	







# teste les fonction de bruitage et débruitage de type "Additif" #
########################################################################
# @sysarg		1		le fichier d'origine
# @stsarg		2		le fichier de sortie (bruité PUIS débruité)
#
# @file 		SaltAndPepper.bmp 		le fichier bruité
#
# @history
#			Parse le fichier d'origine
#			Bruite l'image' et l'enregistre dans "AdditiveNoise.bmp"
#			Débruite l'image et l'enregistre dans le fichier de sortie
def testAdditiveNoise():

	t = Timer();
	

	# lecture du fichier
	print "| Reading Image           |",; t.reset();
	with open( sys.argv[1] ) as file:
		binFile = file.read()
	print "%s |" % (t.get())


	img = BMPFile(); # Instanciation du BMPFile
	noise = Noise(); # Instanciation du NoiseObject


	# Parsing
	print "| Parsing file            |",; t.reset();
	img.parse( binFile );
	print "%s |" % (t.get())



	print "| Creating Additive       |",; t.reset();
	noise.AdditiveNoise_set(img.content.map, seuil=50)
	print "%s |" % (t.get())

	# Unparsing
	print "| Unparsing file          |",; t.reset();
	img.unparse()
	print "%s |" % (t.get())

	# image to stdout
	print "| Writing file            |",; t.reset();
	img.write( "AdditiveNoise.bmp" )
	print "%s |" % (t.get())




	print "| Removing Additive       |",; t.reset();
	noise.AdditiveNoise_unset(img.content.map)
	print "%s |" % (t.get())

	# Unparsing
	print "| Unparsing file          |",; t.reset();
	img.unparse()
	print "%s |" % (t.get())

	# image to stdout
	print "| Writing file            |",; t.reset();
	img.write( sys.argv[2] )
	print "%s |" % (t.get())

	











# teste la création d'image manuelle (UNPARSE) à partir d'une matrice uniquement #
##################################################################################
# @sysarg		1		le fichier de sortie
# @stsarg		2		/
#
# @history
#			Unparse une matrice de pixels aléatoire de taille 100x100
#			L'enregistre dans le fichier de sortie
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

	img.write( sys.argv[2] )
	# print img.binData




# Affiche la palette afin de savoir si elle est connue ou nouvelle #
####################################################################
# @sysarg		1		le fichier d'entrée
# @stsarg		2		/
#
# @history
#			Affiche la palette au format <int>[] 
def printIntPalette():
	img = BMPFile();

	# lecture du fichier
	with open( sys.argv[1] ) as file:
		binFile = file.read()

	img.parse(binFile);

	print img.intPalette;















# Affiche un pourcentage de différence entre 2 images #
#######################################################
# @sysarg		1		le fichier A
# @stsarg		2		le fichier B
#
# @history
#			Parse A et B
#			Compare A et B
#			Affiche le pourcentage de ressemblance/différence
def printImageQuality():
	t = Timer();
	imageFile, modelFile = "", ""


	# lecture des fichiers
	print "| Reading files           |",; t.reset();
	with open( sys.argv[1] ) as f:
		imageFile = f.read();
	with open( sys.argv[2] ) as f:
		modelFile = f.read();
	print "%s |" % (t.get())

	# parsage
	print "| Parsing images          |",; t.reset();
	image = BMPFile(); image.parse( imageFile );
	model = BMPFile(); model.parse( modelFile );
	print "%s |" % (t.get())

	# condition
	imagePixelCount = image.header.width * image.header.height
	modelPixelCount = model.header.width * model.header.height 
	
	if imagePixelCount != modelPixelCount:
		print "*** Taille de matrices différentes"
		exit()


	# comparaison
	print "| Comparaison             |",; t.reset();
	count, totalCount = [0,0,0], imagePixelCount*256*3
	for y in range(0, image.header.height):
		for x in range(0, image.header.width):
			count[0] += abs( image.content.map[y][x].r - model.content.map[y][x].r )
			count[1] += abs( image.content.map[y][x].g - model.content.map[y][x].g )
			count[2] += abs( image.content.map[y][x].b - model.content.map[y][x].b )

	differenceCount = count[0] + count[1] + count[2]
	percentage = 100.0 * (totalCount-differenceCount) / totalCount
	percentage = int(100*percentage)/100.0
	print "%s |" % (t.get())
	print "+-------------------------+"
	print "| Commun     = %s |" % exactLength( str(percentage)+"%",     10, -1 );
	print "| Difference = %s |" % exactLength( str(100-percentage)+"%", 10, -1 );




# Créé une image contenant la différence entre 2 images existantes #
####################################################################
# @sysarg		1		le fichier A
# @stsarg		2		le fichier B
#
# @file 		compare.bmp 		le fichier bruité
#
# @history
#			Parse A et B
#			Créer une matrice de pixels
#			Unparse cette matrice et l'enregistre dans le fichier "compare.bmp"
def imageForImageQuality():
	t = Timer();
	imageFile, modelFile = "", ""
	image, model, newImg = BMPFile(), BMPFile(), BMPFile()


	# lecture des fichiers
	print "Reading files        -",; t.reset();
	with open( sys.argv[1] ) as f:
		imageFile = f.read();
	with open( sys.argv[2] ) as f:
		modelFile = f.read();
	print "%s |" % (t.get())

	# parsage
	print "Parsing images       -",; t.reset();
	image.parse( imageFile );
	model.parse( modelFile );
	print "%s |" % (t.get())

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
	print "%s |" % (t.get())

	print "Writing File         -",; t.reset();
	with open("compare.bmp", "w") as f:
		f.write( newImg.binData );
	print "%s |" % (t.get())

 
	






# Fusionne 2 images (addition uniquement) #
###########################################
# @sysarg		1		le fichier A
# @stsarg		2		le fichier B
#
# @file 		merge.bmp 		le fichier bruité
#
# @history
#			Parse les fichiers A et B
#			Créer la matrice de pixels à partir de l'addition de A et B
#			Unparse le tout et l'enregistre dans merge.bmp
def mergeImages():
	t = Timer();
	imageFile, modelFile = "", ""
	image, model, newImg = BMPFile(), BMPFile(), BMPFile()


	# lecture des fichiers
	print "Reading files        -",; t.reset();
	with open( sys.argv[1] ) as f:
		imageFile = f.read();
	with open( sys.argv[2] ) as f:
		modelFile = f.read();
	print "%s |" % (t.get())

	# parsage
	print "Parsing images       -",; t.reset();
	image.parse( imageFile );
	model.parse( modelFile );
	print "%s |" % (t.get())

	
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

	print "%s |" % (t.get())
	
	print "Unparsing            -",; t.reset();
	newImg.unparse(newBpp=24);
	print "%s |" % (t.get())

	print "Writing File         -",; t.reset();
	with open("merge.bmp", "w") as f:
		f.write( newImg.binData );
	print "%s |" % (t.get())

 
	




















# dure environ 4min 13s
def calSaltAndPepper():

	t = Timer();
	

	# lecture du fichier
	print "Reading Image         -",; t.reset();
	with open( sys.argv[1] ) as file:
		binFile = file.read()
	print "%s |" % (t.get())


	img = BMPFile(); # Instanciation du BMPFile
	noise = Noise(); # Instanciation du NoiseObject


	for seuil in range(0,100,10):
		for borne in range(0,30,10):

			img.parse( binFile );

			print "SaltAndPepper (%s) (%s) -" % (seuil, borne),; t.reset();
			noise.SaltAndPepper_unset(img.content.map, seuil=seuil, borne=borne)
			img.unparse(newBpp=8)
			img.write( "SaltAndPepper/%s_%s.bmp" % (seuil, borne) )
			print "%s |" % (t.get())


	





