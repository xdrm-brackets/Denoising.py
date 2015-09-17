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



############ TESTS ############

# testManualCreation()   # teste la création d'un fichier à partir d'une matrice uniquement
# testFileIntegrity()    # teste le PARSE/UNPARSE
# printIntPalette()      # affiche la palette d'une image

# testSaltAndPepper()    # teste le bruitage/débruitage de type "Sel & Poivre"
# testAdditiveNoise()    # teste le bruitage/débruitage de type "Additif"

printImageQuality()    # compare 2 images et donne le pourcentage de ressemblance/différence

# imageForImageQuality() # crée une image correspondant aux différences de 2 images
# mergeImages()          # crée une image étant la fusion (addition) de 2 images

############ CALIBRATE ############

# calSaltAndPepper()     # Calibration en créant des fichiers pour les paramètres différents de débruitage dans le dossier /SaltAndPepper (sert à comparer)