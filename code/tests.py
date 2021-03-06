# ~*~ encoding: utf-8 ~*~ #
###########################
#   TRAITEMENT D'IMAGES   #
###########################

# classes
from BMPFile import *
from Noise import *
from tests import *
from utility import Drawer

import random
import os
import sys
import time
from math import log


# GLOBAL INSTANCE
FX = Noise();



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








def defaultTest(img):
	t = Timer();
	

	# lecture du fichier
	# print "| Reading Image             |",; t.reset();
	# with open( sys.argv[1] ) as file:
	# 	binFile = file.read()
	# print "%s |" % (t.get())


	# img = BMPFile(); # Instanciation du BMPFile


	# # Parsing
	# print "| Parsing file              |",; t.reset();
	# img.parse( binFile );
	# print "%s |" % (t.get())



	print "| Test par défaut           |",; t.reset();
	img.content.map = FX.Filter.Test(img.content.map)
	print "%s |" % (t.get())

	# Unparsing
	# print "| Unparsing file            |",; t.reset();
	# img.unparse()
	# print "%s |" % (t.get())

	# # image to stdout
	# print "| Writing file              |",; t.reset();
	# img.write( sys.argv[2] )
	# print "%s |" % (t.get())







# teste la création d'image manuelle (UNPARSE) à partir d'une matrice uniquement #
##################################################################################
# @sysarg		1		le fichier de sortie
# @stsarg		2		/
#
# @history
#			Unparse une matrice de pixels aléatoire de taille 100x100
#			L'enregistre dans le fichier de sortie
def testManualCreation(img, width=100, height=100):

	t = Timer();

	print "| Creating Image            |",; t.reset();
	img.content.map = [];
	img.drawer.setSize(width, height);
	for y in range(0, height):
		img.content.map.append( [] )
		for x in range(0, width):
			img.content.map[y].append( RGBPixel(
				r=random.randint(0, 255),
				g=random.randint(0, 255),
				b=random.randint(0, 255),
				x=x,
				y=y,
				bpp=24
			) );

			img.drawer.setPixel( img.content.map[y][x] );

	# img.unparse();
	print "%s |" % (t.get())


	# print "| Writing Image             |",; t.reset();
	# img.write( sys.argv[2] )
	# print "%s |" % (t.get())





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
def testFileIntegrity(img):

	t = Timer();
	returnValue = ""

	# lecture du fichier
	# print "| Reading Image             |",; t.reset();
	# with open( sys.argv[1] ) as file:
	# 	binFile = file.read()
	# print "%s |" % (t.get())


	# A = BMPFile(); # Instanciation du BMPFile

	# Parsing
	# print "| Parsing file              |",; t.reset();
	# A.parse( binFile );
	# print "%s |" % (t.get())

	returnValue += img.header.info();

	# Unparsing
	print "| Unparsing file            |",; t.reset();
	img.unparse();
	print "%s |" % (t.get())

	# Writing
	print "| Writing file              |",; t.reset();
	img.write( "parseUnparseTest.bmp" )
	print "%s |" % (t.get())


	B = BMPFile()

	# lecture du fichier
	print "| Reading Image             |",; t.reset();
	with open( "parseUnparseTest.bmp" ) as file:
		binFile = file.read()
	print "%s |" % (t.get())

	os.remove("parseUnparseTest.bmp"); # suppression de l'image

	# Parsing
	print "| Parsing file              |",; t.reset();
	B.parse( binFile );
	print "%s |" % (t.get())

	img.drawer.fill( img.content.map );

	returnValue += "\n\n\n" + B.header.info();

	return returnValue;






