# ~*~ encoding: utf-8 ~*~ #

import random
import time

class Color_Noise:

	# Applique le bruitage de type "coloratif" sur la matrice de pixels #
	#########################################################################
	# @param pixelMap 		Matrice de pixel à traiter (modifier)
	# @param seuil			pourcentage de l'image à bruiter (50% <=> 1 pixel sur 2 est bruité) 
	#
	def set(self, pixelMap, seuil=10):
		seuil = float(seuil);

		while seuil >= 1:
			seuil /= 100.0

		nbPixel = int( len(pixelMap) * len(pixelMap[0]) * seuil )

		for bruit in range(0, nbPixel ):
			x = random.randint(0, len(pixelMap[0]) - 1 )
			y = random.randint(0, len(pixelMap)    - 1 )

			pixelMap[y][x].setRGB(
				pixelMap[y][x].r + random.randint(0, (255-pixelMap[y][x].r)/4),
				pixelMap[y][x].g + random.randint(0, (255-pixelMap[y][x].g)/4),
				pixelMap[y][x].b + random.randint(0, (255-pixelMap[y][x].b)/4)
			);

	# Applique le débruitage de type "coloratif" sur la matrice de pixels #
	###########################################################################
	# @param pixelMap 		Matrice de pixel à traiter (modifier)
	# @param seuil			Seuil à partir duquel on doit traiter les pixels (écart entre la moyenne des pixels avoisinant et le pixel concerné)
	#
	def unset(self, pixelMap, seuil=5):
		pass


