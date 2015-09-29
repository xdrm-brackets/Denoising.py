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
	def smooth(self, pixelMap, seuil=0):
		width  = len( pixelMap[0] )
		height = len( pixelMap    )

		a = int( seuil )

		while a >= 100:
			a /= 100;

		kernel = [
			[a, a, a],
			[a, 0, a],
			[a, a, a],
		]

		pixelMap = self.Convolution(pixelMap, kernel)




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
	def Convolution(self, pixelMap, kernel=None):
		width  = len( pixelMap[0] )
		height = len( pixelMap    )

		if kernel == None:
			kernel = [
				[ 4, 3, 2, 3, 4],
				[ 3, 2, 1, 2, 3],
				[ 2, 1, 0, 1, 2],
				[ 3, 2, 1, 2, 3],
				[ 4, 3, 2, 3, 4]
			]

		kMidWidth  = len( kernel[0] ) // 2
		kMidHeight = len( kernel    ) // 2

		# map de résultat (filtrée)
		convolvedMap = [ ]
		
		convolvedMap.append( [] );
		# on parcourt tout les pixels
		for y in range(0, height):

			# on rajoute une ligne à la map filtrée
			convolvedMap.append( [] )

			for x in range(0, width):

				pixel = pixelMap[y][x];

				


				# nb total résultant du kernel des valeurs positives
				kernelFactor = 0;
				for b in kernel:
					for a in b:
						if a > 0:
							kernelFactor += a;

				# on définit la matrice de même taille que le kernel mais correspondant aux pixels superposés
				pixelM = [];

				for b in range(-kMidHeight, 1+kMidHeight):
					pixelM.append( [] );
					for a in range(-kMidWidth, 1+kMidWidth):
						# on met les valeurs entre 0 et longueur ou largeur pour pas récupérer les valeurs de l'autre côté (lissage bizarre)
						ruledX = 0 if x+a<0 else width-1  if x+a>=width  else x+a;
						ruledY = 0 if y+b<0 else height-1 if y+b>=height else y+b;
						
						# on ajoute le pixel courant
						pixelM[len(pixelM)-1].append( pixelMap[ruledY][ruledX] );

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