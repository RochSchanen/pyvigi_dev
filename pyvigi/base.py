#!/usr/bin/python3
# file: base.py
# content: App class definition
# created: 2020 March 21
# modified: 2022 August 24
# modification: use tools module
# author: Roch Schanen
# repository: https://github.com/RochSchanen/pyvigi_dev
# comment:

# constants, methods and classes are imported individually
# this allows to identify clearly the packages usage

# from wxpython: https://www.wxpython.org/

# classes
from wx import Panel                as wxPanel
from wx import Frame                as wxFrame
from wx import App                  as wxApp

# wx classes default constants
from wx import ID_ANY               as wxID_ANY
from wx import DefaultPosition      as wxDefaultPosition
from wx import DefaultSize          as wxDefaultSize
from wx import NO_BORDER            as wxNO_BORDER
from wx import DEFAULT_FRAME_STYLE  as wxDEFAULT_FRAME_STYLE
from wx import RESIZE_BORDER        as wxRESIZE_BORDER
from wx import MAXIMIZE_BOX         as wxMAXIMIZE_BOX

# wx bitmap methods
from wx import PaintDC as wxPaintDC

# wx event constants
from wx import EVT_PAINT            as wxEVT_PAINT
from wx import EVT_KEY_DOWN         as wxEVT_KEY_DOWN
from wx import WXK_ESCAPE           as wxWXK_ESCAPE

# wx system
from wx import Exit                 as wxExit

""" 
    
    Quick App:
    
    On instantiating an "App" object, a frame is
    automatically created and a panel container
    too.
    
    A "BackgroundBitmap" is created and is used for
    painting the panel background when "Refreshed".

    Importantly, the "BackgroundBitmap" is used
    as a canvas for the layout class to draw the
    App's decors.

"""

# Quick Panel
class _basePanel(wxPanel):

    def __init__(self, parent):

        wxPanel.__init__(
            self,
            parent = parent,
            id     = wxID_ANY,
            pos    = wxDefaultPosition,
            size   = wxDefaultSize,
            style  = wxNO_BORDER,
            name   = "")

        # BackgroundBitmaps are used to draw decors
        self.BackgroundBitmap = None

        # bind paint event
        self.Bind(wxEVT_PAINT, self._OnPaint)

        # done
        return

    def _OnPaint(self, event):

        # re-draw BackgroundBitmap if defined
        if self.BackgroundBitmap: 

            # "DCPaint" is used here.
            # maybe "BufferedPaintDC" should be used instead.
            # todo: explore documentation
            dc = wxPaintDC(self)
            dc.DrawBitmap(self.BackgroundBitmap, 0, 0)

        #done
        return

# Quick Frame
class _baseFrm(wxFrame):

    def __init__(self):

        wxFrame.__init__(
            self,
            parent = None,
            id     = wxID_ANY,
            title  = "",
            pos    = wxDefaultPosition,
            size   = wxDefaultSize,
            style  = wxDEFAULT_FRAME_STYLE
                    ^ wxRESIZE_BORDER
                    ^ wxMAXIMIZE_BOX,
            name   = "")

        # create the panel
        # (by default the Panel should
        # take the size of the Frame)
        self.Panel = _basePanel(self)

        # done
        return

# When _ESCAPE = True you can use the
# ESCAPE key  to quit the Application
# (This is used for debbugging)
_ESCAPE = True

# Quick App
class app(wxApp):

    def OnInit(self):
        # create reference to App
        # self.App = self (most likely useless)
        # create and show Frame
        self.Frame = _baseFrm()     
        # create reference to Panel
        self.Panel = self.Frame.Panel
        # call user's start up code
        self.Start()
        # adjust widow size to BackgroundBitmap size
        if self.Frame.Panel.BackgroundBitmap:
            w, h = self.Frame.Panel.BackgroundBitmap.GetSize()
            self.Frame.SetClientSize((w, h))
        # bind key events
        self.Bind(wxEVT_KEY_DOWN, self._OnKeyDown)
        # show the frame
        self.Frame.Show(True)
        # done
        return True

    # Start() is to be overloaded by the user
    def Start(self):
        # user's start up code
        pass

    def Run(self):
        self.MainLoop()
        return

    def _OnKeyDown(self, event):
        
        key = event.GetKeyCode()

        # catch the ESCAPE key and exit the app
        # when the _ESCAPE flag is set. This is
        # used for development purposes. It will
        # be removed at later time.

        if _ESCAPE:
            if key == wxWXK_ESCAPE:
                wxExit()
                return

        event.Skip() # forward event

        # done
        return

    # def __del__(self):
    #     pass

if __name__ == "__main__":

    from pyvigi.tools import header
    header()

    from sys import version
    print(f"run Python version {version.split(' ')[0]}")

    from pyvigi import version
    print(f"using pyvigi version {version}")

    a = app()
    a.Run()
