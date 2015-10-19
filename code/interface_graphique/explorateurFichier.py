import pygtk
pygtk.require('2.0')

import gtk

dialog = gtk.FileChooserDialog("Open ...",
				None,
				gtk.FILE_CHOOSER_ACTION_OPEN,
				(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
				gtk.STOCK_OPEN, gtk.RESPONSE_OK))
dialog.set_default_response(gtk.RESPONSE_OK)

filter = gtk.FileFilter()
filter.set_name("All files");
filter.add_pattern("*")
dialog.add_filter(filter)

#filter = gtk.FileFilter()


response = dialog.run()
if response == gtk.RESPONSE_OK:
	print dialog.get_filename(), 'selected'
	select = dialog.get_filename()
elif response == gtk.RESPONSE_CANCEL:
	print 'Cosed, no files selected'
dialog.destroy()

print "Nom du fichier selectionne :" + select