# Affiche la palette afin de savoir si elle est connue ou nouvelle #
####################################################################
# @sysarg		1		le fichier d'entrée
# @stsarg		2		/
#
# @history
#			Affiche la palette au format <int>[] 
def printIntPalette(img):
	# img = BMPFile();

	t = Timer();
	
	# print "| Reading Image             |",; t.reset();
	# with open( sys.argv[1] ) as file:
	# 	binFile = file.read()
	# print "%s |" % (t.get())


	# print "| Parsing File              |",; t.reset();
	# img.parse(binFile);
	# print "%s |" % (t.get())

	return img.intPalette;










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
def testSaltAndPepper(img, seuilSet=50, seuilUnset=1, borneUnset=1, smooth=1):

	t = Timer();
	

	# lecture du fichier
	# print "| Reading Image             |",; t.reset();
	# with open( sys.argv[1] ) as file:
	# 	binFile = file.read()
	# print "%s |" % (t.get())


	# img = BMPFile(); # Instanciation du BMPFile


	# # Parsing
	# print "| Parsing file              |",; t.reset();
	# img.parse( binFile );
	# print "%s |" % (t.get())



	print "| Creating Salt&Pepper      |",; t.reset();
	FX.SaltAndPepper.set(img.drawer, img.content.map, seuil=seuilSet)
	print "%s |" % (t.get())

	# Unparsing
	# print "| Unparsing file            |",; t.reset();
	# img.unparse()
	# print "%s |" % (t.get())

	# # image to stdout
	# print "| Writing file              |",; t.reset();
	# img.write( "SaltAndPepper.bmp" )
	# print "%s |" % (t.get())




	print "| Removing Salt&Pepper      |",; t.reset();
	FX.SaltAndPepper.unset(img.drawer, img.content.map, seuil=seuilUnset, borne=borneUnset)
	print "%s |" % (t.get())

	if smooth != 0:
		print "| Filtre moyen              |",; t.reset();
		img.content.map = FX.Filter.averageFilter(img.drawer, img.content.map);
		print "%s |" % (t.get())

	# Unparsing
	# print "| Unparsing file            |",; t.reset();
	# img.unparse()
	# print "%s |" % (t.get())

	# # image to stdout
	# print "| Writing file              |",; t.reset();
	# img.write( sys.argv[2] )
	# print "%s |" % (t.get())

	







# teste les fonction de bruitage et débruitage de type "Additif de Bernouilli" #
################################################################################
# @sysarg		1		le fichier d'origine
# @stsarg		2		le fichier de sortie (bruité PUIS débruité)
#
# @file 		AdditiveNoise.bmp 		le fichier bruité
#
# @history
#			Parse le fichier d'origine
#			Bruite l'image' et l'enregistre dans "AdditiveNoise.bmp"
#			Débruite l'image et l'enregistre dans le fichier de sortie
def testAdditiveBernouilliNoise(img, seuilA=10, seuilB=5):

	t = Timer();
	

	# lecture du fichier
	# print "| Reading Image             |",; t.reset();
	# with open( sys.argv[1] ) as file:
	# 	binFile = file.read()
	# print "%s |" % (t.get())


	# img = BMPFile(); # Instanciation du BMPFile


	# # Parsing
	# print "| Parsing file              |",; t.reset();
	# img.parse( binFile );
	# print "%s |" % (t.get())



	print "| Creating Additive         |",; t.reset();
	FX.Additive.setBernouilli(img.drawer, img.content.map, seuil=seuilA)
	print "%s |" % (t.get())

	# Unparsing
	# print "| Unparsing file            |",; t.reset();
	# img.unparse()
	# print "%s |" % (t.get())

	# # image to stdout
	# print "| Writing file              |",; t.reset();
	# img.write( "AdditiveBernouilli.bmp" )
	# print "%s |" % (t.get())




	print "| Removing Additive         |",; t.reset();
	# img.content.map = FX.Additive.unset(img.drawer, img.content.map, seuil=seuilB)
	img.content.map = FX.Additive.unset2(img.drawer, img.content.map, seuil=seuilB)
	print "%s |" % (t.get())

	# Unparsing
	# print "| Unparsing file            |",; t.reset();
	# img.unparse()
	# print "%s |" % (t.get())

	# # image to stdout
	# print "| Writing file              |",; t.reset();
	# img.write( sys.argv[2] )
	# print "%s |" % (t.get())

	









# teste les fonction de bruitage et débruitage de type "Additif Gaussien" #
###########################################################################
# @sysarg		1		le fichier d'origine
# @stsarg		2		le fichier de sortie (bruité PUIS débruité)
#
# @file 		AdditiveNoise.bmp 		le fichier bruité
#
# @history
#			Parse le fichier d'origine
#			Bruite l'image' et l'enregistre dans "AdditiveNoise.bmp"
#			Débruite l'image et l'enregistre dans le fichier de sortie
def testAdditiveGaussianNoise(img, sigma=10, seuil=1):

	t = Timer();
	

	# lecture du fichier
	# print "| Reading Image             |",; t.reset();
	# with open( sys.argv[1] ) as file:
	# 	binFile = file.read()
	# print "%s |" % (t.get())


	# img = BMPFile(); # Instanciation du BMPFile


	# # Parsing
	# print "| Parsing file              |",; t.reset();
	# img.parse( binFile );
	# print "%s |" % (t.get())



	print "| Creating Additive         |",; t.reset();
	FX.Additive.setGaussian(img.drawer, img.content.map, sigma=sigma)
	print "%s |" % (t.get())

	# Unparsing
	# print "| Unparsing file            |",; t.reset();
	# img.unparse()
	# print "%s |" % (t.get())

	# # image to stdout
	# print "| Writing file              |",; t.reset();
	# img.write( "AdditiveGaussian.bmp" )
	# print "%s |" % (t.get())




	print "| Removing Additive         |",; t.reset();
	img.content.map = FX.Additive.unset2(img.drawer, img.content.map, seuil=seuil)
	print "%s |" % (t.get())

	# Unparsing
	# print "| Unparsing file            |",; t.reset();
	# img.unparse()
	# print "%s |" % (t.get())

	# # image to stdout
	# print "| Writing file              |",; t.reset();
	# img.write( sys.argv[2] )
	# print "%s |" % (t.get())

	

















