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

# test par défaut puis quitte
# defaultTest();
# exit();

# arrêt si moins de 2 arguments
if len(sys.argv) < 3:
	print "Require 2 args : \n* input image\n* output image"
	exit()




################" INTERFACE "###################

print "+---------------------------+"
print "|                           |"
print "|    TRAITEMENT D'IMAGE     |"
print "|                           |"
print "+---------------------------+"

# ON CREE LES IMAGES
image1 = BMPFile();
image2 = BMPFile();


with open( sys.argv[1] ) as file:
	image1.parse( file.read() );

for line in image1.content.map:
	for pix in line:
		image1.drawer.setPixel( pix );
image1.drawer.refresh();

print "| <in>  %s |" % exactLength( sys.argv[1], 19, -1) 


with open( sys.argv[2] ) as file:
	image2.parse( file.read() )
print "| <out> %s |" % exactLength( sys.argv[2], 19, -1)



################" INTERFACE "###################

# print "+---------------------------+"
# print "|                           |"
# print "|    TRAITEMENT D'IMAGE     |"
# print "|                           |"
# print "+---------------------------+"
# print "| <in>  %s |" % exactLength( sys.argv[1], 19, -1) 
# print "| <out> %s |" % exactLength( sys.argv[2], 19, -1)
print "+---------------------------+"
print "| %s |" % exactLength("TESTS DE FICHIER", 25, 0)
print "| %s |" % exactLength("", 25, 0)
print "|  0) %s |" % exactLength("Creation manuelle", 21, -1)
print "|  1) %s |" % exactLength("Parse/Unparse",     21, -1)
print "|  2) %s |" % exactLength("Afficher palette",  21, -1)
print "+---------------------------+"
print "| %s |" % exactLength("TESTS DE BRUIT", 25, 0)
print "| %s |" % exactLength("", 25, 0)
print "| 10) %s |" % exactLength("Salt&Pepper", 21, -1)
print "| 11) %s |" % exactLength("Additif (Bernouilli)", 21, -1)
print "| 12) %s |" % exactLength("Additif (Gaussien)", 21, -1)
print "+---------------------------+"
print "| %s |" % exactLength("TESTS DE DIFFERENCES", 25, 0)
print "| %s |" % exactLength("", 25, 0)
print "| 20) %s |" % exactLength("Difference en %", 21, -1)
print "| 21) %s |" % exactLength("SNR (origine/bruit)", 21, -1)
print "| 22) %s |" % exactLength("Difference en image", 21, -1)
print "| 23) %s |" % exactLength("Fusion d'images (+)", 21, -1)
print "| 24) %s |" % exactLength("Fusion d'images (-)", 21, -1)
print "+---------------------------+"
print "| %s |" % exactLength("TESTS DE FORMES", 25, 0)
print "| %s |" % exactLength("", 25, 0)
print "| 30) %s |" % exactLength("Reveler une teinte", 21, -1)
print "| 31) %s |" % exactLength("Colorer une forme", 21, -1)
print "| 32) %s |" % exactLength("Colorer les formes", 21, -1)
print "| 33) %s |" % exactLength("Relever les contours", 21, -1)
print "+---------------------------+"
print "| %s |" % exactLength("TESTS DE FILTRES", 25, 0)
print "| %s |" % exactLength("", 25, 0)
print "| 40) %s |" % exactLength("Filtre moyen", 21, -1)
print "| 41) %s |" % exactLength("Laplace", 21, -1)
print "| 42) %s |" % exactLength("Roberts", 21, -1)
print "| 43) %s |" % exactLength("Prewitt", 21, -1)
print "| 44) %s |" % exactLength("Sobel", 21, -1)
print "| 45) %s |" % exactLength("Convolution", 21, -1)
print "| 46) %s |" % exactLength("bichrome", 21, -1)
print "| 47) %s |" % exactLength("Passe Haut", 21, -1)
print "+---------------------------+"
print
while True:
	action = int( raw_input("choix: ") )
	if action >= 0 and action < 50:
		break;

startStr = "\n+---------------------------+---------+"
result = ""
execTime = Timer(); execTime.reset();


# fichier
if   action == 0:
	w = raw_input("width  [100]: ")
	h = raw_input("height [100]: ")
	arg1, arg2 = 100, 100
	if w != "":
		arg1 = int(w)
	if h != "":
		arg2 = int(h)
	print startStr
	testManualCreation(arg1, arg2)                 # teste la création d'un fichier à partir d'une matrice uniquement
elif action == 1:
	print startStr
	result = testFileIntegrity(image1)                   # teste le PARSE/UNPARSE
