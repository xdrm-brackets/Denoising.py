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

print "+-------------------------+"
print "|   TRAITEMENT D'IMAGE    |"
print "+-------------------------+"
print "| <in>  %s |" % exactLength( sys.argv[1], 17, -1) 
print "| <out> %s |" % exactLength( sys.argv[2], 17, -1)
print "+-------------------------+"
print "| %s |" % exactLength("TESTS DE FICHIER", 23, 0)
print "| %s |" % exactLength("", 23, 0)
print "| 0) %s |" % exactLength("Creation manuelle", 20, -1)
print "| 1) %s |" % exactLength("Parse/Unparse",     20, -1)
print "| 2) %s |" % exactLength("Afficher palette",  20, -1)
print "+-------------------------+"
print "| %s |" % exactLength("TESTS DE BRUIT", 23, 0)
print "| %s |" % exactLength("", 23, 0)
print "| 3) %s |" % exactLength("Salt&Pepper", 20, -1)
print "| 4) %s |" % exactLength("Additif", 20, -1)
print "+-------------------------+"
print "| %s |" % exactLength("TESTS DE DIFFERENCES", 23, 0)
print "| %s |" % exactLength("", 23, 0)
print "| 5) %s |" % exactLength("Difference en %", 20, -1)
print "| 6) %s |" % exactLength("Difference en image", 20, -1)
print "| 7) %s |" % exactLength("Fusion d'images", 20, -1)
print "+-------------------------+"
print
while True:
	action = int( raw_input("choix: ") )
	if action >= 0 and action <= 7:
		break;

print
print "+-------------------------+---------+"

execTime = Timer(); execTime.reset();

if   action == 0:
	testManualCreation()   # teste la création d'un fichier à partir d'une matrice uniquement
elif action == 1:
	testFileIntegrity()    # teste le PARSE/UNPARSE
elif action == 2:
	printIntPalette()      # affiche la palette d'une image
elif action == 3:
	testSaltAndPepper()    # teste le bruitage/débruitage de type "Sel & Poivre"
elif action == 4:
	testAdditiveNoise()    # teste le bruitage/débruitage de type "Additif"
elif action == 5:
	printImageQuality()    # compare 2 images et donne le pourcentage de ressemblance/différence
elif action == 6:
	imageForImageQuality() # crée une image correspondant aux différences de 2 images
elif action == 7:
	mergeImages()          # crée une image étant la fusion (addition) de 2 images
else:
	print "Error! aborting"

print "+-------------------------+---------+"
print "| EXECUTION TIME          | %s |" % execTime.get()
print "+-------------------------+---------+"

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