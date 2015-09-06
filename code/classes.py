# ~*~ encoding: utf-8 ~*~ #


#################################################
# classe qui parse le header (binaire) en objet #
#################################################
class BMPHeader:
	
	# convertit les octets <bytes> en entier
	def toInt(self, bytes):
		intReturn = 0;
		for i, byte in enumerate(bytes):
			intReturn += ord(byte) * (256 ** i)
		return intReturn
	
	# CONSTRUCTEUR: parse le header au format bin en objet
	def __init__(self, binHeader):
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
		self.header    = binHeader


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
		
		# si le fichier a une mauvaise taille donc mauvais format
		if len(binContent) != (2 + header.width * header.bpp/8 ) * header.height:
			print "Mauvais format"
			exit

		
		
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
			
			i += 2 # on saute le padding de saut de ligne				
			
		self.map = self.map[::-1] # on inverse les lignes
			
			
#################################
# classe contenant un pixel RGB #
#################################
class RGBPixel:
	def __init__(self, r, g, b):
		self.r = r
		self.g = g
		self.b = b
	
	def set(self, r, g, b):
		self.r = r
		self.g = g
		self.b = b	