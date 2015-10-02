# ~*~ encoding: utf-8 ~*~ #

import random
import time

import sys
sys.path.append(sys.path[0]+'/..')
from BMPFile import RGBPixel
 

class Filter:

	# Applique un filtre moyen à l'image de base vers l'image de sortie #
	#####################################################################
	# @param pixelMap 		Matrice de pixel à traiter (modifier)
	# @param seuil			Ecart entre le pixel et ses alentours à partir duquel on applique le lissage 
	#
	#
	# Celà revient à effectuer un produit de convolution avec le noyau de conv. suivant :
	#
	#  1   1   1
	#  1   0   1
	#  1   1   1
	#
	def averageFilter(self, pixelMap):
		return self.Convolution(pixelMap, kernel=[
			[1, 1, 1],
			[1, 0, 1],
			[1, 1, 1]
		] );


	# Applique un filtre de Roberts à l'image de base vers l'image de sortie #
	##########################################################################
	# @param pixelMap 		Matrice de pixel à traiter (modifier)
	#
	#
	# Celà revient à effectuer un produit de convolution avec le noyau de conv. suivant :
	#
	#  1   0
	#  0   -1 
	#
	def Roberts(self, pixelMap):
		return self.Convolution(pixelMap, kernel=[
			[1, 0],
			[0, -1]
		] );

	# Applique un filtre de Laplace à l'image de base vers l'image de sortie #
	##########################################################################
	# @param pixelMap 		Matrice de pixel à traiter (modifier)
	#
	#
	# Celà revient à effectuer un produit de convolution avec le noyau de conv. suivant :
	#
	#  -1   -1   -1
	#  -1    8   -1
	#  -1   -1   -1
	#
	def Laplace(self, pixelMap):
		return self.Convolution(pixelMap, kernel=[
			[-1, -1, -1],
			[-1,  8, -1],
			[-1, -1, -1]
		] );


	# Applique un filtre de Sobel à l'image de base vers l'image de sortie #
	########################################################################
	# @param pixelMap 		Matrice de pixel à traiter (modifier)
	#
	#
	# Celà revient à effectuer un produit de convolution avec le noyau de conv. suivant :
	#
	#  -1   0   1
	#  -2   0   2
	#  -1   0   1
	#
	def Sobel(self, pixelMap):
		return self.Convolution(pixelMap, kernel=[
			[-1, 0, 1],
			[-2, 0, 2],
			[-1, 0, 1]
		] );





	# applique le filtre de "convolution" sur l'image #
	###################################################
	# @param pixelMap		la matrice de pixels à modifier
	#
	# @history
	#			applique le filtre
	def Convolution(self, pixelMap, kernel=None):
		width  = len( pixelMap[0] )
		height = len( pixelMap    )

		if kernel == None:
			print "no kernel given!"
			exit()

		# nb total résultant du kernel des valeurs positives
		kernelFactor = 0;
		for b in kernel:
			for a in b:
				if a > 0:
					kernelFactor += a;

		kMidWidth  = len( kernel[0] ) // 2
		kMidHeight = len( kernel    ) // 2

		# map de résultat (filtrée)
		convolvedMap = []

		# on parcourt tout les pixels
		for y in range(0, height):

			# on rajoute une ligne à la map filtrée
			convolvedMap.append( [] )

			for x in range(0, width):

				pixel = pixelMap[y][x];

				# on définit la matrice de même taille que le kernel mais correspondant aux pixels superposés
				pixelM = [];

				for b in range(-kMidHeight, 1+kMidHeight):
					pixelM.append( [] );
					for a in range(-kMidWidth, 1+kMidWidth):
						# on met les valeurs entre 0 et longueur ou largeur pour pas récupérer les valeurs de l'autre côté (lissage bizarre)
						ruledX = 0 if x+a<0 else width-1  if x+a>=width  else x+a;
						ruledY = 0 if y+b<0 else height-1 if y+b>=height else y+b;
						
						# if x+a<0 or x+a>=width or y+b<0 or y+b>=height: # si pixel dépasse de l'image, on l'ajoute pas

						# on ajoute le pixel courant
						pixelM[len(pixelM)-1].append( pixelMap[ruledY][ruledX] );

				r,g,b = 0,0,0

				# on effectue la convolution
				for linePixelM, lineKernel in zip(pixelM, kernel):
					for pix, fact in zip(linePixelM, lineKernel):
						# pour chacun des filtres
						r += pix.r * fact
						g += pix.g * fact
						b += pix.b * fact

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

















