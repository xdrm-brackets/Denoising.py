# ~*~ encoding: utf-8 ~*~ #

#################################################
# classe qui parse le header (binaire) en objet #
#################################################
class BMPHeader:
	
	# CONSTRUCTEUR: initialise les variables
	def __init__(self):
		self.binData   = 0; # header brut (format initial: bin)
		self.intData   = 0; # header brut (format entier)

		self.signature = 0; # signature (4D42)
		self.fileSize  = 0; # taille du fichier bmp (bytes)

		self.offset    = 0; # début de l'image (bytes)
		self.infoSize  = 0; # taille du INFO_HEADER
		self.width     = 0; # longueur de l'image (pixel)
		self.height    = 0; # hauteur de l'image (pixel)
		self.plans     = 0; # nombre de plans (default: 1)
		self.bpp       = 0; # nombre de bits par pixel (1,4,8, 24)
		self.compType  = 0; # type de compression (0=none, 1=RLE-8, 2=RLE-4)
		self.size      = 0; # taille de l'image avec padding (bytes)
		self.horiRes   = 0; # résolution horizontale (pixels)
		self.vertRes   = 0; # résolution verticale (pixels)
		self.colorNb   = 0; # nombre de couleurs de l'image (ou 0)
		self.colorINb  = 0; # nombre d'images importantes (ou 0)
		
		self.rowSize   = 0; # longueur réelle d'une ligne
		self.padding   = 0; # bourrage de fin de ligne (nb de bytes)
		
	
	# parse le header au format bin en objet
	def parse(self, binHeader=""):

		# on utilise l'argument si on l'a sinon l'attribut
		if binHeader != "":
			parsingData = binHeader
		else:
			parsingData = self.binData

		self.binData   = parsingData                      # header brut (format initial: bin)
		
		self.signature = self.toInt( parsingData[ 0: 2] ) # signature (4D42)
		self.fileSize  = self.toInt( parsingData[ 2: 6] ) # taille du fichier bmp (bytes)
		# 4 empty bytes (empty value = 0)
		self.offset    = self.toInt( parsingData[10:14] ) # début de l'image (bytes)
		self.infoSize  = self.toInt( parsingData[14:18] ) # taille du INFO_HEADER
		self.width     = self.toInt( parsingData[18:22] ) # longueur de l'image (pixel)
		self.height    = self.toInt( parsingData[22:26] ) # hauteur de l'image (pixel)
		self.plans     = self.toInt( parsingData[26:28] ) # nombre de plans (default: 1)
		self.bpp       = self.toInt( parsingData[28:30] ) # nombre de bits par pixel (1,4,8, 24)
		self.compType  = self.toInt( parsingData[30:34] ) # type de compression (0=none, 1=RLE-8, 2=RLE-4)
		self.size      = self.toInt( parsingData[34:38] ) # taille de l'image avec padding (bytes)
		self.horiRes   = self.toInt( parsingData[38:42] ) # résolution horizontale (pixels)
		self.vertRes   = self.toInt( parsingData[42:46] ) # résolution verticale (pixels)
		self.colorNb   = self.toInt( parsingData[46:50] ) # nombre de couleurs de l'image (ou 0)
		self.colorINb  = self.toInt( parsingData[50:54] ) # nombre de couleurs importantes de l'images (ou 0)

		# calculated values
		self.rowSize = self.size / self.height                    # taille réelle d'une ligne (+padding)
		self.padding = self.rowSize - self.width*self.bpp/8       # bourrage (nb de bytes)


		self.intData = []
		for byte in parsingData:
			self.intData.append( ord(byte) )
	
	
	# fonction qui créer <self.binData> à partir des attributs
	def unparse(self):

		# on définit le tableau d'entier à partir des attributs
		self.intData = []

		self.fromInt( self.signature, 2) # signature
		self.fromInt( self.fileSize,  4) # taille fichier BMP
		self.fromInt( 0,              4) # 4 bytes inutilisés
		self.fromInt( self.offset,    4) # début de l'image (bytes)
		self.fromInt( self.infoSize,  4) # taille du INFO_HEADER
		self.fromInt( self.width,     4) # longueur de l'image (pixels)
		self.fromInt( self.height,    4) # hauteur de l'image (pixels)
		self.fromInt( self.plans,     2) # nombre de plans (default: 1)
		self.fromInt( self.bpp,       2) # nombre de bits par pixel (1,4,8, 24)
		self.fromInt( self.compType,  4) # type de compression 
		self.fromInt( self.size,      4) # taille de la map (matrice de pixels)
		self.fromInt( self.horiRes,   4) # résolution horizontale
		self.fromInt( self.vertRes,   4) # résolution verticale
		self.fromInt( self.colorNb,   4) # nombre de couleurs de l'image (ou 0)
		self.fromInt( self.colorINb,  4) # nombre de couleurs importantes de l'image (ou 0)

		# calculated values
		# self.rowSize = self.size / self.height                    # taille réelle d'une ligne (+padding)
		# self.padding = self.rowSize - self.width*self.bpp/8       # bourrage (nb de bytes)
		

		self.binData = ""
		for byte in self.intData:
			self.binData += chr( byte )

	# Retourne au format humain, toutes les infos du header
	def info(self, type=0): # 0 = int, 1 = hex

		returnStr = ""

		if type == 0: # si int
			def displayType(value):
				return value
		else:
			def displayType(value):
				return hex(value)

		returnStr += "\n"
		returnStr += "INFORMATION DU HEADER\n"
		returnStr += "=====================\n"	
		returnStr += "signature:         %s\n" % displayType( self.signature ) 
		returnStr += "taille du fichier: %s\n" % displayType( self.fileSize  ) 
		returnStr += "offset du contenu: %s\n" % displayType( self.offset    ) 
		returnStr += "taille infoHeader: %s\n" % displayType( self.infoSize  ) 
		returnStr += "largeur:           %s\n" % displayType( self.width     ) 
		returnStr += "hauteur:           %s\n" % displayType( self.height    ) 
		returnStr += "nombre de plans:   %s\n" % displayType( self.plans     ) 
		returnStr += "bits par pixel:    %s\n" % displayType( self.bpp       ) 
		returnStr += "type compression:  %s\n" % displayType( self.compType  ) 
		returnStr += "taille(+padding):  %s\n" % displayType( self.size      ) 
		returnStr += "horizontal resol:  %s\n" % displayType( self.horiRes   ) 
		returnStr += "vertical resol:    %s\n" % displayType( self.vertRes   ) 
		returnStr += "nombre de couleur: %s\n" % displayType( self.colorNb   ) 
		returnStr += "nb couleurs impor: %s\n" % displayType( self.colorINb  ) 
		returnStr += "=====================\n"
		returnStr += "INFORMATIONS COMP.\n"
		returnStr += "=====================\n"
		returnStr += "rowsize:           %s\n" % displayType( self.rowSize   ) 
		returnStr += "padding:           %s\n" % displayType( self.padding   ) 
		returnStr += "=====================\n"
		returnStr += "\n"

		return returnStr


	# Affiche au format humain, toutes les infos du header
	def printInfo(self, type=0): # 0 = int, 1 = hex

		if type == 0: # si int
			def displayType(value):
				return value
		else:
			def displayType(value):
				return hex(value)

		print
		print "INFORMATION DU HEADER"
		print "====================="	
		print "signature:         %s" % displayType( self.signature ) 
		print "taille du fichier: %s" % displayType( self.fileSize  ) 
		print "offset du contenu: %s" % displayType( self.offset    ) 
		print "taille infoHeader: %s" % displayType( self.infoSize  ) 
		print "largeur:           %s" % displayType( self.width     ) 
		print "hauteur:           %s" % displayType( self.height    ) 
		print "nombre de plans:   %s" % displayType( self.plans     ) 
		print "bits par pixel:    %s" % displayType( self.bpp       ) 
		print "type compression:  %s" % displayType( self.compType  ) 
		print "taille(+padding):  %s" % displayType( self.size      ) 
		print "horizontal resol:  %s" % displayType( self.horiRes   ) 
		print "vertical resol:    %s" % displayType( self.vertRes   ) 
		print "nombre de couleur: %s" % displayType( self.colorNb   ) 
		print "nb couleurs impor: %s" % displayType( self.colorINb  ) 
		print "====================="
		print "INFORMATIONS COMP."
		print "====================="
		print "rowsize:           %s" % displayType( self.rowSize   ) 
		print "padding:           %s" % displayType( self.padding   ) 
		print "====================="
		print


	# convertit les octets <bytes> en entier
	def toInt(self, bytes):
		intReturn = 0;
		for i, byte in enumerate(bytes):
			intReturn += ord(byte) * (256 ** i)
		return intReturn

	# écrit le valeur entière <value> en octet bourrés jusqu'à la taille <size> dans le tableau <intData>
	def fromInt(self, value, size):
		s = '0' + str( bin(value)[2:] )

		for byte in range(0, size):
			if s=="":
				self.intData.append( 0 )
			else:
				self.intData.append( int(s[-8:],2) )
				s = s[:-8]


		

