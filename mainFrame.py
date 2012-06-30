#!/usr/bin/python
# -*- coding: UTF8 -*-


## Module for replicator
#   Class with the main frame

## Modules import
import wx                          # For the GUI
import wx.lib.agw.floatspin as agw # For the GUI, FloatSpin
import os                          # For the OS path

from canvas import canvas


# Generate the whole frame, set all the other elements
class mainFrame (wx.Frame) :

    def __init__ (self) :

        wx.Frame.__init__ (self, None)

        ## Menu
        self.CreateStatusBar  ()

        # Creating the menu bar
        menuBar  = wx.MenuBar ()
        self.SetMenuBar (menuBar)
        
        # Creating the menu
        menuFile = wx.Menu ()
        menuHelp = wx.Menu ()
        
        # Adding some contents
        menuFileOpen  = wx.MenuItem (menuFile, wx.ID_OPEN )
        menuFileNew   = wx.MenuItem (menuFile, wx.ID_NEW  )
        menuFileSave  = wx.MenuItem (menuFile, wx.ID_SAVE )
        menuFileQuit  = wx.MenuItem (menuFile, wx.ID_EXIT )
        
        menuHelpAbout = wx.MenuItem (menuHelp, wx.ID_ABOUT)      
        
        # Binding
        self.Bind (wx.EVT_MENU, self.onOpen , menuFileOpen )
        self.Bind (wx.EVT_MENU, self.onNew  , menuFileNew  )
        self.Bind (wx.EVT_MENU, self.onSave , menuFileSave )
        self.Bind (wx.EVT_MENU, self.onQuit , menuFileQuit )
        
        self.Bind (wx.EVT_MENU, self.onAbout, menuHelpAbout)
        
        # Adding contents to the menus
        menuFile.AppendItem      (menuFileOpen )
        menuFile.AppendSeparator (             )
        menuFile.AppendItem      (menuFileNew  )
        menuFile.AppendItem      (menuFileSave )
        menuFile.AppendSeparator (             )
        menuFile.AppendItem      (menuFileQuit )
        
        menuHelp.AppendItem      (menuHelpAbout)
        
        # Adding the menus to the menu bar
        menuBar.Append (menuFile, "&Fichier")
        menuBar.Append (menuHelp, "&Aide"   )
        
        ## Frame
        
        # Creating some filling for the frame
        iterationText   = wx.StaticText (self, label = "Iteration"          )
        progressionText = wx.StaticText (self, label = "Progression"        )
        repetitionText  = wx.StaticText (self, label = "Chaques"            )
        secondesText    = wx.StaticText (self, label = "Secondes"           )
        
        self.iterationCtrl   = wx.SpinCtrl   (self, initial = 0, min = 0, max = 256, name = "iteration",   style = wx.TE_PROCESS_ENTER                       ) 
        progressionCtrl      = wx.SpinCtrl   (self, initial = 1, min = 1, max = 256, name = "progression", style = wx.TE_PROCESS_ENTER                       )
        repetitionCtrl       = agw.FloatSpin (self, min_val = 0.1, increment = 0.1, value = 0.5, digits = 1, name = "repetition", style = wx.TE_PROCESS_ENTER)
        
        # Adding the canvas
        self.canvas = canvas (self)
        
        # Binding
        self.Bind (wx.EVT_TEXT_ENTER, self.onTextEnter, self.iterationCtrl  )
        self.Bind (wx.EVT_TEXT_ENTER, self.onTextEnter, progressionCtrl     )
        self.Bind (wx.EVT_TEXT_ENTER, self.onTextEnter, repetitionCtrl      )
        
        # Layout the frame
        sizerIteration   = wx.BoxSizer (wx.HORIZONTAL)
        sizerProgression = wx.BoxSizer (wx.HORIZONTAL)
        sizeRepetition   = wx.BoxSizer (wx.HORIZONTAL)
        sizerBar         = wx.BoxSizer (wx.HORIZONTAL)
        self.sizerMain        = wx.BoxSizer (wx.VERTICAL  )
        
        sizerIteration.Add   (iterationText,     flag = wx.CENTER)
        sizerIteration.Add   (self.iterationCtrl                 )
        sizerProgression.Add (progressionText,   flag = wx.CENTER)
        sizerProgression.Add (progressionCtrl                    )
        sizeRepetition.Add   (repetitionText,    flag = wx.CENTER)
        sizeRepetition.Add   (repetitionCtrl                     )
        sizeRepetition.Add   (secondesText,      flag = wx.CENTER)
        
        sizerBar.Add         (sizerIteration                     )
        sizerBar.Add         ((20, -1)                           )
        sizerBar.Add         (sizerProgression                   )
        sizerBar.Add         ((20, -1)                           )
        sizerBar.Add         (sizeRepetition                     )
        
        self.sizerMain.Add        (sizerBar,    flag = wx.CENTER      )
        self.canvasSizer = self.sizerMain.Add        (self.canvas, 1, flag = wx.CENTER      )
        
        self.SetSizerAndFit (self.sizerMain)
        
        # Some setup
        self.defaultDirectory = os.getcwd ()
        self.Show ()
    
    # Open a dialog to find the wanted image
    def onOpen (self, event) :
    
        # Setup the dialog
        wildcard = "Joint Photographic Experts Group (*.jpeg)|*.jp*g|" \
                   "Portable Network Graphics (*.png)|*.png|"          \
                   "Graphics Interchange Format (*.gif)|*.gif|"        \
                   "Bitmap Image File (*.bmp)|*.bmp|"                  \
                   "Tagged Image File Format (*.tiff)|*.tif*|"         \
                   "Personal Computer Exchange (*.pcx)|*.pcx|"         \
                   "Portable Pixmap Format (*.ppm)|*.ppm|"             \
                   "Portable Graymap Format (*.pgm)|*.gpm|"            \
                   "Portable Bitmap Format (*.pbm)|*.pbm|"             \
                   "Portable Anymap Format (*.pnm)|*.pnm|"             \
                   "Interchange File Format (*.iff)|*.iff|"            \
                   "X Pixmap (*.xpm)|*.xpm|"                           \
                   "ICO (*.ico)|*.ico|"                                \
                   "CUR (*.cur)|*.cur|"                                \
                   "ANI (*.ani)|*.ani|"                                \
                   "All files (*.*)|*.*"

        dialog = wx.FileDialog (self,
                                message     = "Choisisser une image",
                                defaultDir  = self.defaultDirectory,
                                wildcard    = wildcard,
                                style       = wx.OPEN | wx.CHANGE_DIR
                                )
        
        # Show the dialog
        if dialog.ShowModal () == wx.ID_OK :
        
            # Get the corresponding info
            path                  = dialog.GetPath ()
            self.imageName        = dialog.GetFilename ()
            self.defaultDirectory = os.path.dirname (path)

            self.canvas.setDefaultImage (path)
            sizeCanvas = self.canvas.reset ()
            
            self.sizerMain.SetItemMinSize (self.canvas, sizeCanvas)
            self.sizerMain.Layout ()
            
        # Cleanup
        dialog.Destroy ()
    
    # Set the canvas to a white background
    def onNew (self, event) :
        self.canvas.reset ()
    
    # Save the canvas' image to a specific file
    def onSave (self, event) :
        
        wildcard = "Joint Photographic Experts Group (*.jpeg)|*.jp*g|" \
                   "Portable Network Graphics (*.png)|*.png|"          \
                   "Bitmap Image File (*.bmp)|*.bmp|"                  \
                   "Tagged Image File Format (*.tiff)|*.tif*|"         \
                   "Personal Computer Exchange (*.pcx)|*.pcx|"         \
                   "Portable Pixmap Format (*.ppm)|*.ppm|"             \
                   "Portable Graymap Format (*.pgm)|*.gpm|"            \
                   "Portable Bitmap Format (*.pbm)|*.pbm|"             \
                   "Portable Anymap Format (*.pnm)|*.pnm|"             \
                   "X Pixmap (*.xpm)|*.xpm|"                           \
                   "ICO (*.ico)|*.ico|"                                \
                   "CUR (*.cur)|*.cur|"                                \
                   "All files (*.*)|*.*"

        dialog = wx.FileDialog (self,
                                message     = "Enregistrer l'image",
                                defaultDir  = self.defaultDirectory,
                                defaultFile = "Replicator -", self.canvas.actualIteration, "iteration"
                                wildcard    = wildcard,
                                style       = wx.OPEN | wx.CHANGE_DIR
                                )
        
        # Show the dialog
        if dialog.ShowModal () == wx.ID_OK :
            path = dialog.GetPaths () [0]
        
            ##! Save the canvas' bitmap to a file
    
        dialog.Destroy ()
    
    # Quit the application
    def onQuit (self, event) :
        self.Close ()
    
    # Show the about dialog
    def onAbout (self, event) :
        
        about = wx.AboutDialogInfo()
        about.Name = "Replicator"
        about.Version = "0.0.1"
        about.Description = "\"Replicator\" is a python script to replicate"\
                            "an image following some kind of biological"\
                            "algorithm and to improve my python's writing."
        about.Developers = [ "Kéwan Marconnet (tharvik)" ]

        wx.AboutBox (about)
        
    # Event handler of the SpinCtrl
    def onTextEnter (self, event) :
    
        # Get the name and actual value of the SpinCtrl
        name      = event.GetEventObject ().Name
        value     = event.GetEventObject ().GetValue ()
        
        # Get the value of the "iterationCtrl"
        iteration = self.iterationCtrl.GetValue ()
        
        if name == "iteration" :
            self.canvas.goTo (value)

        elif name == "progression" :
            ##! Add support for a working increment
            self.iterationCtrl.SetValue (iteration + value)
            self.iterationCtrl.Command  (wx.CommandEvent ())
            
        elif name == "repetition" :
            print "repetition"
        
        else :
            event.skip ()
            
