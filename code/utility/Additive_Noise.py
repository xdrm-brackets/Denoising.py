# ~*~ encoding: utf-8 ~*~ #

import random
import time

import sys
sys.path.append(sys.path[0]+'/..')
from BMPFile import RGBPixel

class Additive_Noise:

	# Applique le bruitage de type "Additif de Bernouilli" sur la matrice de pixels #
	#################################################################################
	# @param pixelMap 		Matrice de pixel à traiter (modifier)
	# @param seuil			pourcentage de l'image à bruiter (50% <=> 1 pixel sur 2 est bruité) 
	#
	def setBernouilli(self, pixelMap, seuil=10):
		seuil = float(seuil);

		while seuil >= 1:
			seuil /= 100.0

		nbPixel = int( len(pixelMap) * len(pixelMap[0]) * seuil )

		for bruit in range(0, nbPixel ):
			x = random.randint(0, len(pixelMap[0]) - 1 )
			y = random.randint(0, len(pixelMap)    - 1 )

			

			if random.randint(0,1) == 1:
				maxColor = max(pixelMap[y][x].r, pixelMap[y][x].g, pixelMap[y][x].b)
				randomAdd = random.randint(0, (255-maxColor) / 2 )
			else:
				minColor = min(pixelMap[y][x].r, pixelMap[y][x].g, pixelMap[y][x].b)
				randomAdd = - random.randint(0, minColor / 2 )

			pixelMap[y][x].setRGB(
				pixelMap[y][x].r + randomAdd,
				pixelMap[y][x].g + randomAdd,
				pixelMap[y][x].b + randomAdd
			);





	# Applique le bruitage de type "Additif Gaussien" sur la matrice de pixels #
	############################################################################
	# @param pixelMap 		Matrice de pixel à traiter (modifier)
	# @param seuil			pourcentage de l'image à bruiter (50% <=> 1 pixel sur 2 est bruité) 
	#
	def setGaussian(self, pixelMap, sigma=10):
		width  = len( pixelMap[0] )
		height = len( pixelMap    )

		sigma = float(sigma);

		# vérification de la cohérence de sigma
		if -255 > sigma or sigma > 255:
			print "sigma have incoherent value"
			exit();


		from numpy import random # random.rand(height,width) renvoie une matrice de flottants entre 0 et 1
		factors = random.rand(height, width)


		# on parcourt en même temps les facteurs aléatoires et la matrice de pixels
		for lineP, lineF in zip(pixelMap, factors):
			for pixel, fact in zip(lineP, lineF):

				r = int( pixel.r + sigma * fact )
				g = int( pixel.g + sigma * fact )
				b = int( pixel.b + sigma * fact )	

				# on attribue les valeurs aux pixels
				pixel.setRGB(
					r = 0 if r<0 else ( 255 if r > 255 else r),
					g = 0 if g<0 else ( 255 if g > 255 else g),
					b = 0 if b<0 else ( 255 if b > 255 else b)
				);



	# Applique le débruitage de type "Additif" sur la matrice de pixels #
	#####################################################################
	# @param pixelMap 		Matrice de pixel à traiter (modifier)
	# @param seuil			Seuil à partir duquel on doit traiter les pixels (écart entre la moyenne des pixels avoisinant et le pixel concerné)
	#
	# @return cleanMatrix	matrice propre qui est retournée
	def unset(self, pixelMap, seuil=10):
		width  = len( pixelMap[0] )
		height = len( pixelMap    )

		# matrice qui sera retournée
		cleanMatrix = []

		if seuil < 0 or seuil > 255: # si le seuil est incohérent  => valeur par défaut (5)
			seuil = 5;


		# on parcourt tout les pixels
		for y in range(0, len(pixelMap)):
			cleanMatrix.append( [] );
			for x in range(0, len(pixelMap[y])):

				# on ajoute le pixel à la matrice "propre"
				cleanMatrix[y].append( RGBPixel(
					r = pixelMap[y][x].r,
					g = pixelMap[y][x].g,
					b = pixelMap[y][x].b,
					x = pixelMap[y][x].x,
					y = pixelMap[y][x].y,
					bpp = pixelMap[y][x].bpp,
				));

				# on calcule la moyenne des valeurs R G B du pixel courant
				pMoy = ( pixelMap[y][x].r + pixelMap[y][x].g + pixelMap[y][x].b ) / 3

				xmin, ymin, xmax, ymax = x, y, x, y;                       # les bornes ducarré 3x3 autour du pixel 
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



				# on parcourt le carré de 3x3
				for j in pixelMap[ymin:ymax+1]:
					for pix in j[xmin:xmax+1]:
						# si le pixel n'est pas le pixel courant (mais ses voisins) et que sa couleur n'est pas trop éloignée des autres
						if pix != pixelMap[y][x]:
							# calcul de la moyenne autour du pixel
							rMoy  += pix.r;
							gMoy  += pix.g;
							bMoy  += pix.b;
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
						cleanMatrix[y][x].setRGB(rMoy, gMoy, bMoy);

		return cleanMatrix;





	# Applique le débruitage de type "Additif" sur la matrice de pixels #
	#####################################################################
	# @param pixelMap 		Matrice de pixel à traiter (modifier)
	# @param seuil			Seuil de "poids statistique" à partir duquel on doit traiter les pixels compris entre 0 et 100
	#
	# @return cleanMatrix	matrice propre qui est retournée
	def unset2(self, pixelMap, seuil=10):
		width  = len( pixelMap[0] )
		height = len( pixelMap    )
		ordre  = 3 # ordre matrice carré
		ordreN = (ordre**2 - 1)/2

		# matrice qui sera retournée
		cleanMatrix = []

		while seuil >= 1: # si le seuil n'est pas un pourcentage, on le met en pourcentage
			seuil /= 100.0;

		seuil *= 256 * ordreN



		# on parcourt tout les pixels
		for y in range(0, len(pixelMap)):
			cleanMatrix.append( [] );
			for x in range(0, len(pixelMap[y])):

				# on ajoute le pixel à la matrice "propre"
				cleanMatrix[y].append( RGBPixel(
					r = pixelMap[y][x].r,
					g = pixelMap[y][x].g,
					b = pixelMap[y][x].b,
					x = pixelMap[y][x].x,
					y = pixelMap[y][x].y,
					bpp = pixelMap[y][x].bpp,
				));

				# on calcule la moyenne des valeurs R G B du pixel courant
				pMoy = ( pixelMap[y][x].r + pixelMap[y][x].g + pixelMap[y][x].b ) / 3

				xmin, ymin, xmax, ymax = x, y, x, y;                       # les bornes ducarré 3x3 autour du pixel 
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



				# contiendra la matrice M' des poids statistiques
				neighboursAbsoluteDiff = []

				# on parcourt le carré de 3x3
				for j in pixelMap[ymin:ymax+1]:
					for pix in j[xmin:xmax+1]:
						# si le pixel n'est pas le pixel courant (mais ses voisins) et que sa couleur n'est pas trop éloignée des autres
						if pix != pixelMap[y][x]:
							# calcul de la moyenne autour du pixel
							rMoy  += pix.r;
							gMoy  += pix.g;
							bMoy  += pix.b;
							count += 1
							# ajout aux poids statistiques
							neighboursAbsoluteDiff.append( abs( (pix.r+pix.g+pix.b)/3 - pMoy ) );

				# on garde que la moitié la plus petite
				statisticWeight = 0;

				neighboursAbsoluteDiff.sort() # on trie la liste

				# on récupère la somme de la moitié des éléments les plus petits (car triée)
				for infVal in range(0, ordreN):
					if infVal >= len(neighboursAbsoluteDiff): # si liste vide on arrête
						break;
					statisticWeight += neighboursAbsoluteDiff[infVal] # on effectue la somme


				# si il y a au moins un pixel autour (normalement tjs mais évite l'erreur div par zéro)
				if count > 0:
					# on calcule les moyennes somme(xi) / n
					rMoy = int( rMoy / count )
					gMoy = int( gMoy / count )
					bMoy = int( bMoy / count )

					# si la couleur est trop "différente" (dépend du seuil) alors on remplace sa couleur par la moyenne des couleurs alentours
					if statisticWeight > seuil:
						cleanMatrix[y][x].setRGB(rMoy, gMoy, bMoy);

		return cleanMatrix;