# Affiche un pourcentage de différence entre 2 images #
#######################################################
# @sysarg		1		le fichier A
# @stsarg		2		le fichier B
#
# @history
#			Parse A et B
#			Compare A et B
#			Affiche le pourcentage de ressemblance/différence
def printImageQuality(image, model):
	t = Timer();
	# imageFile, modelFile = "", ""


	# lecture des fichiers
	# print "| Reading files             |",; t.reset();
	# with open( sys.argv[1] ) as f:
	# 	imageFile = f.read();
	# with open( sys.argv[2] ) as f:
	# 	modelFile = f.read();
	# print "%s |" % (t.get())

	# # parsage
	# print "| Parsing images            |",; t.reset();
	# image = BMPFile(); image.parse( imageFile );
	# model = BMPFile(); model.parse( modelFile );
	# print "%s |" % (t.get())

	# condition
	imagePixelCount = image.header.width * image.header.height
	modelPixelCount = model.header.width * model.header.height 
	
	if imagePixelCount != modelPixelCount:
		print "*** Taille de matrices différentes"
		exit()


	# comparaison
	print "| Comparaison               |",; t.reset();
	count, totalCount = [0,0,0], imagePixelCount*256*3
	for y in range(0, image.header.height):
		for x in range(0, image.header.width):
			count[0] += abs( image.content.map[y][x].r - model.content.map[y][x].r )
			count[1] += abs( image.content.map[y][x].g - model.content.map[y][x].g )
			count[2] += abs( image.content.map[y][x].b - model.content.map[y][x].b )

	differenceCount = count[0] + count[1] + count[2]
	percentage = 100.0 * (totalCount-differenceCount) / totalCount
	percentage = float(100.0*percentage)/100.0
	print "%s |" % (t.get())
	print "+---------------------------+---------+"
	print "| Commun     = %s |" % exactLength( str(percentage)+" %",     22, -1 );
	print "| Difference = %s |" % exactLength( str(100-percentage)+" %", 22, -1 );




# Affiche le SNR entre 2 images (1:origine, 2:bruitée) #
########################################################
# @sysarg		1		le fichier A - image d'origine
# @stsarg		2		le fichier B - image bruitée
#
# @history
#			Parse A et B
#			Calcule le SNR de A et B
#			Affiche le pourcentage de ressemblance/différence
def printSNR(image, model):
	t = Timer();
	# imageFile, modelFile = "", ""


	# # lecture des fichiers
	# print "| Reading files             |",; t.reset();
	# with open( sys.argv[1] ) as f:
	# 	modelFile = f.read();
	# with open( sys.argv[2] ) as f:
	# 	imageFile = f.read();
	# print "%s |" % (t.get())

	# # parsage
	# print "| Parsing images            |",; t.reset();
	# model = BMPFile(); model.parse( modelFile );
	# image = BMPFile(); image.parse( imageFile );
	# print "%s |" % (t.get())

	# condition
	modelPixelCount = model.header.width * model.header.height 
	imagePixelCount = image.header.width * image.header.height
	
	if imagePixelCount != modelPixelCount:
		print "*** Taille de matrices différentes"
		exit()


	# comparaison
	print "| Comparaison               |",; t.reset();
	SNR = FX.SNR(model.content.map, image.content.map)
	SNR2 = 10.0 * log(SNR, 10) if SNR!=0 else 0
	print "%s |" % (t.get())
	

	print "+---------------------------+---------+"
	print "| SNR        = %s |" % exactLength( str(SNR),     22, -1 );
	if SNR2 == 0:
		print "| SNR        = %s |" % exactLength( "100 %",     22, -1 );
	else:
		print "| SNR        = %s |" % exactLength( str(SNR2)+" dB",     22, -1 );








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
def imageForImageQuality(image, model):
	t = Timer();
	# imageFile, modelFile = "", ""
	# image, model = BMPFile(), BMPFile()
	newImg = BMPFile()


	# # lecture des fichiers
	# print "| Reading files             |",; t.reset();
	# with open( sys.argv[1] ) as f:
	# 	imageFile = f.read();
	# with open( sys.argv[2] ) as f:
	# 	modelFile = f.read();
	# print "%s |" % (t.get())

	# # parsage
	# print "| Parsing images            |",; t.reset();
	# image.parse( imageFile );
	# model.parse( modelFile );
	# print "%s |" % (t.get())

	# condition
	imagePixelCount = image.header.width * image.header.height
	modelPixelCount = model.header.width * model.header.height 
	
	if imagePixelCount != modelPixelCount:
		print "*** Taille de images différentes"
		exit()


	# comparaison
	print "| Comparaison               |",; t.reset();
	count, totalCount = [0,0,0], imagePixelCount*256*3
	for y in range(0, image.header.height):
		newImg.content.map.append( [] );
		for x in range(0, image.header.width):
			newImg.content.map[y].append( RGBPixel(
				255 - abs( image.content.map[y][x].r - model.content.map[y][x].r ),
				255 - abs( image.content.map[y][x].g - model.content.map[y][x].g ),
				255 - abs( image.content.map[y][x].b - model.content.map[y][x].b )
			) )
	print "%s |" % (t.get())

	image.drawer.fill( newImg.content.map );
	
	# print "| Unparsing                 |",; t.reset();
	# newImg.unparse();
	# print "%s |" % (t.get())

	# print "| Writing File              |",; t.reset();
	# with open("compare.bmp", "w") as f:
	# 	f.write( newImg.binData );
	# print "%s |" % (t.get())

 
	






