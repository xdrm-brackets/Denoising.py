# ~*~ Encoding: utf-8 ~*~ #

class RGBPixel:

	def __init__(self, r, g, b, x, y):
		self.r = r;
		self.g = g;
		self.b = b;
		self.x = x;
		self.y = y;

	def setRGBPixel(self, r, g, b, x, y):
		self.__init__(r, g, b, x, y);

	def setRGB(self, r, g, b):
		self.r = r;
		self.g = g;
		self.b = b;

	def setXY(self, x, y):
		self.x = x;
		self.y = y;

	def toString(self):
		return 'rgb(%s, %s, %s)' % (self.r, self.g, self.b);

	def toString_grayscale(self):
		return (self.r+self.g+self.b) // 3;
















def printRGBMatrix(m):
	for line in m:
		print '|',
		for row in line:
			print '%s |' % ( row.toString_grayscale() ),
		print;

def printMatrix(m):
	for line in m:
		print '|',
		for row in line:
			print '%s |' % ( row ),
		print;




















# applique le filtre de "convolution" sur l'image #
###################################################
# @param pixelMap		la matrice de pixels à modifier
#
# @history
#			applique le filtre
def Convolution(pixelMap, kernel=None):
	width  = len( pixelMap[0] )
	height = len( pixelMap    )

	if kernel == None:
		print "no kernel given!"
		exit()

	# nb total résultant du kernel des valeurs positives
	kernelFactor = 0;
	for b in kernel:
		for a in b:
			if a > 0:
				kernelFactor += a;

	kMidWidth  = len( kernel[0] ) // 2
	kMidHeight = len( kernel    ) // 2

	# map de résultat (filtrée)
	convolvedMap = []

	# on parcourt tout les pixels
	for y in range(0, height):

		# on rajoute une ligne à la map filtrée
		convolvedMap.append( [] )

		for x in range(0, width):

			pixel = pixelMap[y][x];

			# on définit la matrice de même taille que le kernel mais correspondant aux pixels superposés
			pixelM = [];

			for b in range(-kMidHeight, 1+kMidHeight):
				pixelM.append( [] );
				for a in range(-kMidWidth, 1+kMidWidth):
					# on met les valeurs entre 0 et longueur ou largeur pour pas récupérer les valeurs de l'autre côté (lissage bizarre)
					ruledX = 0 if x+a<0 else width-1  if x+a>=width  else x+a;
					ruledY = 0 if y+b<0 else height-1 if y+b>=height else y+b;
					
					if x+a<0 or x+a>=width or y+b<0 or y+b>=height: # si pixel dépasse de l'image, on l'ajoute pas

					# on ajoute le pixel courant
						pixelM[len(pixelM)-1].append( pixelMap[ruledY][ruledX] );

			r,g,b = 0,0,0

			# on effectue la convolution
			for linePixelM, lineKernel in zip(pixelM, kernel):
				for pix, fact in zip(linePixelM, lineKernel):
					# pour chacun des filtres
					r += pix.r * fact
					g += pix.g * fact
					b += pix.b * fact

					print '(%s) * %s' % ( pix.r, fact );
				print;


			r = int(r/kernelFactor) % 256
			g = int(g/kernelFactor) % 256
			b = int(b/kernelFactor) % 256


			# définition des couleurs sur la map filtrée
			convolvedMap[y].append( RGBPixel(
				r   = r,
				g   = g,
				b   = b,
				x   = x,
				y   = y
			) )
	
	return convolvedMap







# on définit une matrice de base
pixelSample = [ RGBPixel(50, 50, 50, 0, 0),
				RGBPixel(100, 100, 100, 0, 0) ];



# on définit la matrice 10x5
matrix50 = [];

for y in range(0,3):
	matrix50.append( [] );
	for x in range(0,3):
		pixelSample[(x+y*3)%2].setXY(x, y);
		matrix50[y].append( pixelSample[(x+y*5)%2] );

# on l'affiche
printRGBMatrix(matrix50);print;



# on définit le noyau 3x3
k = [ [1, 1, 1],
	  [1, 0, 1], 
	  [1, 1, 1] ];

# on l'affiche
printMatrix(k);print;

matrix50Convolved = Convolution(matrix50, k);

printRGBMatrix(matrix50Convolved);print;
printRGBMatrix(matrix50);print;