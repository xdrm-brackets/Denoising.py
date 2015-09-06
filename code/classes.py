# ~*~ encoding: utf-8 ~*~ #

import sys

#################################################
# classe qui parse le header (binaire) en objet #
#################################################
class BMPHeader:
	
	# CONSTRUCTEUR: initialise les variables
	def __init__(self):
		self.header    = 0; # header brut (format initial: bin)
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

	# convertit les octets <bytes> en entier
	def toInt(self, bytes):
		intReturn = 0;
		for i, byte in enumerate(bytes):
			intReturn += ord(byte) * (256 ** i)
		return intReturn
	
	# parse le header au format bin en objet
	def parse(self, binHeader):
		self.header    = binHeader                    # header brut (format initial: bin)
		self.signature = self.toInt(binHeader[ 0: 2]) # signature (4D42)
		self.fileSize  = self.toInt(binHeader[ 2: 6]) # taille du fichier bmp (bytes)
		self.offset    = self.toInt(binHeader[10:14]) # début de l'image (bytes)
		self.infoSize  = self.toInt(binHeader[14:18]) # taille du INFO_HEADER
		self.width     = self.toInt(binHeader[18:22]) # longueur de l'image (pixel)
		self.height    = self.toInt(binHeader[22:26]) # hauteur de l'image (pixel)
		self.plans     = self.toInt(binHeader[26:28]) # nombre de plans (default: 1)
		self.bpp       = self.toInt(binHeader[28:30]) # nombre de bits par pixel (1,4,8, 24)
		self.compType  = self.toInt(binHeader[30:34]) # type de compression (0=none, 1=RLE-8, 2=RLE-4)
		self.size      = self.toInt(binHeader[34:38]) # taille de l'image avec padding (bytes)
		self.horiRes   = self.toInt(binHeader[38:42]) # résolution horizontale (pixels)
		self.vertRes   = self.toInt(binHeader[42:46]) # résolution verticale (pixels)
		self.colorNb   = self.toInt(binHeader[46:50]) # nombre de couleurs de l'image (ou 0)
		self.colorINb  = self.toInt(binHeader[50:54]) # nombre d'images importantes (ou 0)
		
	
	# Affiche au format humain, toutes les infos du header
	def info(self):
		print "INFORMATION DU HEADER"
		print "====================="	
		print "signature:         %s" % ( hex(self.signature) )
		print "taille du fichier: %s" % ( hex(self.fileSize ) )
		print "offset du contenu: %s" % ( hex(self.offset   ) )
		print "taille infoHeader: %s" % ( hex(self.infoSize ) )
		print "largeur:           %s" % ( hex(self.width    ) )
		print "hauteur:           %s" % ( hex(self.height   ) )
		print "nombre de plans:   %s" % ( hex(self.plans    ) )
		print "bits par pixel:    %s" % ( hex(self.bpp      ) )
		print "type compression:  %s" % ( hex(self.compType ) )
		print "taille(+padding):  %s" % ( hex(self.size     ) )
		print "horizontal resol:  %s" % ( hex(self.horiRes  ) )
		print "vertical resol:    %s" % ( hex(self.vertRes  ) )
		print "nombre de couleur: %s" % ( hex(self.colorNb  ) )
		print "nb couleurs impor: %s" % ( hex(self.colorINb ) )
		print "====================="
		print

####################################################
# classe qui parse le content (binaire) en matrice #		
####################################################
class BMPContent:
	
	# CONSTRUCTEUR: parse le content (bin) <binContent> avec les informations:
	#	<header>	BMPHeader de l'image en question
	def __init__(self, binContent, header):
		# gestion du bpp
		if( header.bpp != 24 ):
			print "ne prends pas en charge les versions autre que bmp24";
			exit
		
		# taille avec un padding de 1
		correctSizes = [
			( header.width * ( 1 +header.bpp/8 ) ) * header.height, # padding de 1
			( header.width * ( 2 + header.bpp/8 ) ) * header.height # padding de 2
		]
		
		# si le fichier a une mauvaise taille donc mauvais format
		padding = 0
		if not len(binContent) in correctSizes:
			print "Mauvais format"
			exit
		elif len(binContent) == correctSizes[0]:
			padding = 1
		else:
			padding = 2

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
			
			i += padding # on saute le padding de saut de ligne				
			
		self.map = self.map[::-1] # on inverse les lignes
			
			
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
	# CONSTRUCTEUR #
	# à partir du fichier <filename>
	# parse le header dans une classe <BMPHeader>
	# parse le contenu dans une classe <BMPContent>
	def __init__(self, filename):
		# gestion du format
		if not ".bmp" in filename[-4:]:
			print "must be a .bmp file"
			exit
			
		self.fileData = ""
		self.readableData = ""
		with open(sys.argv[1]) as file:
			for byte in file.read():
				self.fileData += byte;
				self.readableData += str(hex(ord(byte))) + " "
				
		headerSize = 54
		self.header  = BMPHeader()
		self.header.parse( self.fileData[:headerSize] )
		self.content = BMPContent( self.fileData[self.header.offset:], self.header )