# Fusionne 2 images (addition uniquement) #
###########################################
# @sysarg		1		le fichier A
# @stsarg		2		le fichier B
#
# @file 		merge.bmp 		le fichier résultant
#
# @history
#			Parse les fichiers A et B
#			Créer la matrice de pixels à partir de l'addition de A et B
#			Unparse le tout et l'enregistre dans mergeAdd.bmp
def mergeImagesAdditive(A, B):
	t = Timer();
	# imageFile, modelFile = "", ""
	# A, B = BMPFile(), BMPFile()
	newImg = BMPFile()

	# lecture des fichiers
	# print "| Reading files             |",; t.reset();
	# with open( sys.argv[1] ) as f:
	# 	AFile = f.read();
	# with open( sys.argv[2] ) as f:
	# 	BFile = f.read();
	# print "%s |" % (t.get())

	# # parsage
	# print "| Parsing images            |",; t.reset();
	# A.parse( AFile );
	# B.parse( BFile );
	# print "%s |" % (t.get())

	
	# condition
	APixelCount = A.header.width * A.header.height
	BPixelCount = B.header.width * B.header.height 

	if APixelCount != BPixelCount:
		print "*** Taille de images différentes"
		exit()


	# comparaison
	print "| Merging                   |",; t.reset();
	newImg.content.map = []
	for lineA, lineB in zip(A.content.map, B.content.map):
		newImg.content.map.append( [] );
		for aPix, bPix in zip(lineA, lineB):
			newImg.content.map[aPix.y].append( RGBPixel(
				r   = ( aPix.r + bPix.r ) / 2, # moyenne du rouge
				g   = ( aPix.g + bPix.g ) / 2, # moyenne du vert
				b   = ( aPix.b + bPix.b ) / 2, # moyenne du bleu
				x   = aPix.x,
				y   = aPix.y,
				bpp = aPix.bpp
			) )
			A.drawer.setPixel( newImg.content.map[aPix.y][aPix.x] );

	print "%s |" % (t.get())

	# print "| Unparsing                 |",; t.reset();
	# newImg.unparse(newBpp=24);
	# print "%s |" % (t.get())

	# print "| Writing File              |",; t.reset();
	# with open("mergeAdd.bmp", "w") as f:
	# 	f.write( newImg.binData );
	# print "%s |" % (t.get())

 
	






