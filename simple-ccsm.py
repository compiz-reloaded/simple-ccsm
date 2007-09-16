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
import gobject
import gtk.glade

import compizconfig as ccs
import ccm

DataDir = './'

class MainWin:
    def __init__(self, context):
        self.GladeXML = gtk.glade.XML(DataDir + "simple-ccsm.glade")
		
        self.Context = context
        
        self.Window = self.GladeXML.get_widget("mainWin")
        self.Window.show_all()
        self.Window.connect('destroy', self.Quit)

        self.FillAnimationBoxes()

    def FillAnimationBoxes(self):
        plugin = self.Context.Plugins['animation']
        
        boxes = {}
        boxes['closeAnimationBox'] =  "close_effects"
        boxes['openAnimationBox'] = "open_effects"
        boxes['minimizeAnimationBox'] = "minimize_effects"

        for boxName, settingName in boxes.items():
            box = self.GladeXML.get_widget(boxName)
            setting = plugin.Screens[0][settingName]
            items = sorted(setting.Info[1][2].items(), ccm.EnumSettingSortCompare)
            store = gtk.ListStore(gobject.TYPE_STRING)
            box.set_model(store)
            cell = gtk.CellRendererText()
            box.pack_start(cell, True)
            box.add_attribute(cell, 'text', 0)
            for key, value in items:
                iter = store.append(None)
                store.set(iter, 0, key)
            box.set_active(setting.Value[0])

    def Quit(self, widget):
        gtk.main_quit()

context = ccs.Context()
mainWin = MainWin(context)
gtk.main()
