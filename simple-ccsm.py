#!/usr/bin/env python
# -*-  coding: UTF-8 -*-

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
import gtk.gdk as gdk
import gtk.glade as glade
import cairo
import compizconfig as ccs
import ccm

DataDir = './'
Profiles = [\
"Low Effects", "Easy to the eyes", "Medium Effects", "High Effects", "Hollywood got nothing"
]
 
class DesktopPreview(gtk.Widget):
    def __init__(self, size=(0,0)):
        gtk.Widget.__init__(self)

        self.size = size
        self.desktop_height = 30
        self.desktop_width = 40
        self.desktop_space = 5
        self.line_width = 1.0

    def set_value(self, size):
        self.size = size
        self.queue_resize()

    def get_value(self):
        return self.size

    def do_realize(self):
        self.set_flags(self.flags() | gtk.REALIZED)

        self.window = gdk.Window(
            self.get_parent_window(),
            width = self.allocation.width,
            height = self.allocation.height,
            window_type = gdk.WINDOW_CHILD,
            wclass = gdk.INPUT_OUTPUT,
            event_mask = self.get_events() | gdk.EXPOSURE_MASK)

        self.window.set_user_data(self)
        self.style.attach(self.window)
        self.style.set_background(self.window, gtk.STATE_NORMAL)
        self.window.move_resize(*self.allocation)
        self.bg = self.style.bg[gtk.STATE_NORMAL]
        self.fg = self.style.bg[gtk.STATE_SELECTED]
        self.dark = self.style.fg[gtk.STATE_NORMAL]
    
    def do_unrealize(self):
        self.window.destroy()

    def do_size_request(self, req):
        req.height = (self.desktop_height+self.desktop_space)*self.size[1] - self.desktop_space + self.line_width
        req.width = (self.desktop_width+self.desktop_space)*self.size[0] - self.desktop_space + self.line_width 

    def do_size_allocation(self, allocation):
        if self.flags() & gtk.REALIZED:
            self.window.move_resize(*alloaction)

    def do_expose_event(self, event):
        cr = self.window.cairo_create()
        
        cr.set_operator(cairo.OPERATOR_CLEAR)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)

        cr.set_source_rgb(self.bg.red/65535.0,
                          self.bg.green/65535.0,
                          self.bg.blue/65535.0)
        cr.paint()
        cr.translate(self.line_width/2.0, self.line_width/2.0)

        x = 0
        y = 0
        for i in range(self.size[1]):
            for j in range(self.size[0]):
                cr.set_source_rgb(self.fg.red/65535.0,
                              self.fg.green/65535.0,
                              self.fg.blue/65535.0)

                cr.rectangle(x, y, self.desktop_width, self.desktop_height)
                cr.fill_preserve()
                
                cr.set_line_width(self.line_width)
                cr.set_source_rgb(self.dark.red/65535.0,
                              self.dark.green/65535.0,
                              self.dark.blue/65535.0)
                cr.stroke()


                x += self.desktop_width + self.desktop_space
            y += self.desktop_height + self.desktop_space
            x = 0