# Fusionne 2 images (soustraction uniquement) #
###############################################
# @sysarg		1		le fichier A
# @stsarg		2		le fichier B
#
# @file 		mergeSub.bmp 		le fichier résultant
#
# @history
#			Parse les fichiers A et B
#			Créer la matrice de pixels à partir de l'addition de A et B
#			Unparse le tout et l'enregistre dans mergeSub.bmp
def mergeImagesSubstractive(A, B):
	t = Timer();
	# imageFile, modelFile = "", ""
	# A, B = BMPFile(), BMPFile()
	newImg = BMPFile()

	# lecture des fichiers
	# print "| Reading files             |",; t.reset();
	# with open( sys.argv[1] ) as f:
	# 	AFile = f.read();
	# with open( sys.argv[2] ) as f:
	# 	BFile = f.read();
	# print "%s |" % (t.get())

	# # parsage
	# print "| Parsing images            |",; t.reset();
	# A.parse( AFile );
	# B.parse( BFile );
	# print "%s |" % (t.get())

	
	# condition
	APixelCount = A.header.width * A.header.height
	BPixelCount = B.header.width * B.header.height 

	if len(A.content.map) != len(B.content.map) or len(A.content.map[0]) != len(B.content.map[0]):
		print "*** Taille de images différentes"
		exit()


	# comparaison
	print "| Merging                   |",; t.reset();
	newImg.content.map = [];
	for lineA, lineB in zip(A.content.map, B.content.map):
		newImg.content.map.append( [] );
		for aPix, bPix in zip(lineA, lineB):
			newImg.content.map[aPix.y].append( RGBPixel(
				r   = ( aPix.r - bPix.r ) % 256, # moyenne du rouge
				g   = ( aPix.g - bPix.g ) % 256, # moyenne du vert
				b   = ( aPix.b - bPix.b ) % 256, # moyenne du bleu
				x   = aPix.x,
				y   = aPix.y,
				bpp = aPix.bpp
			) )
			A.drawer.setPixel( newImg.content.map[aPix.y][aPix.x] );

	print "%s |" % (t.get())

	A.content.map = newImg.content.map;
	
	# print "| Unparsing                 |",; t.reset();
	# newImg.unparse(newBpp=24);
	# print "%s |" % (t.get())

	# print "| Writing File              |",; t.reset();
	# with open("mergeSub.bmp", "w") as f:
	# 	f.write( newImg.binData );
	# print "%s |" % (t.get())





















# Révèle la couleur RGB spécifiée en blanc et le reste en noir #
################################################################
# @sysarg		1		Image à traiter
# @stsarg		2		Image de sortie
#
# @history
#			Parse le fichier d'entrée
#			colore l'image
#			Unparse le tout et l'enregistre dans le fichier de sortie
def revealShapes(img, red=0,green=0,blue=0, seuil=50):
	t = Timer();
	# img = BMPFile()

	rMin, rMax = red-seuil, red+seuil
	gMin, gMax = green-seuil, green+seuil
	bMin, bMax = blue-seuil, blue+seuil


	# lecture du fichier
	# print "| Reading file              |",; t.reset();
	# with open( sys.argv[1] ) as f:
	# 	binFile = f.read();
	# print "%s |" % (t.get())

	# # parsage
	# print "| Parsing image             |",; t.reset();
	# img.parse( binFile );
	# print "%s |" % (t.get())


	# coloration
	print "| Revealing color           |",; t.reset();
	for line in img.content.map:
		for pixel in line:
			# si on a la couleur spécifiée
			if rMin <= pixel.r <= rMax and gMin <= pixel.g <= gMax and bMin <= pixel.b <= bMax:
				pixel.setRGB(255,255,255)  # on colore en blanc
			else:
				pixel.setRGB(0,0,0)        # sinon on colore en noir
			img.drawer.setPixel( pixel );
	print "%s |" % (t.get())
	
	# print "| Unparsing                 |",; t.reset();
	# img.unparse(newBpp=24);
	# print "%s |" % (t.get())

	# print "| Writing File              |",; t.reset();
	# with open( sys.argv[2], "w") as f:
	# 	f.write( img.binData );
	# print "%s |" % (t.get())





# Colore une la forme contenant le pixel de coordonnées donnée #
################################################################
# @sysarg		1		Image à traiter
# @stsarg		2		Image de sortie
#
# @history
#			Parse le fichier d'entrée
#			colore la forme
#			Unparse le tout et l'enregistre dans le fichier de sortie
def colorShape(img, x=0, y=0):
	t = Timer();
	# img = BMPFile()

	# # lecture du fichier
	# print "| Reading file              |",; t.reset();
	# with open( sys.argv[1] ) as f:
	# 	binFile = f.read();
	# print "%s |" % (t.get())

	# # parsage
	# print "| Parsing image             |",; t.reset();
	# img.parse( binFile );
	# print "%s |" % (t.get())



	# condition (si loin du noir uniquement)
	if img.content.map[y][x].r + img.content.map[y][x].g + img.content.map[y][x].b <= 100: # si loin du noir
		print "\n*** must be a WHITE pixel"
		exit()





	# récupère la forme
	print "| Getting shape             |",; t.reset();
	shape = FX.Shape.getShape(img.drawer, img.content.map[y][x], img.content.map)
	img.drawer.refresh();

	# on colorie la forme en rouge
	for pixel in shape:
		pixel.setRGB(255,0,0);
	print "%s |" % (t.get())



	# print "| Unparsing                 |",; t.reset();
	# img.unparse(newBpp=24);
	# print "%s |" % (t.get())

	# print "| Writing File              |",; t.reset();
	# with open( sys.argv[2], "w") as f:
	# 	f.write( img.binData );
	# print "%s |" % (t.get())










