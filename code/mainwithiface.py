# ~*~ encoding: utf-8 ~*~ #
###########################
#   TRAITEMENT D'IMAGES   #
###########################

# classes
from BMPFile import *
from Noise import *
from tests import *

import random
import sys
from os import system as sh
import time

# test par défaut puis quitte
# defaultTest();
# exit();

# arrêt si moins de 2 arguments
if len(sys.argv) < 3:
	print "Require 2 args : \n* input image\n* output image"
	exit()




import pygtk
pygtk.require('2.0')
import gtk
from interface.Explorateur import *

class Interface:
	#DEFINITION DES EVENEMENT BOUTON
	def evnmt_quitter(self, widget, donnees = None):
		print "Evnmt delete survenu"
		gtk.main_quit()
	def evnmt_exploreur(self, widget, donnees = None):
		self.name = select_file() #stoque le nom du fichier selection dans cette variable
		self.libelle.set_label("fichier selectionne : " + self.name)

	def evnmt_refresh_text(self, widget, donnees = None):
		print "Evenement refresh"
		print self.bouton3.get_label()
		print self.diag.get_text()
		self.bouton3.set_label(self.diag.get_text())
		
	#EVENEMENT COMBOBOX
	def changed_cb(self, widget):
		print "coucou toi"
		str1 = self.get_active_text(widget)
		self.traitement_img(str1)


  	def get_active_text(self, widget):
      		modele = widget.get_model()
      		est_actif = widget.get_active()
      		if est_actif < 0:
          		return None
      		return modele[est_actif][0]
	
	#fonction qui repere l option choisit
	def traitement_img(self, str1):
		interfaceSelection(self.combo.get_active())


	def __init__(self):
		self.fen = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.fen.set_title("Traitement d image")
		self.fen.set_default_size(500, 500)
		self.fen.connect("delete_event", self.evnmt_quitter)
		
		#creation du libelle
		self.libelle = gtk.Label("Aucun fichier selectionnee")
		#creation de la zone de dialogue
		#self.diag = gtk.Entry(0)
		self.diag = gtk.Entry(0)
		self.diag.set_text("nom du fichier qui contiendra la nouvelle image")

		#Creationd  une combo box
		self.combo = gtk.combo_box_new_text()
		self.combo.set_wrap_width(4);self.combo.set_entry_text_column(1)
		self.combo.set_column_span_column(10);

		self.combo.append_text( "Traitement à effectuer:"     );
		self.combo.append_text( "*** TESTS DE FICHIER ***"     );
		self.combo.append_text( "Creation manuelle"            );
		self.combo.append_text( "Parse/Unparse"                );
		self.combo.append_text( "Afficher palette"             );
		self.combo.append_text( ""                             );
		self.combo.append_text( "*** TESTS DE BRUIT ***"       );
		self.combo.append_text( "Salt&Pepper"                  );
		self.combo.append_text( "Additif (Bernouilli)"         );
		self.combo.append_text( "Additif (Gaussien)"           );
		self.combo.append_text( ""                             );
		self.combo.append_text( "*** TESTS DE DIFFERENCES ***" );
		self.combo.append_text( "Difference en %"              );
		self.combo.append_text( "SNR (origine/bruit)"          );
		self.combo.append_text( "Difference en image"          );
		self.combo.append_text( "Fusion d'images (+)"          );
		self.combo.append_text( "Fusion d'images (-)"          );
		self.combo.append_text( ""                             );
		self.combo.append_text( "*** TESTS DE FORMES ***"      );
		self.combo.append_text( "Reveler une teinte"           );
		self.combo.append_text( "Colorer une forme"            );
		self.combo.append_text( "Colorer les formes"           );
		self.combo.append_text( "Relever les contours"         );
		self.combo.append_text( ""                             );
		self.combo.append_text( "*** TESTS DE FILTRES ***"     );
		self.combo.append_text( "Filtre moyen"                 );
		self.combo.append_text( "Laplace"                      );
		self.combo.append_text( "Roberts"                      );
		self.combo.append_text( "Prewitt"                      );
		self.combo.append_text( "Sobel"                        );
		self.combo.append_text( "Convolution"                  );
		self.combo.append_text( "bichrome"                     );
		self.combo.append_text( "Passe Haut"                   );
		self.combo.connect('changed', self.changed_cb)
		
		self.combo.set_active(0);
		#creation des boutons
		self.bouton = gtk.Button("Explorateur de fichier")
		self.bouton2 = gtk.Button("Quitter le programme")
		self.bouton3 = gtk.Button("Texte entree")



		self.bouton.connect("clicked", self.evnmt_exploreur)
		self.bouton2.connect("clicked", self.evnmt_quitter)
		self.bouton3.connect("clicked", self.evnmt_refresh_text)


		self.box  = gtk.VBox(False, 0)
		self.box1 = gtk.HBox(False, 0)
		self.box2 = gtk.HBox(False, 0)
		self.fen.add(self.box)

		#Gestion des differents elements de la fenetre
		#box 1 permet de creer deux elements sur la meme igne de box
		self.box1.pack_start(self.bouton, True, True, 0) #bouton d explorateur
		self.box1.pack_start(self.bouton2, True, True, 0)#bouton pour quitter le porogramme
		self.box.pack_start(self.box1, True, True, 0)    #ajout d une boite dans une boite
		self.box.pack_start(self.libelle, True, True, 0) #ajout du libelle contenant le chemin ou non du fichier selectionnne
		
		self.box.pack_start(self.box2, True, True, 0)
		self.box2.pack_start(self.diag, True, True, 0)
		
		self.box.pack_start(self.bouton3)

		self.box.pack_start(self.combo)

		self.bouton.show()
		self.bouton2.show()
		self.bouton3.show()
		self.libelle.show()
		self.diag.show()
		self.combo.show()
		self.box.show()
		self.box1.show()
		self.box2.show()
		self.fen.show()

	def boucle(self):
		gtk.main()


