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
		print "Evnmt explorateur survenu"
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
		if str1 == "Additif(Gaussien)":
			print "gaussien"
		elif str1 == "Additif(Bernouilli)":
			print "bernouilli"
		elif str1 == "Salt and Pepper":
			print "salt and peper"
		else:
			print "Not found"


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
		self.combo.append_text("Salt and Pepper")
		self.combo.append_text("Additif(Bernouilli)")
		self.combo.append_text("Additif(Gaussien)")
		self.combo.connect('changed', self.changed_cb)
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

if __name__ == "__main__":
	m = Test()
	m.boucle()
