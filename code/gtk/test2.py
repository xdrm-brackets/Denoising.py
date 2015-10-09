import pygtk
pygtk.require('2.0')
import gtk
from random import *

#renvoi une valeur aleatoire
def random2():
	a  = random() 
	aa = a*255.0*257.0
	b = round(aa)
	c = int(b)
	return c

#fonction qui genere un evenement quitter
def click_quite(widget):
        gtk.main_quit()

#seconde gestionn de pixel
def expose_handler_remplir(widget, event):
	widget.set_size_request(512,512)
	w, h = widget.window.get_size()
	print "w = " + str(w) + " | h = " + str(h)
	xgc = widget.window.new_gc()
	cptW = 0
	cptH = 0
	while cptH < 512:
		while cptW < 512:
			xgc.set_rgb_fg_color(gtk.gdk.Color(random2(),0,0, pixel = 0))	
			widget.window.draw_point(xgc, cptW, cptH)
			cptW += 1
		cptH += 1
		cptW =  0
	print "cptW = " + str(cptW) + "| cptH = " + str(cptH)

#definition des elements de base de la fenetre
def param_main_window(widget):
	widget.set_title("Test object drawable")
	widget.set_size_request(500,500)

def param_main_manual_window(widget, src1, sizeX, sizeY):
	widget.set_title(src1)
	widget.set_size_request(sizeX, sizeY)


#creation de la fneetre principal
fen = gtk.Window(gtk.WINDOW_TOPLEVEL)
#definition des elements de base de la fenetre
param_main_manual_window(fen, "Test object drawable manual", 800, 800)
button = gtk.Button("Quit") #bouton
button2 = gtk.Button("Quit") # seocnd bouton
zone   = gtk.DrawingArea() #zone de dessin
vBox   = gtk.VBox() #boite de placement


#raccordement a la fenetre de la box
fen.add(vBox)

#connection des differents elements
button.connect("clicked", click_quite)
button2.connect("clicked", click_quite)
zone.set_size_request(512,512)
zone.connect("expose-event", expose_handler_remplir)

#ajout des elemnts dans les box
vBox.pack_start(button)
vBox.pack_start(zone)
vBox.pack_start(button2)

#affichage des differents elements
button.show()
button2.show()
zone.show()
vBox.show()
fen.show()
gtk.main()