class StarScale(gtk.Widget):
    def __init__(self, stars=0):
       gtk.Widget.__init__(self)

       self.stars = stars
       self.star_size = 16
       self.star_space = 5

       self.star_surface = cairo.ImageSurface.create_from_png("%s/star.png" % DataDir)
    
    def set_value(self, stars):
        self.stars = stars
        self.queue_resize()

    def get_value(self):
        return self.stars
    
    def do_realize(self):
        self.set_flags(self.flags() | gtk.REALIZED)

        self.window = gdk.Window(
            self.get_parent_window(),
            width = self.allocation.width,
            height = self.allocation.height,
            window_type = gdk.WINDOW_CHILD,
            wclass = gdk.INPUT_OUTPUT,
            event_mask = self.get_events() | gdk.EXPOSURE_MASK)

        self.window.set_user_data(self)
        self.style.attach(self.window)
        self.style.set_background(self.window, gtk.STATE_NORMAL)
        self.window.move_resize(*self.allocation)
        self.bg = self.style.bg[gtk.STATE_NORMAL]
    
    def do_unrealize(self):
        self.window.destroy()

    def do_size_request(self, req):
        req.height = self.star_size
        req.width = (self.star_size+self.star_space)*self.stars

    def do_size_allocation(self, allocation):
        if self.flags() & gtk.REALIZED:
            self.window.move_resize(*alloaction)

    def do_expose_event(self, event):
        cr = self.window.cairo_create()
        
        cr.set_operator(cairo.OPERATOR_CLEAR)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)

        cr.set_source_rgb(self.bg.red/65535.0,
                          self.bg.green/65535.0,
                          self.bg.blue/65535.0)
        cr.paint()

        x = 0
        for star in range(self.stars):
            cr.set_source_surface(self.star_surface, x, 0)
            cr.rectangle(x, 0, self.star_size, self.star_size)
            cr.fill()
            x += self.star_size + self.star_space


gobject.type_register(StarScale)
gobject.type_register(DesktopPreview)
        
