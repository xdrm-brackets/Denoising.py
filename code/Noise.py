# ~*~ encoding: utf-8 ~*~ #

import random

class Noise:


	# ajout de bruit "poivre & sel" avec un seuil (% de l'image bruité)
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


	# enlève le bruit "poivre et sel"
	def SaltAndPepper_unset(self, pixelMap, seuil=5, borne=5):
		width  = len( pixelMap[0] )
		height = len( pixelMap    )

		while seuil >= 1:
			seuil /= 100.0

		while borne >= 100:
			borne /= 100.0

		seuil = int( seuil * 256 );

		for y in range(0, len(pixelMap)):
			for x in range(0, len(pixelMap[y])):
				pMoy = ( pixelMap[y][x].r + pixelMap[y][x].g + pixelMap[y][x].b ) / 3
				# traitement si couleur extreme
				if pMoy >= 255-borne or pMoy <= borne:
					xmin, ymin, xmax, ymap = x, y, x, y;
					rMoy, gMoy, bMoy, count = 0.0, 0.0, 0.0, 0 # moyennes des couleurs
					rInterval, gInterval, bInterval, rgbInterval = 0, 0, 0, 0  # décalage avec le pixel

					if y-1 > -1:
						ymin = y-1
					if y+1 < height:
						ymax = y+1
					if x-1 > -1:
						xmin = x-1
					if x+1 < width:
						xmax = x+1


					# pixels = [ pixelMap[y][xmin], pixelMap[y][xmax], pixelMap[ymin][x], pixelMap[ymax][x] ];
					# for p in pixels:
					# 	if p != pixelMap[y][x]:
					# 		rMoy += p.r;
					# 		gMoy += p.g;
					# 		bMoy += p.b;
					# 		count += 1

					for j in pixelMap[ymin:ymax]: # on parcourt les pixels autour
						for pix in j[xmin:xmax]:
							# calcul de la moyenne autour du pixel
							if pix != pixelMap[y][x]:
								rMoy  += pix.r;
								gMoy  += pix.g;
								bMoy  += pix.b;
								count += 1

					if count > 0:
						rMoy = int( rMoy / count )
						gMoy = int( gMoy / count )
						bMoy = int( bMoy / count )

						rInterval = abs( pixelMap[y][x].r - rMoy )
						gInterval = abs( pixelMap[y][x].g - gMoy )
						bInterval = abs( pixelMap[y][x].b - bMoy )

						rgbInterval = ( rInterval + gInterval + bInterval ) / 3

						# si la couleur est trop "différente" alors on remplace sa couleur par la moyenne des couleurs alentours
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