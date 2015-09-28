# ~*~ encoding: utf-8 ~*~ #

import random
import time

# import des libs internes
from utility import SaltAndPepper_Noise, Additive_Noise, Multiplicative_Noise, Color_Noise, Gaussian_Noise
from utility import Filter, Shape

from BMPFile import RGBPixel




class Noise:
	
	# instanciation des classes qui sont dans utility/
	def __init__(self):	
		self.SaltAndPepper  = SaltAndPepper_Noise.SaltAndPepper_Noise();
		self.Additive       = Additive_Noise.Additive_Noise();
		self.Multiplicative = Multiplicative_Noise.Multiplicative_Noise();
		self.Gaussian       = Gaussian_Noise.Gaussian_Noise();
		self.Color          = Color_Noise.Color_Noise();

		self.Filter         = Filter.Filter();
		self.Shape          = Shape.Shape();

	# retourne le SNR d'une image bruitée par rapport à sa référence
	# @param uRef					matrice de pixels de l'image d'origine
	# @param uNoisy					matrice de pixels de l'image bruitée
	#
	# @return SNR 					retourne le SNR associé
	#
	def SNR(self, uRef, uNoisy, grayscale=True):
		width  = len( uRef[0] )
		height = len( uRef    )

		# si les images n'ont pas les mêmes tailles
		if len(uNoisy) != height or len(uNoisy[0]) != width:
			print "Tailles différentes";
			exit();

		# on calcule la puissance du signal
		P_uRef = self.Power( uRef ) if not grayscale else self.Power_grayscale( uRef )

		# on calcule la matrice de  = l'image bruitée - l'image d'origine = le bruit uniquement
		uNoise = []

		# pour chaque pixel
		for lineNoisy, lineRef in zip(uNoisy, uRef):

			uNoise.append( [] );
			
			for pixNoisy, pixRef in zip(lineNoisy, lineRef):
				uNoise[pixRef.y].append( RGBPixel(
						r   = 0 if pixNoisy.r-pixRef.r < 0 else pixNoisy.r-pixRef.r, # on tronque à 0 si négatif
						g   = 0 if pixNoisy.g-pixRef.g < 0 else pixNoisy.g-pixRef.g, # on tronque à 0 si négatif
						b   = 0 if pixNoisy.b-pixRef.b < 0 else pixNoisy.b-pixRef.b, # on tronque à 0 si négatif
						x   = pixRef.x,
						y   = pixRef.y,
						bpp = pixRef.bpp,
				) )


		# on calcule la puissance du bruit
		P_uNoise = self.Power( uNoise ) if not grayscale else self.Power_grayscale( uNoise )

		if P_uNoise == 0:
			return 0;
		else:
			return 1.0 * P_uRef / P_uNoise;




	# retourne la puissance d'une image (somme du carré de ses valeurs) teinte de gris
	# @param pixelMap				matrice de pixels de l'image de laquelle on veut la puissance
	#
	# @return power 				puissance de l'image
	#
	def Power_grayscale(self, pixelMap):
		power = 0;

		for line in pixelMap:
			for pix in line:
				power += pix.grayscale() ** 2

		return power;


	# retourne la puissance d'une image (somme du carré de ses valeurs) teinte de gris
	# @param pixelMap				matrice de pixels de l'image de laquelle on veut la puissance
	#
	# @return power 				puissance de l'image
	#
	def Power(self, pixelMap):
		power = 0;

		for line in pixelMap:
			for pix in line:
				power += pix.r ** 2 + pix.g ** 2 + pix.b ** 2

		return power;