####################################################
# classe qui parse le content (binaire) en matrice #		
####################################################
class BMPContent:
	
	# CONSTRUCTEUR: instancie les attribus
	def __init__(self):
		self.map = []
		self.binData = ""
		self.intData = []

	# parse le content (bin) <binContent> avec les informations:
	#	<header>	BMPHeader de l'image en question
	def parse(self, binContent, header):
		# gestion du bpp
		#if( header.bpp != 24 ):
		#	print "Ne prends pas en charge les versions autre que bmp24";
		#	exit()
		
		# taille avec un padding de 1
		correctSize = (header.width*header.bpp/8+header.padding) * header.height;


		# si le fichier a une mauvaise taille donc mauvais format
		if not len(binContent) == correctSize:
			print "Mauvais format (erreur de taille)"
			exit()

		# attribution de la map		
		self.map = []
		i = 0.0
		
		for line in range(0, header.height):
			self.map.append( [] ) # on créé la colonne
			
			for pixel in range(0, header.width):
				newPixel = RGBPixel(y=header.height-line-1, x=pixel)
				newPixel.setBin(binContent, header.width, header.padding, i, bpp=header.bpp)
				self.map[line].append( newPixel );
				
				i += header.bpp / 8.0 # on passe à la suite
			
			i += header.padding # on saute le padding de saut de ligne				
		
		self.map = self.map[::-1] # on inverse les lignes
		
		self.binData = binContent
		
		# human-readable data
		self.intData = []
		for byte in self.binData:
			self.intData.append( ord( byte ) )


	# unparse une map de pixels en binaire
	def unparse(self, pixelMap, palettes, headerHandler=None):

		self.map = pixelMap
		
		if not isinstance(headerHandler, BMPHeader):
			headerHandler = BMPHeader()

		if headerHandler.bpp not in [1,4,8,24]: # définition du bpp si incohérent
			headerHandler.bpp = pixelMap[0][0].bpp

		headerHandler.signature = int( 0x4D42 )
		headerHandler.offset    = 54 + len(palettes[headerHandler.bpp])  # taille header(54) + taille palette(68)
		headerHandler.infoSize  = 40                                     # valeur d'offset - 14
		headerHandler.width     = len( pixelMap[0] )                     # récupérée à partir de l'argument <map>
		headerHandler.height    = len( pixelMap    )                     # récupérée à partir de l'argument <map>
		headerHandler.plans     = 1

		headerHandler.compType  = 0
		headerHandler.horiRes   = 0
		headerHandler.vertRes   = 0
		headerHandler.colorNb   = 0
		headerHandler.colorINb  = 0

		

		# valeurs calculées
		headerHandler.rowSize     = headerHandler.width * headerHandler.bpp/8
		headerHandler.padding     = 4 - headerHandler.rowSize%4
		if headerHandler.padding == 4:
			headerHandler.padding = 0;
		headerHandler.rowSize    += headerHandler.padding
		headerHandler.size        = headerHandler.rowSize * headerHandler.height   # taille de la map (hauteur*largeur* nombre d'octets par pixel)
		headerHandler.fileSize    = headerHandler.offset + headerHandler.size      # taille du fichier BMP = offset + taille map 

		self.binData = ""
		for line in pixelMap[::-1]:
			for pixel in line:
				pixel.setRGB(pixel.r, pixel.g, pixel.b, bpp=headerHandler.bpp);
				self.binData += pixel.binData
			for zero in range(0, headerHandler.padding):
				self.binData += chr(0)

		self.intData = []
		for byte in self.binData:
			self.intData.append( ord(byte) )

		
