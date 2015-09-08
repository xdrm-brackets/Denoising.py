# ~*~ encoding: utf-8 ~*~ #

import sys

#################################################
# classe qui parse le header (binaire) en objet #
#################################################
class BMPHeader:
	
	# CONSTRUCTEUR: initialise les variables
	def __init__(self):
		self.binData   = 0; # header brut (format initial: bin)
		self.intData   = 0; # header brut (format entier)
		self.hexData   = 0; # header brut (format hexadécimal)

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
				

		self.binData = ""
		for byte in self.intData:
			self.binData += chr( byte )


	# Affiche au format humain, toutes les infos du header
	def info(self, type=0): # 0 = int, 1 = hex

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
		print "rowEncoded:        %s" % displayType( self.padding   ) 
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
		self.readableData = ""

	# parse le content (bin) <binContent> avec les informations:
	#	<header>	BMPHeader de l'image en question
	def parse(self, binContent, header):
		# gestion du bpp
		if( header.bpp != 24 ):
			print "Ne prends pas en charge les versions autre que bmp24";
			exit()
		
		# taille avec un padding de 1
		correctSize = header.rowSize * header.height;
		
		# si le fichier a une mauvaise taille donc mauvais format
		if not len(binContent) == correctSize:
			print "Mauvais format (erreur de taille)"
			exit()

		# attribution de la map		
		self.map = []
		i = 0
		
		for line in range(0, header.height):
			self.map.append( [] ) # on créé la colonne
			
			for pix in range(0, header.width):
				self.map[line].append( # on ajoute le pixel à la ligne 
					RGBPixel(
						ord( binContent[i+2] ), # rouge
						ord( binContent[i+1] ), # vert
						ord( binContent[i+0] )  # bleu
					)
				);
				
				i += 3 # on passe à la suite
			
			i += header.padding # on saute le padding de saut de ligne				
		
		self.map = self.map[::-1] # on inverse les lignes
		
		self.binData = binContent
		
		# human-readable data
		self.intData = []
		for byte in self.binData:
			self.intData.append(      ord( byte )   )


	# unparse une map de pixels en binaire
	def unparse(self, map):
		self.map = map
		
		height  = len( map    ) # nb de lignes   = taille de la map
		width   = len( map[0] ) # nb de colonnes = taille des lignes de la map
		padding = ( 4 - width*3 % 4 ) % 4 # padding de bourrage de lignes
		
		self.bin = ""
		for line in self.map[::-1]:
			for pixel in line:
				self.bin += chr(pixel.b) + chr(pixel.g) + chr(pixel.r)
			for zero in range(0, padding):
				self.bin += chr(0)

		
#################################
# classe contenant un pixel RGB #
#################################
class RGBPixel:
	def __init__(self, r, g, b):
		self.r = r
		self.g = g
		self.b = b
		
		

####################################################
# classe qui parse un fichier BMP complet en objet #
####################################################
class BMPFile:

	# parse à partir de <binFile> en objets <BMPHeader> et <BMPContent>
	def parse(self, binFile=""):
		# si on a défini le fichier
		if binFile == "":
			print "<BMPFile.parse()> need an argument"
			exit()

		# human-readable data
		self.binData = binFile
		self.intData = []
		self.hexData = []

		for byte in binFile:
			self.intData.append(      ord(byte)   )
			self.hexData.append( hex( ord(byte) ) )
				
		headerSize = 54

		# parsing header
		self.header  = BMPHeader()
		self.header.parse( self.binData[:headerSize] )
		
		# parsing content
		self.content = BMPContent()
		self.content.parse( self.binData[self.header.offset:], self.header )

	# unparse à partir d'un <BMPHeader> et d'un <BMPContent>
	def unparse(self):
		print "To Do !"
		print "implement unparse function"