class MainWin:
    def __init__(self, context):
        self.GladeXML = glade.XML(DataDir + "simple-ccsm.glade")
		
        self.Context = context
        self.Block = 0
        
        self.Window = self.GladeXML.get_widget("mainWin")
        self.Window.connect('destroy', self.Quit)

        profileSelector = self.GladeXML.get_widget("profileSelector")
        profileSelector.connect('value-changed', self.ProfileChanged) 

        checkList = self.GladeXML.get_widget("checkList")
        effectStars = StarScale()
        effectStars.set_value(3)
        animationStars = StarScale()
        animationStars.set_value(4)
        checkList.attach(animationStars, 1, 2, 0, 1, gtk.EXPAND)
        checkList.attach(effectStars, 1, 2, 1, 2, gtk.EXPAND)

        desktopTable = self.GladeXML.get_widget("desktopTable")
        self.DesktopPreview = DesktopPreview()
        desktopTable.attach(self.DesktopPreview, 1, 2, 4, 5, 0, 0)
        
        self.CurrentProfile = self.GladeXML.get_widget("currentProfile")
        self.ProfileLayout = "<span size='large'><b>Profile:</b> %s</span>" 
        
        self.DesktopLayout = "<i><span size='large'>%s</span></i>"

        self.Update()

        desktopBox = self.GladeXML.get_widget("desktopPluginChooser")
        desktopBox.connect('changed', self.AppearenceBoxChanged)

        desktopHSize = self.GladeXML.get_widget("horizontalDesktops")
        desktopHSize.connect('value-changed', self.DesktopSizeChanged, "hsize")
        desktopVSize = self.GladeXML.get_widget("verticalDesktops")
        desktopVSize.connect('value-changed', self.DesktopSizeChanged, "vsize")

        animationClose = self.GladeXML.get_widget("closeAnimationBox")
        animationClose.connect('changed', self.AnimationBoxChanged, "close_effects")
        animationOpen = self.GladeXML.get_widget("openAnimationBox")
        animationOpen.connect('changed', self.AnimationBoxChanged, "open_effects")
        animationMinimize = self.GladeXML.get_widget("minimizeAnimationBox")
        animationMinimize.connect('changed', self.AnimationBoxChanged, "minimize_effects")
        
        self.Window.show_all()

    def EnablePlugin(self, plugin, active):
        if self.Block > 0:
            return
        self.Block += 1
        # attempt to resolve conflicts...
        conflicts = plugin.Enabled and plugin.DisableConflicts or plugin.EnableConflicts
        conflict = ccm.PluginConflict(plugin, conflicts, autoResolve=True)
        if conflict.Resolve():
            plugin.Enabled = active
        else:
            return False
        self.Context.Write()
        self.Block = self.Block-1
        return True
    
    def SetupBoxModel(self, box):
        store = gtk.ListStore(gobject.TYPE_STRING)
        box.set_model(store)
        cell = gtk.CellRendererText()
        box.pack_start(cell, True)
        box.add_attribute(cell, 'text', 0)
    
    def UpdateDesktopPlugins(self):
        self.DesktopPlugins = {}
        for plugin in self.Context.Plugins.values():
            if "largedesktop" in plugin.Features:
                self.DesktopPlugins[plugin.ShortDesc] = plugin
    
    def Update(self):
        profile = self.Context.CurrentProfile.Name
        self.CurrentProfile.set_markup(self.ProfileLayout % (profile != "" and profile or "Default"))
        
        self.FillAnimationBoxes()
        self.UpdateDesktopPlugins()
        self.FillAppearenceBox()
        self.SetDesktopLabel()
        self.SetDesktopSize()
        self.SetDesktopPreview()

    def ProfileChanged(self, widget):
        value = int(widget.get_value()) -1
        profile = Profiles[value]
        
        #self.Context.CurrentProfile = profile
    
    def SetDesktopPreview(self):
        hsize = self.Context.Plugins['core'].Screens[0]["hsize"].Value
        vsize = self.Context.Plugins['core'].Screens[0]["vsize"].Value
        self.DesktopPreview.set_value((hsize, vsize))
    
    def DesktopSizeChanged(self, widget, settingName):
        value = widget.get_value()
        self.Context.Plugins['core'].Screens[0][settingName].Value = value
        self.Context.Write()
        self.SetDesktopPreview()
    
    def SetDesktopSize(self):
        scales = {"horizontalDesktops" : "hsize",
                  "verticalDesktops"   : "vsize"}

        for widgetName, settingName in scales.items():
            widget = self.GladeXML.get_widget(widgetName)
            setting = self.Context.Plugins['core'].Screens[0][settingName]
            widget.set_value(setting.Value)
    
    def SetDesktopLabel(self):
        label = self.GladeXML.get_widget("desktopLabel")
        for shortDesc, plugin in self.DesktopPlugins.items():
            if plugin.Enabled:
                label.set_markup(self.DesktopLayout % shortDesc)
                break
    
    def AppearenceBoxChanged(self, widget):
        text = widget.get_active_text()

        for shortDesc, plugin in self.DesktopPlugins.items():
            if text != shortDesc:
                self.EnablePlugin(plugin, False)
        
        self.Context.Write()

        for shortDesc, plugin in self.DesktopPlugins.items():
            if text == shortDesc:
                plugin.Enabled = True
                # exception for cube, since it requires rotate
                if plugin.Name == 'cube':
                    self.EnablePlugin(self.Context.Plugins['rotate'], True)

        self.Context.Write()

    def FillAppearenceBox(self):
        box = self.GladeXML.get_widget("desktopPluginChooser")
        self.SetupBoxModel(box)

        i = 0
        for shortDesc, plugin in self.DesktopPlugins.items():
            box.append_text(shortDesc)
            if plugin.Enabled:
                box.set_active(i)
            i += 1
    
    def AnimationBoxChanged(self, widget, settingName):
        text = widget.get_active_text()
        plugin = self.Context.Plugins['animation']
        setting = plugin.Screens[0][settingName]
        value = setting.Value
        if len(value) >= 1:
            value[0] = setting.Info[1][2][text]
            setting.Value = value
            self.Context.Write()
        else:
            for setting in plugin.Groups[setting.Group][setting.SubGroup].Screens[0].values():
                setting.Reset()
            self.Context.Write()
            self.AnimationBoxChanged(widget, settingName)
    
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
            self.SetupBoxModel(box)
            for key, value in items:
                box.append_text(key)
            if len(setting.Value):
                box.set_active(setting.Value[0])
            else:
                box.set_active(0)

    def Quit(self, widget):
        gtk.main_quit()

context = ccs.Context()
mainWin = MainWin(context)
gtk.main()
