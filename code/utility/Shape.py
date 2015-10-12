# ~*~ encoding: utf-8 ~*~ #

import random
import time


import sys
sys.path.append(sys.path[0]+'/..')
from BMPFile import RGBPixel


class Shape:
	# récupère la forme complète autour du pixel donné #
	####################################################
	# @param originalPixel		pixel de base
	# @param pixelMap 			matrice de pixels
	# @param seuil				Ecart entre le pixel et ses alentours à partir duquel on considère un contour ou une continuité de la forme
	#
	# @return					retourne la liste des pixels composant la forme (références)
	#
	def getShape(self, drawer, originalPixel, pixelMap, seuil=10):
		width  = len( pixelMap[0] )
		height = len( pixelMap    )

		shape     = []                  # contiendra les pixels de la forme
		waiting   = [originalPixel]     # contient les pixels à traiter

		# on continue d'analyser tant qu'il y a des pixels à traiter
		while len(waiting) > 0:
			pixel = waiting[0]
			pixel.done = True;

			drawer.setPixel( RGBPixel(
				r   = 255,
				g   = 0,
				b   = 0,
				x   = pixel.x,
				y   = pixel.y,
				bpp = pixel.bpp
			));

			# on ajoute le pixel à la forme
			shape.append( pixel )

			xm, xM = pixel.x, pixel.x # valeurs minimales et maximales de x autour du pixel
			ym, yM = pixel.y, pixel.y # valeurs minimales et maximales de y autour du pixel


			# si on est pas sur le bord gauche
			if pixel.x > 0:
				xm = pixel.x - 1

			# si on est pas sur le bord droit
			if pixel.x < width-1:
				xM = pixel.x + 1

			# si on est pas sur le bord haut
			if pixel.y > 0:
				ym = pixel.y - 1

			# si on est pas sur le bord bas
			if pixel.y < height-1:
				yM = pixel.y + 1

			

			# on parcourt les pixels alentours
			for j in range(ym, yM+1):
				for i in range(xm, xM+1):
					currentP = pixelMap[j][i]
					# si le pixel n'a pas une couleur trop éloignée du pixel central
					if abs(pixel.r-currentP.r) <= seuil and abs(pixel.g-currentP.g) <= seuil and abs(pixel.b-currentP.b) <= seuil:
						# on ajoute le pixel à la liste d'attente
						if currentP not in shape and currentP not in waiting:
						# if currentP.done == False: 
							waiting.append( currentP )

			
			# on retire le pixel de la liste d'attente
			try:
				waiting.remove( pixel )
			except:
				pass

		return shape;

	# récupère le contour dans lequel est le pixel donné #
	######################################################
	# @param originalPixel		pixel original
	# @param pixelMap 			matrice de pixels
	# @param seuil				Ecart entre le pixel et ses alentours à partir duquel on considère un contour ou une continuité de la forme
	#
	# couleur de originalPixel = forme
	# + de seuil par rapport à originalPixel = fond
	#
	# @return					retourne la liste des pixels composant le contour
	#
	def getEdges(self, originalPixel, pixelMap, seuil=10):
		width  = len( pixelMap[0] )
		height = len( pixelMap    )

		# retourne un kernel 2x2 (sur lequel on fera les traitements)
		def getKernel(pixel, pos):
			x, y = pixel.x, pixel.y
			if   pos == 0:
				return [ pixelMap[y][x], pixelMap[y][x+1], pixelMap[y+1][x], pixelMap[y+1][x+1] ]; # [pixel, autre], [autre, autre]
			elif pos == 1:
				return [ pixelMap[y][x-1], pixelMap[y][x], pixelMap[y+1][x-1], pixelMap[y+1][x] ]; # [autre, pixel], [autre, autre]
			elif pos == 2:
				return [ pixelMap[y-1][x+1], pixelMap[y-1][x], pixelMap[y][x], pixelMap[y][x+1] ]; # [autre, autre], [pixel, autre]
			elif pos == 3:
				return [ pixelMap[y-1][x-1], pixelMap[y-1][x], pixelMap[y][x-1], pixelMap[y][x] ]; # [autre, autre], [autre, pixel]

		# retourne un kernel 2x2 en fonction de la direction actuelle et de la position (changement de position)
		def flipKernel(kernel, pos, vect):
			pixel = kernel[pos];
			if pos == 0:          # si kernel de type [pixel, autre], [autre, autre]
				if vect == 0:     # si direction == 0 (vers la droite)
					return getKernel(pixel, pos+2)
				if vect == 1:     # si direction == 1 (vers le bas)
					return getKernel(pixel, pos+1)

			if pos == 1:          # si kernel de type [autre, pixel], [autre, autre]
 				if vect == 1:     # si direction == 1 (vers le bas)
 					return getKernel(pixel, pos-1)
 				if vect == 2:     # si direction == 2 (vers la gauche)
 					return getKernel(pixel, pos+2)

			if pos == 2:          # si kernel de type [autre, autre], [pixel, autre]
 				if vect == 3:     # si direction == 3 (vers le haut)
 					return getKernel(pixel, pos+1)
 				if vect == 0:     # si direction == 0 (vers la droite)
 					return getKernel(pixel, pos-2)

			if pos == 3:          # si kernel de type [autre, autre], [autre, pixel]
 				if vect == 2:     # si direction == 2 (vers la gauche)
 					return getKernel(pixel, pos-2)
 				if vect == 3:     # si direction == 3 (vers le haut)
 					return getKernel(pixel, pos-1)

 			# dans un cas non pris en charge on renvoie une liste de "0"
 			return [0,0,0,0]


		stroke  = []

		# le pixel de départ
		master = originalPixel
		slaves = [];
		nextP = None

		position  = 0; # cf. getKernel
		direction = 0; # 0 = droite, 1 = bas, 2 = gauche, 4 = haut


		# récupère les pixels
		while nextP != master:
			# on définit le kernel
			k = getKernel(master, position)

			pixel = k[position];

			# on vide la liste des esclaves
			slaves = []

			# on parcourt les pixels du kernel
			for pix in k:
				# si pixel sur même ligne ou colonne (contre le pixel maître)
				if pix.x == pixel.x or pix.y == pixel.y:
					slaves.append( pix );
			
			maybeNext = [None, 0];

			# on parcourt les esclaves
			for pix in slaves:
				# si l'esclave est quasiment de la même couleur (différence r+g+b < seuil)
				if abs(pixel.r-pix.r) <= seuil and abs(pixel.g-pix.g) <= seuil and abs(pixel.b-pix.b) <= seuil:
					if pixel.x != pix.x: # si le contour suit les x
						maybeNext = [pix, pix.x-pixel.x]
					else:                # si le contour suit les y
						maybeNext = [pix, ]



		return stroke


	# récupère les contours de chaque forme à partir de formes pleines #
	####################################################################
	# @param pixelMap 			matrice de pixels
	# @param seuil				Ecart entre le pixel et ses alentours à partir duquel on considère un contour ou une continuité de la forme
	#
	# Blanc = fond
	# Noir  = forme
	#
	# @return					retourne la liste des contours contenant chacun les pixels la composant
	#
	def getStrokes(self, pixelMap, seuil=10):
		strokeArray = []     # contiendra la liste des contours
		already     = []     # contient la liste des contours, séparés par un élément valant "0"
		stroke      = []     # contiendra les pixels du contour en cours

		# on parcourt tout les pixels
		for line in pixelMap:
			for pixel in line:
				if (pixel.r+pixel.g+pixel.b) >= 3*255/2 and pixel not in already: # si pixel ~blanc~ et pas déjà dans un contour
					# traitement de forme
					stroke = self.getEdges(pixel, pixelMap, seuil=seuil);
					already += [0] + stroke

		return strokeArray;