# Colore toutes les formes chacune avec des couleurs aléatoires #
#################################################################
# @sysarg		1		Image à traiter
# @stsarg		2		Image de sortie
#
# @history
#			Parse le fichier d'entrée
#			colore les formes
#			Unparse le tout et l'enregistre dans le fichier de sortie
def colorAllShapes(img):
	t = Timer();
	# img = BMPFile()

	# # lecture du fichier
	# print "| Reading file              |",; t.reset();
	# with open( sys.argv[1] ) as f:
	# 	binFile = f.read();
	# print "%s |" % (t.get())

	# # parsage
	# print "| Parsing image             |",; t.reset();
	# img.parse( binFile );
	# print "%s |" % (t.get())




	# récupère les formes
	print "| Getting shapes            |",; t.reset();
	already = []
	for line in img.content.map:
		for pixel in line:
			# condition (si ce n'est pas le fond ~= noir)
			if pixel.r + pixel.g + pixel.b > 3*100 and pixel not in already: # si loin du noir
				shape = FX.Shape.getShape(img.drawer, pixel, img.content.map)
				print "shape detected"
				R, G, B = random.randint(0,255), random.randint(0,255), random.randint(0,255)
				
				# on colorie la forme en rouge
				for p in shape:
					p.setRGB(R, G, B);
				already += shape

	print "%s |" % (t.get())



	# print "| Unparsing                 |",; t.reset();
	# img.unparse(newBpp=24);
	# print "%s |" % (t.get())

	# print "| Writing File              |",; t.reset();
	# with open( sys.argv[2], "w") as f:
	# 	f.write( img.binData );
	# print "%s |" % (t.get())











# Récupère et colore les contours à partir de formes pleines #
##############################################################
# @sysarg		1		Image à traiter
# @stsarg		2		Image de sortie
#
# @history
#			Parse le fichier d'entrée
#			récupère les contours
# 			trace les contours
#			Unparse le tout et l'enregistre dans le fichier de sortie
def testStroke(img):
	t = Timer();
	# img = BMPFile()

	# lecture du fichier
	# print "| Reading file              |",; t.reset();
	# with open( sys.argv[1] ) as f:
	# 	binFile = f.read();
	# print "%s |" % (t.get())

	# # parsage
	# print "| Parsing image             |",; t.reset();
	# img.parse( binFile );
	# print "%s |" % (t.get())


	strokes = []
	# récupère la forme
	print "| Getting Strokes           |",; t.reset();
	strokes = FX.Shape.getStrokes(img.content.map)

	# met tout les pixels hors des contours en noir et les autres en blanc
	for line in img.content.map:
		for pixel in line:
			if pixel in strokes:
				pixel.setRGB(255,255,255)
			else:
				pixel.setRGB(0,0,0)
			img.drawer.setPixel( pixel );
	print "%s |" % (t.get())



	# print "| Unparsing                 |",; t.reset();
	# img.unparse(newBpp=24);
	# print "%s |" % (t.get())

	# print "| Writing File              |",; t.reset();
	# with open( sys.argv[2], "w") as f:
	# 	f.write( img.binData );
	# print "%s |" % (t.get())
















# teste la fonction de filtrage par filtre moyen #
##################################################
# @sysarg		1		le fichier d'origine
# @stsarg		2		le fichier de sortie (lissé)
#
# @history
#			Parse le fichier d'origine
#			Applique le filtre
#			Unparse l'image et l'enregistre dans le fichier de sortie
def testAverageFilter(img):
	t = Timer();
	

	# lecture du fichier
	# print "| Reading Image             |",; t.reset();
	# with open( sys.argv[1] ) as file:
	# 	binFile = file.read()
	# print "%s |" % (t.get())


	# img = BMPFile(); # Instanciation du BMPFile


	# # Parsing
	# print "| Parsing file              |",; t.reset();
	# img.parse( binFile );
	# print "%s |" % (t.get())


	print "| Filtre moyen              |",; t.reset();
	img.content.map = FX.Filter.averageFilter(img.drawer, img.content.map)
	print "%s |" % (t.get())

	# Unparsing
	# print "| Unparsing file            |",; t.reset();
	# img.unparse()
	# print "%s |" % (t.get())

	# # image to stdout
	# print "| Writing file              |",; t.reset();
	# img.write( sys.argv[2] )
	# print "%s |" % (t.get())

	











