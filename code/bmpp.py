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


# affiche le contenu d un pixel
# tab_pixel : envoi d un bojet de type RGBPixel
def display_pixel(tab_pixel):
	print "moyenne pixel rouge : " + str(tab_pixel.r)
	print "moyenne pixel vert : " + str(tab_pixel.g)
	print "moyenne pixel bleu : " + str(tab_pixel.b)


#fonction qui calcul la moyenne d un bloc
#retourne un objet RGBpixel
#ameliorer cette fonction en prenant en compte la position actuel
def moyenne_bloc(tab, x_actual, y_actual, size):
	print 'Calcul de la moyenne du bloc'
	cpt_x = 0
	cpt_y = 0
	m_pixel = RGBPixel(0,0,0)
        while cpt_y < 3:
                cpt_x = 0
                while cpt_x < 3:
                        m_pixel.setRGB(
                        	m_pixel.r + tab[cpt_y][cpt_x].r,
                        	m_pixel.g + tab[cpt_y][cpt_x].g,
                        	m_pixel.b + tab[cpt_y][cpt_x].b
                        );
                        cpt_x += 1
                cpt_y += 1
        m_pixel.setRGB(
        	m_pixel.r / (size * size),
        	m_pixel.g / (size * size),
        	m_pixel.b / (size * size)
        );
        print 'moyenne red : ' + str(m_pixel.r)
        print 'moyenne green : ' + str(m_pixel.g)
        print 'moyenne blue : ' + str(m_pixel.b)
	return m_pixel

#Si un pixel est contenu dans l intervalle specifie
#pixel_test : pixel a tester
#pixel_moy  : envoi le pixel moyen du bloc
#intervalle : logique flou sur pixel_moy (-intervalle, +intervalle)
#retourne vrai si le pixel est comprit dans l intervalle sinon faux
def intervalle_true(pixel_test, pixel_moy, intervalle):
	if (pixel_moy.r + intervalle < pixel_test.r) or (pixel_moy.r - intervalle > pixel_test.r):
		return False
	if (pixel_moy.g + intervalle < pixel_test.g) or (pixel_moy.g - intervalle > pixel_test.g):
                return False
	if (pixel_moy.b + intervalle < pixel_test.b) or (pixel_moy.b - intervalle > pixel_test.b):
                return False
	return True

#Modification du pixel 
#tab : tableau de pixel
#x  :  position en x du pixel a modifier
#y  : position en y du pixel a modifier
#new pixel : contient les nouvelles valeurs du pixel a modifier
def change_pixel(tab, x, y, new_pixel):
	tab[y][x].setRGB(
		new_pixel.r,
		new_pixel.g,
		new_pixel.b
	);
#Appliquer une fonction de debrutiage
#tab : contient le tableau de pixel a traiter
#max_x : taille du tableau en longueur
#max_y : taille du tableau en hauteur
# size_bloc : taile du bloc a traiter
# intervalle : definit la condition demodification d un pixel
def raise_bruit_one_bloc(tab, max_x, max_y, size_bloc, intervalle):
	x = 0
	y = 0
#def moyenne_bloc(tab, x_actual, y_actual, size):
	moy_pixel = moyenne_bloc(tab, x, y, size_bloc)
#def intervalle_true(pixel_test, pixel_moy, intervalle):
	while y < 3:
		while x < 3:
			#test si le pixel actuel n est pas co;prit dans l intervalle
			if intervalle_true(tab[y][x], moy_pixel, intervalle) == False:
				change_pixel(tab, x, y, moy_pixel)
			x += 1
		y +=1
		x = 0

def raise_bruit_all_bloc(tab, max_x, max_y, size_bloc, intervalle):
	x_actual = 0
	y_actual = 0
	while y_actual + 3 < max_y :
		while x_actual + 3 < max_x :
			raise_bruit_one_bloc(tab, x_actual, y_actual, size_bloc, intervalle)
			x_actual += 1
		y_actual += 1
		x_actual =  0  

#corp du programme
pourcent_bruit = 30
img = BMPFile( sys.argv[1] )
#print img.readableData
#my code
copie_tab = img.map
#print copie_tab[0][0].r
print
#applique une fonction de bruit simple
#applie_bruit_black_white_line(copie_tab, pourcent_bruit)
#test moyenne debruitage
#def raise_bruit_one_bloc(tab, max_x, max_y, size_bloc, intervalle):
display_tab(copie_tab)
raise_bruit_one_bloc(copie_tab, 3, 3, 3, 100)
#raise_bruit_all_bloc(copie_tab, 3, 3, 3, 100)
#affichage du nouveau tableau
display_tab(copie_tab)

#moyenne bloc
#def moyenne_bloc(tab, x_actual, y_actual, size):
moy_pixel = moyenne_bloc(copie_tab, 0, 0, 3)
#afficher le contenu d un pixel
display_pixel(moy_pixel)
