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
print "| 12) %s |" % exactLength("Lissage", 21, -1)
print "+---------------------------+"
print "| %s |" % exactLength("TESTS DE DIFFERENCES", 25, 0)
print "| %s |" % exactLength("", 25, 0)
print "| 20) %s |" % exactLength("Difference en %", 21, -1)
print "| 21) %s |" % exactLength("Difference par P", 21, -1)
print "| 22) %s |" % exactLength("Difference en image", 21, -1)
print "| 23) %s |" % exactLength("Fusion d'images (+)", 21, -1)
print "| 24) %s |" % exactLength("Fusion d'images (-)", 21, -1)
print "+---------------------------+"
print
while True:
	action = int( raw_input("choix: ") )
	if action >= 0 and action < 30:
		break;

print
print "+---------------------------+---------+"

execTime = Timer(); execTime.reset();

result = ""

# fichier
if   action == 0:
	testManualCreation()            # teste la création d'un fichier à partir d'une matrice uniquement
elif action == 1:
	result = testFileIntegrity()    # teste le PARSE/UNPARSE
elif action == 2:
	result = printIntPalette()      # affiche la palette d'une image

# bruits
elif action == 10:
	testSaltAndPepper()             # teste le bruitage/débruitage de type "Sel & Poivre"
elif action == 11:
	testAdditiveNoise()             # teste le bruitage/débruitage de type "Additif"
elif action == 12:
	testSmooth()                    # teste le lissage

# performances
elif action == 20:
	printImageQuality()             # compare 2 images et donne le pourcentage de ressemblance/différence
elif action == 21:
	print "not implemented yet"
	exit()
	printImageQualityByPower()      # compare 2 images et donne le pourcentage de ressemblance/différence (utilisant la puissance)
elif action == 22:
	imageForImageQuality()          # crée une image correspondant aux différences de 2 images
elif action == 23:
	mergeImagesAdditive()           # crée une image étant la fusion (addition) de 2 images
elif action == 24:
	mergeImagesSubstractive()       # crée une image étant la fusion (soustractive) de 2 images
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