# teste le filtre de "Laplace" sur d'une image #
##############################################
# @sysarg		1		le fichier d'origine
# @stsarg		2		le fichier de sortie (filtré)
#
# @history
#			Parse le fichier d'origine
#			Applique le filtre
#			Unparse l'image et l'enregistre dans le fichier de sortie
def testLaplace(img):
	t = Timer();
	

	# # lecture du fichier
	# print "| Reading Image             |",; t.reset();
	# with open( sys.argv[1] ) as file:
	# 	binFile = file.read()
	# print "%s |" % (t.get())


	# img = BMPFile(); # Instanciation du BMPFile


	# # Parsing
	# print "| Parsing file              |",; t.reset();
	# img.parse( binFile );
	# print "%s |" % (t.get())


	print "| Application du filtre     |",; t.reset();
	img.content.map = FX.Filter.Laplace(img.drawer, img.content.map);
	print "%s |" % (t.get())

	# Unparsing
	# print "| Unparsing file            |",; t.reset();
	# img.unparse()
	# print "%s |" % (t.get())

	# # image to stdout
	# print "| Writing file              |",; t.reset();
	# img.write( sys.argv[2] )
	# print "%s |" % (t.get())



# teste le filtre de "Roberts" sur d'une image #
################################################
# @sysarg		1		le fichier d'origine
# @stsarg		2		le fichier de sortie (filtré)
#
# @history
#			Parse le fichier d'origine
#			Applique le filtre
#			Unparse l'image et l'enregistre dans le fichier de sortie
def testRoberts(img):
	t = Timer();
	

	# lecture du fichier
	# print "| Reading Image             |",; t.reset();
	# with open( sys.argv[1] ) as file:
	# 	binFile = file.read()
	# print "%s |" % (t.get())


	# img = BMPFile(); # Instanciation du BMPFile


	# # Parsing
	# print "| Parsing file              |",; t.reset();
	# img.parse( binFile );
	# print "%s |" % (t.get())


	print "| Application du filtre     |",; t.reset();
	img.content.map = FX.Filter.Roberts(img.drawer, img.content.map);
	print "%s |" % (t.get())

	# Unparsing
	# print "| Unparsing file            |",; t.reset();
	# img.unparse()
	# print "%s |" % (t.get())

	# # image to stdout
	# print "| Writing file              |",; t.reset();
	# img.write( sys.argv[2] )
	# print "%s |" % (t.get())

	




# teste le filtre de "Prewitt" sur d'une image #
################################################
# @sysarg		1		le fichier d'origine
# @stsarg		2		le fichier de sortie (filtré)
#
# @history
#			Parse le fichier d'origine
#			Applique le filtre
#			Unparse l'image et l'enregistre dans le fichier de sortie
def testPrewitt(img):
	t = Timer();
	

	# lecture du fichier
	# print "| Reading Image             |",; t.reset();
	# with open( sys.argv[1] ) as file:
	# 	binFile = file.read()
	# print "%s |" % (t.get())


	# img = BMPFile(); # Instanciation du BMPFile


	# # Parsing
	# print "| Parsing file              |",; t.reset();
	# img.parse( binFile );
	# print "%s |" % (t.get())


	print "| Application du filtre     |",; t.reset();
	FX.Filter.Prewitt(img.drawer, img.content.map);
	print "%s |" % (t.get())

	# Unparsing
	# print "| Unparsing file            |",; t.reset();
	# img.unparse()
	# print "%s |" % (t.get())

	# # image to stdout
	# print "| Writing file              |",; t.reset();
	# img.write( sys.argv[2] )
	# print "%s |" % (t.get())

	






# teste le filtre de "Sobel" sur d'une image #
##############################################
# @sysarg		1		le fichier d'origine
# @stsarg		2		le fichier de sortie (filtré)
#
# @history
#			Parse le fichier d'origine
#			Applique le filtre
#			Unparse l'image et l'enregistre dans le fichier de sortie
def testSobel(img):
	t = Timer();
	

	# lecture du fichier
	# print "| Reading Image             |",; t.reset();
	# with open( sys.argv[1] ) as file:
	# 	binFile = file.read()
	# print "%s |" % (t.get())


	# img = BMPFile(); # Instanciation du BMPFile


	# # Parsing
	# print "| Parsing file              |",; t.reset();
	# img.parse( binFile );
	# print "%s |" % (t.get())


	print "| Application du filtre     |",; t.reset();
	img.content.map = FX.Filter.Sobel(img.drawer, img.content.map);
	print "%s |" % (t.get())

	# Unparsing
	# print "| Unparsing file            |",; t.reset();
	# img.unparse()
	# print "%s |" % (t.get())

	# # image to stdout
	# print "| Writing file              |",; t.reset();
	# img.write( sys.argv[2] )
	# print "%s |" % (t.get())

	









