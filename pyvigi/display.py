#!/usr/bin/python3
# file: display.py
# content:
# created: 2020 April 02
# modified: 2022 August 23
# modification:
# author: roch schanen
# repository: https://github.com/RochSchanen/pyvigi_dev
# comment:

# constants, methods and classes are imported individually
# this allows to identify clearly the packages usage

# from wxpython: https://www.wxpython.org/

# wx control class
from wx import Control              as wxControl

# wx control class default constants
from wx import ID_ANY               as wxID_ANY
from wx import DefaultPosition      as wxDefaultPosition
from wx import DefaultSize          as wxDefaultSize
from wx import NO_BORDER            as wxNO_BORDER
from wx import DefaultValidator     as wxDefaultValidator

# wx bitmap methods
from wx import Bitmap               as wxBitmap
from wx import BufferedPaintDC      as wxBufferedPaintDC

# wx event constants
from wx import EVT_ERASE_BACKGROUND as wxEVT_ERASE_BACKGROUND
from wx import EVT_PAINT            as wxEVT_PAINT

"""

The bitmap control is used to display an image
taken from a select set that is loaded during
instanciation of the control. Note that There
are three methods for loading the images.
you can then select the image to display by
name or by number: the image index in the
collection.

"""

class bitmapControl(wxControl):

    def __init__(
        self,
        parent,
        images,
        names = None):

        wxControl.__init__(
            self,
            parent      = parent,
            id          = wxID_ANY,
            pos         = wxDefaultPosition,
            size        = wxDefaultSize,
            style       = wxNO_BORDER,
            validator   = wxDefaultValidator,
            name        = "")

        # parameters
        self.parent = parent

        # a single image
        if  isinstance(images, wxBitmap):
            self.images = [images]

            # with a single name
            if isinstance(names, str):
                self.names = [names]

        # list of images and list of names
        elif isinstance(images, list):
            self.images = images
            self.names = names

        # dictionary of images with names
        else:
            self.images = images.Values()
            self.names  = images.Keys()

        # status is a pointer to an image
        # its value is a string or a integer
        # default value is zero: the first image
        self.status = 0

        # get png size from first image
        w, h = self.images[self.status].GetSize()
        self.SetSize((w, h))

        # bindings
        self.Bind(wxEVT_ERASE_BACKGROUND, self._onEraseBackground)
        self.Bind(wxEVT_PAINT, self._onPaint)

        # done
        return

    def _onEraseBackground(self, event):
        # force bypass to avoid flicker
        pass

    def _onPaint(self, event):
        v = self.status
        if isinstance(v, int): n = v
        if isinstance(v, str): n = self.names.index(v)
        dc = wxBufferedPaintDC(self)
        dc.DrawBitmap(self.images[n], 0, 0)
        return

    def SetValue(self, Value):
        self.status = Value
        self.Refresh()
        return

    def GetValue(self):
        return self.status

if __name__ == "__main__":

    from pyvigi.tools import header
    header()

    from sys import version
    print(f"run Python version {version.split(' ')[0]}")

    from pyvigi import version
    print(f"using pyvigi version {version}")

    from pyvigi.base import app
    from pyvigi.theme import imageCollect
    from pyvigi.theme import imageSelect
    from pyvigi.timer import timeloop

    # derive a new class from app
    class myapp(app):

        def Start(self):
            # manually setup the background image of myapp
            PANELS = imageCollect("panels")
            self.Panel.BackgroundBitmap = imageSelect(PANELS, "medium")[0]
            # add a led to the panel
            LEDS = imageCollect("leds", "green")
            self.b = bitmapControl(self.Panel, imageSelect(LEDS))
            # set led position
            # (small panel is 128x128)
            w, h = self.b.GetSize()
            self.b.SetPosition((int(256/2-w/2), int(256/2-h/2)))
            # start blinking led
            timeloop(self, self.update, 200)
            # done
            return
    
        def update(self, event):
            # inverse led state
            self.b.SetValue(self.b.GetValue()^1)
            return

    # instanciate myapp
    m = myapp()

    # run myapp
    m.Run()
