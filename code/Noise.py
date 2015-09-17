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
	def SaltAndPepper_unset(self, pixelMap, seuil=10, borne=20):
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
					




	def getShapeRecursive(self, coords, pixelMap, pixelList ): # return PixelList
		# coords = [lastx, lasty, x, y]
		width  = len( pixelMap[0] )	
		height = len( pixelMap    )

		lastx = coords[0]
		lasty = coords[1]
		x     = coords[2]
		y     = coords[3]

		newCoords = [x, y]


		# si le pixel existe (pas de dépassement de la pixelMap)
		if x<width and x>=0 and y<height and y>=0:

			already = False;
			for i in range(0, len(pixelList)):
				if pixelList[i] == pixelMap[y][x]:
					already = True;
					break

			# si le pixel n'est pas déjà dans le tableau
			if not already:

				pixelMap[y][x].setRGB(255,0,0);

				# si trop de différence
				lastP = pixelMap[lasty][lastx]
				pix   = pixelMap[y][x]



				if abs(lastP.r-pix.r) <= 50 and abs(lastP.g-pix.g) <= 50 and abs(lastP.b-pix.b) <= 50:

					pixelList.append( pixelMap[y][x] ) # ajout au tableau

					self.getShapeRecursive( [x, y, x-1, y+1], pixelMap, pixelList) # 1
					self.getShapeRecursive( [x, y, x,   y+1], pixelMap, pixelList) # 2
					self.getShapeRecursive( [x, y, x+1, y+1], pixelMap, pixelList) # 3

					self.getShapeRecursive( [x, y, x-1, y ],  pixelMap, pixelList) # 4
					# current pixel
					self.getShapeRecursive( [x, y, x+1, y ],  pixelMap, pixelList) # 6

					self.getShapeRecursive( [x, y, x-1, y-1], pixelMap, pixelList) # 7
					self.getShapeRecursive( [x, y, x,   y-1], pixelMap, pixelList) # 8
					self.getShapeRecursive( [x, y, x+1, y-1], pixelMap, pixelList) # 9

	
	def getShape(self, coords, pixelMap, pixelList):
		# coords = [lastx, lasty, x, y]
		width  = len( pixelMap[0] )	
		height = len( pixelMap    )
		
		lastx = coords[0]
		lasty = coords[1]
		x     = coords[2]
		y     = coords[3]

		if x<width and x>=0 and y<height and y>=0:

			already = False;
			for pix in pixelList:
				if pix == pixelMap[y][x]:
					already = True;
					break

			# si le pixel n'est pas déjà dans le tableau
			if not already:

				# si trop de différence
				lastP = pixelMap[lasty][lastx]
				pix   = pixelMap[y][x]

				if abs(lastP.r-pix.r) <= 50 and abs(lastP.g-pix.g) <= 50 and abs(lastP.b-pix.b) <= 50:

					return pixelMap[y][x];

				# self.getShape( [x, y, x-1, y+1], pixelMap, pixelList) # 1
				# self.getShape( [x, y, x,   y+1], pixelMap, pixelList) # 2
				# self.getShape( [x, y, x+1, y+1], pixelMap, pixelList) # 3

				# self.getShape( [x, y, x-1, y ],  pixelMap, pixelList) # 4
				# # current pixel
				# self.getShape( [x, y, x+1, y ],  pixelMap, pixelList) # 6

				# self.getShape( [x, y, x-1, y-1], pixelMap, pixelList) # 7
				# self.getShape( [x, y, x,   y-1], pixelMap, pixelList) # 8
				# self.getShape( [x, y, x+1, y-1], pixelMap, pixelList) # 9

		return None # return none si le pixel n'est plus de la forme