# teste le filtre de Convolution sur d'une image #
##############################################
# @sysarg		1		le fichier d'origine
# @stsarg		2		le fichier de sortie (filtré)
#
# @history
#			Parse le fichier d'origine
#			Applique le filtre
#			Unparse l'image et l'enregistre dans le fichier de sortie
def testConvolution(img):
	t = Timer();
	

	# lecture du fichier
	# print "| Reading Image             |",; t.reset();
	# with open( sys.argv[1] ) as file:
	# 	binFile = file.read()
	# print "%s |" % (t.get())


	# img = BMPFile(); # Instanciation du BMPFile


	# # Parsing
	# print "| Parsing file              |",; t.reset();
	# img.parse( binFile );
	# print "%s |" % (t.get())

	kernel = [
		[ 4, 3, 2, 3, 4],
		[ 3, 2, 1, 2, 3],
		[ 2, 1, 0, 1, 2],
		[ 3, 2, 1, 2, 3],
		[ 4, 3, 2, 3, 4]
	]

	print "| Application du filtre     |",; t.reset();
	img.content.map = FX.Filter.Convolution(img.drawer, img.content.map, kernel);
	print "%s |" % (t.get())

	# Unparsing
	# print "| Unparsing file            |",; t.reset();
	# img.unparse()
	# print "%s |" % (t.get())

	# # image to stdout
	# print "| Writing file              |",; t.reset();
	# img.write( sys.argv[2] )
	# print "%s |" % (t.get())

	












# teste le passage au bichromatique #
#####################################
# @sysarg		1		le fichier d'origine
# @stsarg		2		le fichier de sortie (bichromé)
#
# @history
#			Parse le fichier d'origine
#			Applique le filtre
#			Unparse l'image et l'enregistre dans le fichier de sortie
def testBichrome(img):
	t = Timer();
	

	# lecture du fichier
	# print "| Reading Image             |",; t.reset();
	# with open( sys.argv[1] ) as file:
	# 	binFile = file.read()
	# print "%s |" % (t.get())


	# img = BMPFile(); # Instanciation du BMPFile


	# # Parsing
	# print "| Parsing file              |",; t.reset();
	# img.parse( binFile );
	# print "%s |" % (t.get())


	print "| Application du filtre     |",; t.reset();
	for line in img.content.map:
		for pixel in line:
			pixel.setRGB(
				255*int( (pixel.r+pixel.g+pixel.b)/3 >= 128 ),
				255*int( (pixel.r+pixel.g+pixel.b)/3 >= 128 ),
				255*int( (pixel.r+pixel.g+pixel.b)/3 >= 128 )
			)
			img.drawer.setPixel( pixel );
	img.drawer.refresh();
	print "%s |" % (t.get())


	# Unparsing
	# print "| Unparsing file            |",; t.reset();
	# img.unparse()
	# print "%s |" % (t.get())

	# # image to stdout
	# print "| Writing file              |",; t.reset();
	# img.write( sys.argv[2] )
	# print "%s |" % (t.get())

	








# teste le filtre de passe haut sur d'une image #
#################################################
# @sysarg		1		le fichier d'origine
# @stsarg		2		le fichier de sortie (filtré)
#
# @history
#			Parse le fichier d'origine
#			Applique le filtre
#			Unparse l'image et l'enregistre dans le fichier de sortie
def testHighPass(img):
	t = Timer();
	

	# lecture du fichier
	# print "| Reading Image             |",; t.reset();
	# with open( sys.argv[1] ) as file:
	# 	binFile = file.read()
	# print "%s |" % (t.get())


	# img = BMPFile(); # Instanciation du BMPFile


	# # Parsing
	# print "| Parsing file              |",; t.reset();
	# img.parse( binFile );
	# print "%s |" % (t.get())


	print "| Application du filtre     |",; t.reset();
	img.content.map = FX.Filter.HighPass(img.drawer, img.content.map);
	print "%s |" % (t.get())

	# Unparsing
	# print "| Unparsing file            |",; t.reset();
	# img.unparse()
	# print "%s |" % (t.get())

	# # image to stdout
	# print "| Writing file              |",; t.reset();
	# img.write( sys.argv[2] )
	# print "%s |" % (t.get())

	

