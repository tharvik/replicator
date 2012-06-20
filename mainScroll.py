#!/usr/bin/python
# -*- coding: UTF8 -*-


## Module for replicator
#   Class with the scroll windows which hold the canvas

## Still unused, have to be added

## Modules import
import wx # For the GUI

from canvas import canvas


## Class
class mainScroll (wx.ScrolledWindow) :

    def __init__ (self, parent) :
        
        # Set the class as a Scrolled Window    
        wx.ScrolledWindow.__init__ (self, parent)
        
        self.SetScrollbars (20, 20, 60, 40)
        
        # Add the canvas
        self.canvas = canvas (self)
        
        self.Show ()
