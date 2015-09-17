# ~*~ encoding: utf-8 ~*~ #

import random

class Noise:


	# Applique le bruitage de type "Poivre & Sel" sur la matrice de pixels #
	########################################################################
	# @param pixelMap 		Matrice de pixel à traiter (modifier)
	# @param seuil			pourcentage de l'image à bruiter (50% <=> 1 pixel sur 2 est bruité) 
	#
	def SaltAndPepper_set(self, pixelMap, seuil=10):
		seuil = float(seuil);

		while seuil >= 1:
			seuil /= 100.0

		nbPixel = int( len(pixelMap) * len(pixelMap[0]) * seuil )

		for bruit in range(0, nbPixel ):
			x = random.randint(0, len(pixelMap[0]) - 1 )
			y = random.randint(0, len(pixelMap)    - 1 )

			if random.randint(0,1) == 1:
				pixelMap[y][x].setRGB(255,255,255);
			else:
				pixelMap[y][x].setRGB(0,0,0);


	# Applique le débruitage de type "Poivre & Sel" sur la matrice de pixels #
	##########################################################################
	# @param pixelMap 		Matrice de pixel à traiter (modifier)
	# @param seuil			Seuil à partir duquel on doit traiter les pixels (écart entre la moyenne des pixels avoisinant et le pixel concerné)
	# @param borne			0 = Noir pur et blanc pur sont enlevés; 255 ou + = tout les pixels sont traités 
	#
	def SaltAndPepper_unset(self, pixelMap, seuil=5, borne=5):
		width  = len( pixelMap[0] )
		height = len( pixelMap    )

		if seuil < 0 or seuil > 255: # si le seuil est incohérent  => valeur par défaut (5)
			seuil = 5;

		if borne < 0 or borne > 255: # si la borne est incohérente => valeur par défaut (5)
			borne = 5;


		# on parcourt tout les pixels
		for y in range(0, len(pixelMap)):
			for x in range(0, len(pixelMap[y])):

				# on calcule la moyenne des valeurs R G B du pixel courant
				pMoy = ( pixelMap[y][x].r + pixelMap[y][x].g + pixelMap[y][x].b ) / 3

				# si couleur proche du blanc ou noir (en fonction de la borne)
				if pMoy >= 255-borne or pMoy <= borne:
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


					# pixels = [ pixelMap[y][xmin], pixelMap[y][xmax], pixelMap[ymin][x], pixelMap[ymax][x] ];
					# for p in pixels:
					# 	if p != pixelMap[y][x]:
					# 		rMoy += p.r;
					# 		gMoy += p.g;
					# 		bMoy += p.b;
					# 		count += 1

					# on parcourt le carré de 3x3
					for j in pixelMap[ymin:ymax]:
						for pix in j[xmin:xmax]:

							# si le pixel n'est pas le pixel courant (mais ceux autour)
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
							pixelMap[y][x].setRGB(rMoy, gMoy, bMoy);
					











































	def AdditiveNoise_set(self, pixelMap, seuil=10):
		seuil = float(seuil);

		while seuil >= 1:
			seuil /= 100.0

		nbPixel = int( len(pixelMap) * len(pixelMap[0]) * seuil )

		for bruit in range(0, nbPixel ):
			x = random.randint(0, len(pixelMap[0]) - 1 )
			y = random.randint(0, len(pixelMap)    - 1 )

			

			if random.randint(0,1) == 1:
				maxColor = max(pixelMap[y][x].r, pixelMap[y][x].g, pixelMap[y][x].b)
				randomAdd = random.randint(0, (255-maxColor) / 10 )
			else:
				minColor = min(pixelMap[y][x].r, pixelMap[y][x].g, pixelMap[y][x].b)
				randomAdd = - random.randint(0, minColor / 10 )

			pixelMap[y][x].setRGB(
				pixelMap[y][x].r + randomAdd,
				pixelMap[y][x].g + randomAdd,
				pixelMap[y][x].b + randomAdd
			);

	def AdditiveNoise_unset(self, pixelMap, seuil=5):
		pass






























	def MultiplicativeNoise_set(self, pixelMap, seuil=10):
		seuil = float(seuil);

		while seuil >= 1:
			seuil /= 100.0

		nbPixel = int( len(pixelMap) * len(pixelMap[0]) * seuil )

		for bruit in range(0, nbPixel ):
			x = random.randint(0, len(pixelMap[0]) - 1 )
			y = random.randint(0, len(pixelMap)    - 1 )

			

			if random.randint(0,1) == 1:
				maxColor = max(pixelMap[y][x].r, pixelMap[y][x].g, pixelMap[y][x].b)
				randomAdd = random.randint(0, (255-maxColor) / 10 )
			else:
				minColor = min(pixelMap[y][x].r, pixelMap[y][x].g, pixelMap[y][x].b)
				randomAdd = - random.randint(0, minColor / 10 )

			pixelMap[y][x].setRGB(
				pixelMap[y][x].r + randomAdd,
				pixelMap[y][x].g + randomAdd,
				pixelMap[y][x].b + randomAdd
			);

	def MultiplicativeNoise_unset(self, pixelMap, seuil=5):
		pass


















































	def ColorNoise_set(self, pixelMap, seuil=10):
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

	def ColorNoise_unset(self, pixelMap, seuil=5):
		pass








































	def Gaussian_set(self, pixelMap, seuil=10):
		pass

	def Gaussian_unset(self, pixelMap, seuil=5):
		pass