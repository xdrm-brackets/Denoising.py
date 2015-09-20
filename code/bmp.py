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
print "| <in>  %s |" % exactLength( sys.argv[1], 19, -1) 
print "| <out> %s |" % exactLength( sys.argv[2], 19, -1)
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
print "| 11) %s |" % exactLength("Additif", 21, -1)
print "+---------------------------+"
print "| %s |" % exactLength("TESTS DE DIFFERENCES", 25, 0)
print "| %s |" % exactLength("", 25, 0)
print "| 20) %s |" % exactLength("Difference en %", 21, -1)
print "| 21) %s |" % exactLength("Difference par P", 21, -1)
print "| 22) %s |" % exactLength("Difference en image", 21, -1)
print "| 23) %s |" % exactLength("Fusion d'images (+)", 21, -1)
print "| 24) %s |" % exactLength("Fusion d'images (-)", 21, -1)
print "+---------------------------+"
print "| %s |" % exactLength("TESTS DE FORMES", 25, 0)
print "| %s |" % exactLength("", 25, 0)
print "| 30) %s |" % exactLength("Reveler une teinte", 21, -1)
print "| 31) %s |" % exactLength("Colorer une forme", 21, -1)
print "+---------------------------+"
print "| %s |" % exactLength("TESTS DE FILTRES", 25, 0)
print "| %s |" % exactLength("", 25, 0)
print "| 40) %s |" % exactLength("Lissage", 21, -1)
print "| 41) %s |" % exactLength("Roberts", 21, -1)
print "| 42) %s |" % exactLength("Prewitt", 21, -1)
print "| 43) %s |" % exactLength("Sobel", 21, -1)
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
	testManualCreation(arg1, arg2)            # teste la création d'un fichier à partir d'une matrice uniquement
elif action == 1:
	print startStr
	result = testFileIntegrity()    # teste le PARSE/UNPARSE
elif action == 2:
	print startStr
	result = printIntPalette()      # affiche la palette d'une image

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
	testSaltAndPepper(arg1, arg2, arg3, arg4)  # teste le bruitage/débruitage de type "Sel & Poivre"
elif action == 11:
	print startStr
	testAdditiveNoise()             # teste le bruitage/débruitage de type "Additif"
# performances
elif action == 20:
	print startStr
	printImageQuality()             # compare 2 images et donne le pourcentage de ressemblance/différence
elif action == 21:
	print startStr
	print "not implemented yet"
	exit()
	printImageQualityByPower()      # compare 2 images et donne le pourcentage de ressemblance/différence (utilisant la puissance)
elif action == 22:
	print startStr
	imageForImageQuality()          # crée une image correspondant aux différences de 2 images
elif action == 23:
	print startStr
	mergeImagesAdditive()           # crée une image étant la fusion (addition) de 2 images
elif action == 24:
	print startStr
	mergeImagesSubstractive()       # crée une image étant la fusion (soustractive) de 2 images
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
	revealShapes(arg1, arg2, arg3, arg4)  # révèle la couleur spécifiée
elif action == 31:
	x = raw_input("abscisses(x) [0]: ")
	y = raw_input("ordonnées(y) [0]: ")
	arg1, arg2 = 0,0
	if x != "":
		arg1 = int(x)
	if y != "":
		arg2 = int(y)
	print startStr
	colorShape(arg1, arg2)       # colorie la forme contenant le pixel de coordonnées donné


# filtres
elif action == 40:
	s = raw_input("Seuil [5]: ");
	arg1 = 5
	if s != "":
		arg1 = int(s)
	print startStr
	testSmooth(arg1)                # teste le lissage
elif action == 41:
	print startStr
	testRoberts()                # teste le filtre de Roberts
elif action == 42:
	print startStr
	testPrewitt()                # teste le filtre de Prewitt
elif action == 43:
	print startStr
	testSobel()                # teste le filtre de Prewitt

else:
	print "Wrong choice"
	exit();

print "+---------------------------+---------+"
print "| EXECUTION TIME            | %s |" % execTime.get()
print "+---------------------------+---------+"
print
print result

############ TESTS ############

# testManualCreation()   # teste la création d'un fichier à partir d'une matrice uniquement
# testFileIntegrity()    # teste le PARSE/UNPARSE
# printIntPalette()      # affiche la palette d'une image

# testSaltAndPepper()    # teste le bruitage/débruitage de type "Sel & Poivre"
# testAdditiveNoise()    # teste le bruitage/débruitage de type "Additif"

# printImageQuality()    # compare 2 images et donne le pourcentage de ressemblance/différence

# imageForImageQuality() # crée une image correspondant aux différences de 2 images
# mergeImages()          # crée une image étant la fusion (addition) de 2 images

############ CALIBRATE ############

# calSaltAndPepper()     # Calibration en créant des fichiers pour les paramètres différents de débruitage dans le dossier /SaltAndPepper (sert à comparer)