#################################
# classe contenant un pixel RGB #
#################################
class RGBPixel:
	def __init__(self, r=0, g=0, b=0, x=-1, y=-1, bpp=24):
		if bpp not in [1,4,8,24]:
			if not hasattr(self, 'bpp'): # si l'attribut n'est pas déjà défini, alors on met la valeur par défaut
				self.bpp = 24
		else:
			self.bpp = bpp

		self.x = x
		self.y = y

		self.r = r
		self.g = g
		self.b = b


		# gestion des différents bpp
		if bpp == 1:
			self.intData = [ int( (r+g+b)/3 >= 128 )        ]
			self.binData = chr( self.intData[0] )
		elif bpp == 4:
			self.intData = [ int( 16 * ((r+g+b)/3) / 256 ) ]
			self.binData = chr( self.intData[0] )
		elif bpp == 8:
			self.intData = [ int( (r+g+b) / 3 )            ]
			self.binData = chr( self.intData[0] )
		else:
			self.intData = [ r, g, b                       ]
			self.binData = chr(g) + chr(b) + chr(r)


	def setRGB(self, r=0, g=0, b=0, x=-1, y=-1, bpp=24):
		self.__init__(r=r, g=g, b=b, x=x, y=y, bpp=bpp);
		
	def setBin(self, binData, width, padding, index, bpp=24): 
		if bpp not in [1,4,8,24]:
			if not( hasattr(self, 'bpp') and self.bpp in [1,4,8,24] ): # si l'attribut n'est pas déjà défini, alors on met la valeur par défaut
				self.bpp = 24
		else:
			self.bpp = bpp


		# il faut garder uniquement les données utiles dans binData (de i à i+bpp/8)
		firstBit = int(index) + index%1.0; # retourne le rang du premier bit (pas byte)
		lastBit = firstBit + bpp/8.0

		startByte = int( firstBit )                   # ex: pour i =29, on a: 3 octets
		startBit  = int( 8 * (firstBit-startByte) )   #                       et 5 bits

		stopByte  = int( lastBit )
		stopBit   = int( 8 * (lastBit-stopByte) )

		bytes = binData[startByte:stopByte+1]


		intArray = [ ord(x) for x in bytes ]
		binArray = [ bin(x)[2:] for x in intArray ]
		binArray = [ "0"*(8-len(binArray[x])) + binArray[x] for x in range(0, len(binArray)) ]
		binary = ""
		for byte in binArray:
			binary += byte;
		
		start = startBit
		stop  = 8*(stopByte-startByte) + stopBit

		colorValue = int( binary[start:stop] , 2 )



		# gestion des différents bpp
		if bpp == 1:
			self.intData = [ 255 * colorValue      ]
			self.r = self.intData[0]
			self.g = self.intData[0]
			self.b = self.intData[0]
		elif bpp == 4:
			self.intData = [ 256 * colorValue / 16 ]
			self.r = self.intData[0]
			self.g = self.intData[0]
			self.b = self.intData[0]
		elif bpp == 8:
			self.intData = [ colorValue            ]
			self.r = self.intData[0]
			self.g = self.intData[0]
			self.b = self.intData[0]
		else:
			red   = colorValue % 256
			green = colorValue // 256 % 256
			blue  = colorValue // 256 // 256 % 256
			self.intData = [ red, blue, green      ]
			self.r = self.intData[0]
			self.g = self.intData[1]
			self.b = self.intData[2]


		
		

