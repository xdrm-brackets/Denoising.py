# ~*~ encoding: utf-8 ~*~ #

import pygame

class Drawer():

	# initialise l'image en fonction de sa taille
    def __init__(self, width, height):
        self.width  = width;
        self.height = height;
        self.screen = pygame.display.set_mode( (width, height) );
        self.count  = 0;


    # remet le compteur à zéro
    def reset(self):
        self.count = 0;


    # rafraîchit l'image
    def refresh(self):
        pygame.display.flip()


    # dessine un pixel de type RGBPixel(BMPFile)
    def setPixel(self, rgbpix):
        self.screen.set_at( (rgbpix.x, rgbpix.y), (rgbpix.r, rgbpix.g, rgbpix.b) );
        self.count = (self.count + 1) % self.width; # incrémente le compteur

        if( self.count >= self.width-1 ): # si le compteur a fait une ligne complète
        	self.refresh();             # on rafraîchi l'image

    # dessine toute la matrice
    def fill(self, matrix):
        for line in matrix:
            for pixel in line:
                self.setPixel( pixel );

        self.refresh();