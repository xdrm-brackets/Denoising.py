# ~*~ encoding: utf-8 ~*~ #

class Noise:

	def getShape( x, y, map, pixelList ): # return PixelList
		width  = len( map[0] )	
		height = len( map    )


		# si le pixel existe (pas de dépassement de la map)
		if x < width and y < height:

			already = False;
			for i in range(0, len(pixelList)):
				if pixelList[i] == map[y][x]:
					already = True;
					break

			# si le pixel n'est pas déjà dans le tableau
			if not already:
				
				pixelList.append( map[y][x] ) # ajout au tableau

				getShape(x-1, y+1, map, pixelList) # 1
				getShape(x, y+1, map, pixelList)   # 2
				getShape(x+1, y+1, map, pixelList) # 3

				getShape(x-1, y, map, pixelList)   # 4
				# current pixel
				getShape(x+1, y, map, pixelList)   # 6

				getShape(x-1, y-1, map, pixelList) # 7
				getShape(x, y-1, map, pixelList)   # 8
				getShape(x+1, y-1, map, pixelList) # 9
			