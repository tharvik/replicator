#!/usr/bin/python
# -*- coding: UTF8 -*-


## Script to replicate an image on a DC using some kind of biologic algorithme.
#   Version 0.0.1

## Modules import
import wx # For the GUI

from mainFrame import mainFrame


## Script

# Init function, lauch all the others 
def main () :

    application = wx.App (False)
    mainFrame ()
    application.MainLoop ()
    

# Launcher
main ()
