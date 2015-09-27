# ~*~ encoding: utf-8 ~*~ #

import random
import time
import sys
sys.path.append(sys.path[0]+'/..')
from BMPFile import RGBPixel

class Filter:

	# Applique un filtre de type "lissage" ou "floutae" à l'image #
	###############################################################
	# @param pixelMap 		Matrice de pixel à traiter (modifier)
	# @param seuil			Ecart entre le pixel et ses alentours à partir duquel on applique le lissage 
	#
	def smooth(self, pixelMap, seuil=5):
		width  = len( pixelMap[0] )
		height = len( pixelMap    )

		if seuil < 0 or seuil > 255: # si le seuil est incohérent  => valeur par défaut (5)
			seuil = 5;


		# on parcourt tout les pixels
		for y in range(0, len(pixelMap)):
			for x in range(0, len(pixelMap[y])):

				# on calcule la moyenne des valeurs R G B du pixel courant
				pMoy = ( pixelMap[y][x].r + pixelMap[y][x].g + pixelMap[y][x].b ) / 3


				xmin, ymin, xmax, ymap = x, y, x, y;                       # les bornes ducarré 3x3 autour du pixel 
				rMoy, gMoy, bMoy, count = 0.0, 0.0, 0.0, 0                 # initialisation des variables de moyennes et de total
				rInterval, gInterval, bInterval, rgbInterval = 0, 0, 0, 0  # initialisation des variables d'intervalles entre les couleurs


				# GESTION DES ANGLES

				# ordonnées: borne inférieure
				if y-1 > -1:
					ymin = y-1
				# ordonnées: borne supérieure
				if y+1 < height:
					ymax = y+1
				# abscisses: borne inférieure
				if x-1 > -1:
					xmin = x-1
				# abscisses: borne supérieure
				if x+1 < width:
					xmax = x+1


				pixels = [ pixelMap[y][xmin], pixelMap[y][xmax], pixelMap[ymin][x], pixelMap[ymax][x] ];
				for p in pixels:
					if p != pixelMap[y][x]:
						rMoy += p.r;
						gMoy += p.g;
						bMoy += p.b;
						count += 1

				# si il y a au moins un pixel autour (normalement tjs mais évite l'erreur div par zéro)
				if count > 0:
					# on calcule les moyennes somme(xi) / n
					rMoy = int( rMoy / count )
					gMoy = int( gMoy / count )
					bMoy = int( bMoy / count )

					# calcul de la différence entre les couleurs du pixel et la moyenne des couleurs des pixels autour
					rInterval = abs( pixelMap[y][x].r - rMoy )
					gInterval = abs( pixelMap[y][x].g - gMoy )
					bInterval = abs( pixelMap[y][x].b - bMoy )

					# calcul de la différence en nuance de gris (moyenne des couleurs)
					rgbInterval = ( rInterval + gInterval + bInterval ) / 3

					# si la couleur est trop "différente" (dépend du seuil) alors on remplace sa couleur par la moyenne des couleurs alentours
					if rgbInterval > seuil:
						pixelMap[y][x].setRGB(rMoy, gMoy, bMoy);






	# applique le filtre de "Laplace" sur l'image #
	###############################################
	# @param pixelMap		la matrice de pixels à modifier
	#
	# @history
	#			applique le filtre
	#
	#             -1  -1  -1
	#
	#  1/8   *    -1   8  -1
	#
	#             -1  -1  -1
	def Laplace(self, pixelMap):
		# on parcourt tout les pixels
		for y in range(1, len(pixelMap)-1):
			for x in range(1, len(pixelMap[y])-1):

				pixel = pixelMap[y][x];

				filters = [
					[
						[-1, -1, -1],
						[-1,  8, -1],
						[-1, -1, -1]
					]
				]

				pixelM = [ pixelMap[y+1][x-1:x+2], pixelMap[y][x-1:x+2], pixelMap[y-1][x-1:x+2] ]

				r,g,b = 0,0,0

				for j in range(0,len(pixelM)):
					for i in range(0,len(pixelM[j])):
						# pour chacun des filtres
						for f in filters:
							r += pixelM[j][i].r * f[j][i]
							g += pixelM[j][i].g * f[j][i]
							b += pixelM[j][i].b * f[j][i]

				r = r/(1*len(filters)) % 256
				g = g/(1*len(filters)) % 256
				b = b/(1*len(filters)) % 256

				# définition des couleurs
				pixel.setRGB(
				# print "%s - %s - %s" % (
					int( r ),
					int( g ),
					int( b )
				)



	# applique le filtre de "Roberts" sur l'image #
	###############################################
	# @param pixelMap		la matrice de pixels à modifier
	#
	# @history
	#			applique le filtre
	#
	# 1  0
	#
	# 0  -1
	#
	def Roberts(self, pixelMap):

		# on parcourt tout les pixels
		for y in range(1, len(pixelMap)-1):
			for x in range(1, len(pixelMap[y])-1):

				pixel = pixelMap[y][x]

				filters = [
					[ [1, 0], [0,-1] ],
					[ [0, 1], [-1,0] ]
				]

				pixelM = [ pixelMap[y][x:x+1], pixelMap[y+1][x:x+1] ] 

				r,g,b = 0,0,0

				for j in range(0,len(pixelM)):
					for i in range(0,len(pixelM[j])):
						# pour chacun des filtres
						for f in filters:
							r += pixelM[j][i].r * f[j][i]
							g += pixelM[j][i].g * f[j][i]
							b += pixelM[j][i].b * f[j][i]

				r = r % 256
				g = g % 256
				b = b % 256


				# définition des couleurs
				pixel.setRGB(
				# print "%s - %s - %s" % (
					int( r ),
					int( g ),
					int( b )
				)



	# applique le filtre de "Prewitt" sur l'image #
	###############################################
	# @param pixelMap		la matrice de pixels à modifier
	#
	# @history
	#			applique le filtre
	#
	#             -1   0   1         -1   -1   -1
	#
	#  1/3   *    -1   0   1      +   0    0    0
	#
	#             -1   0   1          1    1    1
	def Prewitt(self, pixelMap):
		# on parcourt tout les pixels
		for y in range(1, len(pixelMap)-1):
			for x in range(1, len(pixelMap[y])-1):

				pixel = pixelMap[y][x];

				filters = [
					3*[[-1, 0, 1]],
					[ 3*[-1], 3*[0], 3*[1] ]
				]

				pixelM = [ pixelMap[y-1][x-1:x+1], pixelMap[y][x-1:x+1], pixelMap[y+1][x-1:x+1] ] 

				r,g,b = 0,0,0

				for j in range(0,len(pixelM)):
					for i in range(0,len(pixelM[j])):
						# pour chacun des filtres
						for f in filters:
							r += pixelM[j][i].r * f[j][i]
							g += pixelM[j][i].g * f[j][i]
							b += pixelM[j][i].b * f[j][i]

				r = r/4 % 256
				g = g/4 % 256
				b = b/4 % 256


				# définition des couleurs
				pixel.setRGB(
				# print "%s - %s - %s" % (
					int( r ),
					int( g ),
					int( b )
				)



	# applique le filtre de "Sobel" sur l'image #
	###############################################
	# @param pixelMap		la matrice de pixels à modifier
	#
	# @history
	#			applique le filtre
	#
	#             -1   0   1         -1   -2   -1
	#
	#  1/4   *    -2   0   2      +   0    0    0
	#
	#             -1   0   1          1    2    1
	def Sobel(self, pixelMap):
		# on parcourt tout les pixels
		for y in range(1, len(pixelMap)-1):
			for x in range(1, len(pixelMap[y])-1):

				pixel = pixelMap[y][x];

				filters = [
					[ [-1,0,1],   [-2,0,2], [-1,0,1]  ],
					[ [-1,-2,-1], [0,0,0],  [1,2,1]   ],
					[ [0,1,2],    [-1,0,1], [-2,-1,0] ]
				]

				pixelM = [ pixelMap[y-1][x-1:x+1], pixelMap[y][x-1:x+1], pixelMap[y+1][x-1:x+1] ] 

				r,g,b = 0,0,0

				for j in range(0,len(pixelM)):
					for i in range(0,len(pixelM[j])):
						# pour chacun des filtres
						for f in filters:
							r += pixelM[j][i].r * f[j][i]
							g += pixelM[j][i].g * f[j][i]
							b += pixelM[j][i].b * f[j][i]

				r = r/4 % 256
				g = g/4 % 256
				b = b/4 % 256


				# définition des couleurs
				pixel.setRGB(
				# print "%s - %s - %s" % (
					int( r ),
					int( g ),
					int( b )
				)


	# applique le filtre de "convolution" sur l'image #
	###################################################
	# @param pixelMap		la matrice de pixels à modifier
	#
	# @history
	#			applique le filtre
	#
	#             -1  -1  -1
	#
	#  1/8   *    -1   8  -1
	#
	#             -1  -1  -1
	def Convolution(self, pixelMap):
		width  = len( pixelMap[0] )
		height = len( pixelMap    )

		# map de résultat (filtrée)
		convolvedMap = [ ]
		
		convolvedMap.append( [] );
		# on parcourt tout les pixels
		for y in range(0, height):

			# on rajoute une ligne à la map filtrée
			convolvedMap.append( [] )

			for x in range(0, width):

				pixel = pixelMap[y][x];

				kernel = [
					[ 4, 3, 2, 3, 4],
					[ 3, 2, 1, 2, 3],
					[ 2, 1, 0, 1, 2],
					[ 3, 2, 1, 2, 3],
					[ 4, 3, 2, 3, 4]
				]


				# nb total résultant du kernel des valeurs positives
				kernelFactor = 0;
				for b in kernel:
					for a in b:
						if a > 0:
							kernelFactor += a;

				# on définit la matrice de même taille que le kernel mais correspondant aux pixels superposés
				pixelM = [];
				print "(%s, %s)" % (-len(kernel)/2, 1+len(kernel)/2)

				for b in range(1-len(kernel)/2, 1+len(kernel)/2):
					pixelM.append( [] );
					for a in range(1-len(kernel[b])/2, 1+len(kernel[b])/2):

						print "(%s, %s)" % (b, a)

					
					# 	pixelM[len(pixelM)-1].append( pixelMap[(y+b)%height][(x+a)%width] );
				exit()

				r,g,b = 0,0,0

				for j in range( 0, len(pixelM) ):
					for i in range( 0, len(pixelM[j]) ):
						# pour chacun des filtres
						r += pixelM[j][i].r * kernel[j][i]
						g += pixelM[j][i].g * kernel[j][i]
						b += pixelM[j][i].b * kernel[j][i]

				r = int(r/kernelFactor) % 256
				g = int(g/kernelFactor) % 256
				b = int(b/kernelFactor) % 256


				# définition des couleurs sur la map filtrée
				convolvedMap[y].append( RGBPixel(
					r   = r,
					g   = g,
					b   = b,
					x   = x,
					y   = y,
					bpp = pixel.bpp
				) )

		return convolvedMap