# ~*~ encoding: utf-8 ~*~ #

import random
import time


class Shape:
	# récupère la forme complète autour du pixel donné #
	####################################################
	# @param originalPixel		pixel de base
	# @param pixelMap 			matrice de pixels
	# @param seuil				Ecart entre le pixel et ses alentours à partir duquel on considère un contour ou une continuité de la forme
	#
	# @return					retourne la liste des pixels composant la forme (références)
	#
	def get(self, originalPixel, pixelMap, seuil=10):
		width  = len( pixelMap[0] )
		height = len( pixelMap    )

		shape     = []                  # contiendra les pixels de la forme
		waiting   = [originalPixel]     # contient les pixels à traiter

		# on continue d'analyser tant qu'il y a des pixels à traiter
		while len(waiting) > 0:
			pixel = waiting[0]

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
						if not( currentP in shape or currentP in waiting): 
							waiting.append( currentP )

			
			# on retire le pixel de la liste d'attente
			try:
				waiting.remove( pixel )
			except:
				pass

		return shape;