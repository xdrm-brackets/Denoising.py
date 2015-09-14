# ~*~ encoding: utf-8 ~*~ #

import random

class Noise:


	def SaltAndPepper_set(self, seuil, pixelMap):
		seuil = float(seuil);

		while seuil >= 1:
			seuil /= 100

		nbPixel = int( len(pixelMap) * len(pixelMap[0]) * seuil )

		for bruit in range(0, nbPixel ):
			x = random.randint(0, len(pixelMap[0]) - 1 )
			y = random.randint(0, len(pixelMap)    - 1 )

			if random.randint(0,1) == 1:
				pixelMap[y][x].setRGB(255,255,255);
			else:
				pixelMap[y][x].setRGB(0,0,0);












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

				# si trop de différence
				lastP = pixelMap[lasty][lastx]
				pix   = pixelMap[y][x]



				if abs(lastP.r-pix.r) <= 50 and abs(lastP.g-pix.g) <= 50 and abs(lastP.b-pix.b) <= 50:

					pixelList.append( pixelMap[y][x] ) # ajout au tableau

					self.getShape( [x, y, x-1, y+1], pixelMap, pixelList) # 1
					self.getShape( [x, y, x,   y+1], pixelMap, pixelList) # 2
					self.getShape( [x, y, x+1, y+1], pixelMap, pixelList) # 3

					self.getShape( [x, y, x-1, y ],  pixelMap, pixelList) # 4
					# current pixel
					self.getShape( [x, y, x+1, y ],  pixelMap, pixelList) # 6

					self.getShape( [x, y, x-1, y-1], pixelMap, pixelList) # 7
					self.getShape( [x, y, x,   y-1], pixelMap, pixelList) # 8
					self.getShape( [x, y, x+1, y-1], pixelMap, pixelList) # 9
	
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