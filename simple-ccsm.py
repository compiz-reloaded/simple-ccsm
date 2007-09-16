#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
# Authors: Patrick Niklaus (marex@opencompositing.org)
# Copyright (C) 2007 Patrick Niklaus

import pygtk
import gtk
import gtk.glade

DataDir = './'

class MainWin:
	def __init__(self):
		gladeXML = gtk.glade.XML(DataDir + "simple-ccsm.glade")
		self.Window = gladeXML.get_widget("mainWin")
		self.Window.show_all()
		self.Window.connect('destroy', self.Quit)
	
	def Quit(self, widget):
		gtk.main_quit()

mainWin = MainWin()
gtk.main()