m = Interface()


################" INTERFACE "###################
def interfaceSelection(action):

	startStr = "\n+---------------------------+---------+"
	result = ""
	execTime = Timer(); execTime.reset();


	# fichier
	if   action == 2:
		w = raw_input("width  [100]: ")
		h = raw_input("height [100]: ")
		arg1, arg2 = 100, 100
		if w != "":
			arg1 = int(w)
		if h != "":
			arg2 = int(h)
		print startStr
		testManualCreation(image1, arg1, arg2)                 # teste la création d'un fichier à partir d'une matrice uniquement
	elif action == 3:
		print startStr
		result = testFileIntegrity(image1)                   # teste le PARSE/UNPARSE
	elif action == 4:
		print startStr
		result = printIntPalette(image1)                     # affiche la palette d'une image

	# bruits
	elif action == 7:
		inS  = raw_input("seuil bruitage    [50]: ")
		outS = raw_input("seuil débruitage  [1] : ")
		outB = raw_input("borne débruitage  [1] : ")
		s    = raw_input("Lissage ?        (0-1): ")
		arg1, arg2, arg3, arg4 = 50, 1, 1, 1
		if inS != "":
			arg1 = int(inS)
		if outS != "":
			arg2 = int(outS)
		if outB != "":
			arg3 = int(outB)
		if s != "":
			arg4 = int(s)
		print startStr
		testSaltAndPepper(image1, arg1, arg2, arg3, arg4)      # teste le bruitage/débruitage de type "Sel & Poivre"
	elif action == 8:
		inS  = raw_input("seuil bruitage    [10]: ")
		outS = raw_input("seuil débruitage  [35] : ")
		arg1, arg2 = 10, 35
		if inS != "":
			arg1 = int(inS)
		if outS != "":
			arg2 = int(outS)
		print startStr
		testAdditiveBernouilliNoise(image1, arg1, arg2)        # teste le bruitage/débruitage de type "Additif"
	elif action == 9:
		inS  = raw_input("sigma             [10]: ")
		outS = raw_input("seuil débruitage  [35] : ")
		arg1, arg2 = 10, 35
		if inS != "":
			arg1 = int(inS)
		if outS != "":
			arg2 = int(outS)
		print startStr
		testAdditiveGaussianNoise(image1, arg1, arg2)          # teste le bruitage/débruitage de type "Additif"
	# performances
	elif action == 12:
		print startStr
		printImageQuality(image1, image2)                            # compare 2 images et donne le pourcentage de ressemblance/différence
	elif action == 13:
		print startStr
		printSNR(image1, image2)                                     # compare 2 images et retourne le SNR
	elif action == 14:
		print startStr
		imageForImageQuality(image1, image2)                         # crée une image correspondant aux différences de 2 images
	elif action == 15:
		print startStr
		mergeImagesAdditive(image1, image2)                          # crée une image étant la fusion (addition) de 2 images
	elif action == 16:
		print startStr
		mergeImagesSubstractive(image1, image2)                      # crée une image étant la fusion (soustractive) de 2 images

	elif action == 19:
		r  = raw_input("rouge  [0]: ")
		g  = raw_input("vert   [0]: ")
		b  = raw_input("bleu   [0]: ")
		s  = raw_input("seuil [50]: ")
		arg1, arg2, arg3, arg4 = 0,0,0,50
		if r != "":
			arg1 = int(r)
		if g != "":
			arg2 = int(g)
		if b != "":
			arg3 = int(b)
		if s != "":
			arg4 = int(s)
		print startStr
		revealShapes(image1, arg1, arg2, arg3, arg4)           # révèle la couleur spécifiée
	elif action == 20:
		x = raw_input("abscisses(x) [0]: ")
		y = raw_input("ordonnées(y) [0]: ")
		arg1, arg2 = 0,0
		if x != "":
			arg1 = int(x)
		if y != "":
			arg2 = int(y)
		print startStr
		colorShape(image1, arg1, arg2)                         # colorie la forme contenant le pixel de coordonnées donné
	elif action == 21:
		print startStr
		colorAllShapes(image1)                               # colorie la forme contenant le pixel de coordonnées donné
	elif action == 22:
		print startStr
		testStroke(image1)                                   # trace les contours uniquement à partir de formes pleines


	# filtres
	elif action == 25:
		print startStr
		testAverageFilter(image1)                                   # teste le lissage
	elif action == 26:
		print startStr
		testLaplace(image1)                                  # teste le filtre de Laplace
	elif action == 27:
		print startStr
		testRoberts(image1)                                  # teste le filtre de Roberts
	elif action == 28:
		print startStr
		testPrewitt(image1)                                  # teste le filtre de Prewitt
	elif action == 29:
		print startStr
		testSobel(image1)                                    # teste le filtre de Sobel
	elif action == 30:
		print startStr
		testConvolution(image1)                              # teste le filtre de Convolution
	elif action == 31:
		print startStr
		testBichrome(image1)                                 # teste le passage au bichromatique
	elif action == 32:
		print startStr
		testHighPass(image1)                                 # teste le filtre passe haut

	else:
		print "Wrong choice"
		exit();

	print "+---------------------------+---------+"
	print "| EXECUTION TIME            | %s |" % execTime.get()
	print "+---------------------------+---------+"
	print
	print result



	print '- [PRESS ANY KEY TO CONTINUE] -';
	print '- [  BUT PRESS "Q" TO QUIT  ] -';
	print '- [ OR PRESS "R" TO RELOAD  ] -';
	loopKey = raw_input('- [  OR PRESS "S" TO SAVE   ] -');
	
	if( loopKey == 'q' or loopKey == 'Q' ):
		exit();
	elif( loopKey == 'r' or loopKey == 'R' ):
		loadFiles();
	elif( loopKey == 's' or loopKey == 'S' ):
		out = raw_input("out file: ");
		image1.unparse();
		image1.write(out);
	
	interfaceLoop();





















################" EXECUTABLE "###################

sh('clear');

print "+---------------------------+"
print "|                           |"
print "|       CHARGEMENT...       |"
print "|                           |"
print "+---------------------------+"

# ON CREE LES IMAGES
image1, file1 = BMPFile(True), "";
image2, file2 = BMPFile(), "";

with open( sys.argv[1] ) as file:
	file1 += file.read();

try:
	with open( sys.argv[2] ) as file:
		file2 += file.read()
except Exception as e:
	print e;

def loadFiles():
	image1.parse( file1 );

	for line in image1.content.map:
		for pix in line:
			image1.drawer.setPixel( pix );
	image1.drawer.refresh();

	if( file2 != "" ):
		image2.parse( file2 );



loadFiles();


m.boucle()

# interfaceLoop();
