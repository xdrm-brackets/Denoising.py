# ~*~ encoding: utf-8 ~*~ #
###########################
#   TRAITEMENT D'IMAGES   #
###########################

# classes
from classes import *

import sys

import random

#affichage
def display_tab(tab):
	x = 0
	y = 0
	for line in tab:
        	for pixel in line:
                	print "[y : %s | x : %s] [%s, %s, %s]" % (y, x, pixel.r, pixel.g, pixel.b)
			x += 1
		x = 0
		y += 1

#ajout du bruit?
#si apparition = 40 % alors 40 % de chance de renvoyer vrai
def bruit(proba):
	if proba >= random.randint(1,100):
		return True
	else:
		return False

#applique le bruit a tout le tableau
def applie_bruit(tab, apparition):
	y = 0
	for line in tab:
        	x = 0
        	for pixel in line:
                	if bruit(apparition) == True:
                        	tab[y][x].r = random.randint(0, 255)
                        	tab[y][x].g = random.randint(0, 255)
                        	tab[y][x].b = random.randint(0, 255)
               		x += 1
        	y += 1
	

#corp du programme
pourcent_bruit = 88
img = BMPFile( sys.argv[1] )
#print img.readableData
#my code
copie_tab = img.map
#print copie_tab[0][0].r
# affichage du tableau
display_tab(copie_tab)
print
#applique une fonction de bruit simple
applie_bruit(copie_tab, pourcent_bruit)
#affichage
display_tab(copie_tab)
