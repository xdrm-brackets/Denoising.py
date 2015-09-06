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
		
		
		self.map = ""
		for byte in binContent:
			self.map += str(ord(byte)) + " "
		