elif action == 2:
	print startStr
	result = printIntPalette(image1)                     # affiche la palette d'une image

# bruits
elif action == 10:
	inS  = raw_input("seuil bruitage    [50]: ")
	outS = raw_input("seuil débruitage  [1] : ")
	outB = raw_input("borne débruitage  [1] : ")
	s    = raw_input("Lissage ?        (0-1): ")
	arg1, arg2, arg3, arg4 = 50, 1, 1, 1
	if inS != "":
		arg1 = int(inS)
	if outS != "":
		arg2 = int(outS)
	if outB != "":
		arg3 = int(outB)
	if s != "":
		arg4 = int(s)
	print startStr
	testSaltAndPepper(image1, arg1, arg2, arg3, arg4)      # teste le bruitage/débruitage de type "Sel & Poivre"
elif action == 11:
	inS  = raw_input("seuil bruitage    [10]: ")
	outS = raw_input("seuil débruitage  [35] : ")
	arg1, arg2 = 10, 35
	if inS != "":
		arg1 = int(inS)
	if outS != "":
		arg2 = int(outS)
	print startStr
	testAdditiveBernouilliNoise(image1, arg1, arg2)        # teste le bruitage/débruitage de type "Additif"
elif action == 12:
	inS  = raw_input("sigma             [10]: ")
	outS = raw_input("seuil débruitage  [35] : ")
	arg1, arg2 = 10, 35
	if inS != "":
		arg1 = int(inS)
	if outS != "":
		arg2 = int(outS)
	print startStr
	testAdditiveGaussianNoise(image1, arg1, arg2)          # teste le bruitage/débruitage de type "Additif"
# performances
elif action == 20:
	print startStr
	printImageQuality(image1)                            # compare 2 images et donne le pourcentage de ressemblance/différence
elif action == 21:
	print startStr
	printSNR(image1)                                     # compare 2 images et retourne le SNR
elif action == 22:
	print startStr
	imageForImageQuality(image1)                         # crée une image correspondant aux différences de 2 images
elif action == 23:
	print startStr
	mergeImagesAdditive(image1)                          # crée une image étant la fusion (addition) de 2 images
elif action == 24:
	print startStr
	mergeImagesSubstractive(image1)                      # crée une image étant la fusion (soustractive) de 2 images
elif action == 30:
	r  = raw_input("rouge  [0]: ")
	g  = raw_input("vert   [0]: ")
	b  = raw_input("bleu   [0]: ")
	s  = raw_input("seuil [50]: ")
	arg1, arg2, arg3, arg4 = 0,0,0,50
	if r != "":
		arg1 = int(r)
	if g != "":
		arg2 = int(g)
	if b != "":
		arg3 = int(b)
	if s != "":
		arg4 = int(s)
	print startStr
	revealShapes(image1, arg1, arg2, arg3, arg4)           # révèle la couleur spécifiée
elif action == 31:
	x = raw_input("abscisses(x) [0]: ")
	y = raw_input("ordonnées(y) [0]: ")
	arg1, arg2 = 0,0
	if x != "":
		arg1 = int(x)
	if y != "":
		arg2 = int(y)
	print startStr
	colorShape(image1, arg1, arg2)                         # colorie la forme contenant le pixel de coordonnées donné
elif action == 32:
	print startStr
	colorAllShapes(image1)                               # colorie la forme contenant le pixel de coordonnées donné
elif action == 33:
	print startStr
	testStroke(image1)                                   # trace les contours uniquement à partir de formes pleines


# filtres
elif action == 40:
	print startStr
	testAverageFilter(image1)                                   # teste le lissage
elif action == 41:
	print startStr
	testLaplace(image1)                                  # teste le filtre de Laplace
elif action == 42:
	print startStr
	testRoberts(image1)                                  # teste le filtre de Roberts
elif action == 43:
	print startStr
	testPrewitt(image1)                                  # teste le filtre de Prewitt
elif action == 44:
	print startStr
	testSobel(image1)                                    # teste le filtre de Sobel
elif action == 45:
	print startStr
	testConvolution(image1)                              # teste le filtre de Convolution
elif action == 46:
	print startStr
	testBichrome(image1)                                 # teste le passage au bichromatique
elif action == 47:
	print startStr
	testHighPass(image1)                                 # teste le filtre passe haut

else:
	print "Wrong choice"
	exit();

print "+---------------------------+---------+"
print "| EXECUTION TIME            | %s |" % execTime.get()
print "+---------------------------+---------+"
print
print result



raw_input('- [PRESS ANY KEY TO EXIT] -');