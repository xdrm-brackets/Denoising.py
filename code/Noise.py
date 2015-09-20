# ~*~ encoding: utf-8 ~*~ #

import random
import time

# import des libs internes
from utility import SaltAndPepper_Noise, Additive_Noise, Multiplicative_Noise, Color_Noise, Gaussian_Noise
from utility import Filter, Shape

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