####################################################
# classe qui parse un fichier BMP complet en objet #
####################################################
class BMPFile:

	# CONSTRUCTEUR: instancie les attributs
	def __init__(self):
		self.header = BMPHeader()
		self.content = BMPContent()
		self.binData = ""
		self.intData = []
		self.binPalette = ""
		self.intPalette = []

	# parse à partir de <binFile> en objets <BMPHeader> et <BMPContent>
	def parse(self, binFile=""):
		# si on a défini le fichier
		if binFile == "":
			print "<BMPFile.parse()> need an argument"
			exit()

		# human-readable data
		self.binData = binFile
		self.intData = []

		for byte in binFile:
			self.intData.append( ord(byte) )
				
		headerSize = 54

		# parsing header
		self.header  = BMPHeader()
		self.header.parse( self.binData[:headerSize] )
		
		# parsing content
		self.content = BMPContent()
		self.content.parse( self.binData[self.header.offset:], self.header )

		# création de la pallette (header complémentaire=définition des couleurs+codage)
		self.binPalette = self.binData[54:self.header.offset]
		self.intPalette = []
		for byte in self.binPalette:
			self.intPalette.append( ord(byte) )

	# unparse à partir d'un <BMPHeader> et d'un <BMPContent>
	def unparse(self, newBpp=None):

		palette = [[]]*25

		# définition des palettes par défaut
		tmp = [[x,x,x,0] for x in range(0,256)]
		palette[8] = []; palette[8] += [x for l in tmp for x in l]
		
		palette[24] = [ord("B"), ord("G"), ord("R"), ord("s")] + [0]*48 + [2] + [0]*15
		
		
		if newBpp in [1,4,8,24]: # si nouveau bpp défini
			self.header.bpp = newBpp;
		else:
			if self.header.bpp not in [1,4,8,24]:
				self.header.bpp = 24

		# on déparse les classes utilisées
		self.content.unparse( self.content.map, palette, self.header)
		self.header.unparse()

		self.intPalette = palette[self.header.bpp]

		self.binPalette = ""
		for byte in self.intPalette:
			self.binPalette += chr(byte)

		# on enregistre le contenu brut binaire du fichier complet
		self.binData = "%s%s%s" % (self.header.binData, self.binPalette, self.content.binData)

		self.intData = []
		for byte in self.binData:
			self.intData.append( ord(byte) )


	# écrit l'image dans un fichier
	def write(self, filename):
		with open(filename,"w") as file:
			file.write( self.binData );