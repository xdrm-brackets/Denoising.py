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
def applie_bruit_mult(tab, apparition):
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
	
def applie_bruit_black_white(tab, apparition):
	y = 0
	for line in tab:
		x = 0
		for pixel in line:
			if bruit(apparition) == True:
				if bruit(50) == True:
					tab[y][x].r = 0
					tab[y][x].g = 0
					tab[y][x].b = 0
				else:
					tab[y][x].r = 255
					tab[y][x].g = 255
					tab[y][x].b = 255
			x =+ 1
		y += 1
				
#applique  un bruit a une seul ligne
def applie_bruit_black_white_line(tab, apparition):
        y = 0
        bruit_present_line = False
        for line in tab:
                x = 0
                for pixel in line:
                        if bruit(apparition) == True and bruit_present_line == False:
                                if bruit(50) == True:
                                        tab[y][x].r = 0
                                        tab[y][x].g = 0
                                        tab[y][x].b = 0
                                else:
                                        tab[y][x].r = 255
                                        tab[y][x].g = 255
                                        tab[y][x].b = 255
                                bruit_present_line = True
                        x += 1
                y += 1
                print "--"
                bruit_present_line = False


#corp du programme
pourcent_bruit = 30
img = BMPFile( sys.argv[1] )
#print img.readableData
#my code
copie_tab = img.map
#print copie_tab[0][0].r
# affichage du tableau
display_tab(copie_tab)
print
#applique une fonction de bruit simple
applie_bruit_black_white_line(copie_tab, pourcent_bruit)
#affichage
display_tab(copie_tab)
