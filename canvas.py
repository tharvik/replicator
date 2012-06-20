#!/usr/bin/python
# -*- coding: UTF8 -*-


## Module for replicator
#   Class with the canvas


## Modules import
import wx # For the GUI


## Class generating and setting the canvas
class canvas (wx.Window) :

    def __init__ (self, parent, *args, **kwargs) :

        # Initiate a dummy window to have a canvas
        wx.Window.__init__ (self, parent, size = (512, 512), *args, **kwargs)
        self.Bind (wx.EVT_PAINT, self.onPaint)

        # Static
        self.sizeAdd = 267

        # Initialisation
        self.setDefaultImage (             )
        self.reset           (             )


    # Seter to change the default bitmap
    def setDefaultImage (self, path = None) :

        # Test if the path is given, or it's the first launch and we just need an empty one
        if path :
            image          = wx.Image                 (path)
            image          = image.ConvertToGreyscale (    )

        else :
            image          = wx.NullBitmap.ConvertToImage ()

        # Setup some variables
        sizeImage       = image.GetSize (         )
        self.sizeCanvas = (sizeImage [0] + self.sizeAdd * 2, sizeImage [1] + self.sizeAdd * 2)
        self.arrayImage = self.newArray (self.sizeCanvas)

        # Main part of the function, we treat all the pixel in the input image, and we set the result in the array
        for y in xrange (0, sizeImage [1]) :

            for x in xrange (0, sizeImage [0]) :

                self.arrayImage [y + self.sizeAdd] [x + self.sizeAdd] = 1 - int ((image.GetRed   (x, y) +         \
                                                                                  image.GetGreen (x, y) +         \
                                                                                  image.GetBlue  (x, y))          \
                                                                                  / 383)

        # Set the default bitmap
        bitmap             = wx.EmptyBitmap (self.sizeCanvas [0], self.sizeCanvas [1])
        self.blit (bitmap, self.arrayImage)
        self.defaultCanvas = bitmap
        
    # A nice way to reset an array of bite array
    def newArray (self, size) :

        array = []
        line  = []

        # Create a line of the given size
        # "xrange" is used to lower memory usage
        for i in xrange (size [0]) :
            line.append (0)

        # Add the lines to the array
        for i in xrange (size [1]) :
            array.append (line [:]) # "[:]" used to create an independant copy of the list

        return array

    # A fonction blitting a bitmap based on an array
    def blit (self, bitmap, array) :

        # Create the DC we will draw on and adding the bitmap to update
        dc = wx.MemoryDC ()
        dc.SelectObject (bitmap)
        dc.Clear ()

        size = (len (array [0]), len (array))

        # An array of pen, black: alive, white: dead
        arrayPen = [wx.Pen (wx.WHITE), wx.Pen (wx.BLACK)]

        # An ugly way to treat the 2D array
        for y in range (size [1]) :

            for x in range (size [0]) :

                #print y, x, array [y] [x]
                dc.DrawPointList (((x, y), (0, 0)), (arrayPen [array [y] [x]]))

        # Update the bitmap (DC backend)
        dc.SelectObject (wx.NullBitmap)

    # Return True if, at the given point, the next buffer's pixel is alive (black)
    def nextAlive (self, x, y) :
        
        return (self.arrayImage [y - 1] [x - 1] + \
                self.arrayImage [y - 1] [x    ] + \
                self.arrayImage [y - 1] [x + 1] + \
                self.arrayImage [y    ] [x - 1] + \
                self.arrayImage [y    ] [x + 1] + \
                self.arrayImage [y + 1] [x - 1] + \
                self.arrayImage [y + 1] [x    ] + \
                self.arrayImage [y + 1] [x + 1]) % 2
        

    # Calculate the next image (applicate the mathematic method)
    def nextBuffer (self) :

        nextArray = self.newArray (self.sizeCanvas)

        for y in range (1, self.sizeCanvas [1] - 1) :

            for x in range (1, self.sizeCanvas [0] - 1) :

                #print str(x) + " " + str(y)
                nextArray [y] [x] = self.nextAlive (x, y)

        self.arrayImage = nextArray

        self.actualIteration += 1

        print self.actualIteration

    # Go to a certain value (make a loop of "nextBuffer" function)
    def goTo (self, value) :

        # If minimisation of the value
        if value < self.actualIteration :

            # Setup a new canvas
            self.reset ()

        for i in range (self.actualIteration, value) :
            self.nextBuffer ()

        bitmap      = wx.EmptyBitmap (self.sizeCanvas [0], self.sizeCanvas [1])
        self.blit (bitmap, self.arrayImage)
        self.buffer = bitmap

        # Update the buffer to the screen
        self.Refresh ()
        self.Update  ()

    # Dummy function to set to 0 size a (-1; -1) size, else, return the size
    def normalise (self, size) :

        if size [0] == -1 :
            size [0] = 0

        if size [1] == -1 :
            size [1] = 0

        return size

    # Set the canvas at his original state, with the picture on it
    def reset (self) :

        # Resize the canvas
        self.SetSize (self.sizeCanvas)

        # Reset the buffer
        self.buffer = self.defaultCanvas

        # Update the buffer to the screen
        self.Refresh ()
        self.Update  ()

        self.actualIteration = 0

        return self.sizeCanvas

    # Copy the buffer to the screen (paint event handler)
    def onPaint (self, event) :
        wx.BufferedPaintDC (self, self.buffer)
