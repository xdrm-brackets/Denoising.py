# ~*~ encoding: utf-8 ~*~ #

import random
import time

class Multiplicative_Noise:

	# Applique le bruitage de type "Multiplicatif" sur la matrice de pixels #
	#########################################################################
	# @param pixelMap 		Matrice de pixel à traiter (modifier)
	# @param seuil			pourcentage de l'image à bruiter (50% <=> 1 pixel sur 2 est bruité) 
	#
	def set(self, pixelMap, seuil=10):
		pass

	# Applique le débruitage de type "Multiplicatif" sur la matrice de pixels #
	###########################################################################
	# @param pixelMap 		Matrice de pixel à traiter (modifier)
	# @param seuil			Seuil à partir duquel on doit traiter les pixels (écart entre la moyenne des pixels avoisinant et le pixel concerné)
	#
	def unset(self, pixelMap, seuil=5):
		pass


