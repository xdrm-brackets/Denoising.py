# ~*~ encoding: utf-8 ~*~ #

class Noise:

	def getShape(self, coords, pixelMap, pixelList ): # return PixelList
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
			