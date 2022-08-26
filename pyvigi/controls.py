#!/usr/bin/python3
# file: controls.py
# content: Control class definition
# created: 2020 April 03
# modified: 2022 August 22
# modification: use tools module
# author: Roch Schanen
# repository: https://github.com/RochSchanen/pyvigi_dev
# comment:

# wxpython: https://www.wxpython.org/

# constants, methods and classes are imported individually
# this allows to identify clearly the package usage

# classes
from wx import Control              as wxControl

# wx classes default constants
from wx import ID_ANY               as wxID_ANY
from wx import DefaultPosition      as wxDefaultPosition
from wx import DefaultSize          as wxDefaultSize
from wx import NO_BORDER            as wxNO_BORDER
from wx import DefaultValidator     as wxDefaultValidator

# wx bitmap methods
from wx import BufferedPaintDC      as wxBufferedPaintDC

# wx event constants
from wx import EVT_ERASE_BACKGROUND as wxEVT_ERASE_BACKGROUND
from wx import EVT_PAINT            as wxEVT_PAINT

# wx event methods
from wx import wxPostEvent
from wx.lib.newevent import wxNewEvent

class Control(wxControl):

    def __init__(
        self,
        parent):

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

        # status is the value returned
        # by SendEvent to owner class
        self.status = None
        
        # When defined the BackgroundBitmap
        # is automatically re-drawn on any
        # paint event
        self.BackgroundBitmap = None
        
        # "self.ctr" is used to build the event
        # object that needs to be returned to
        # the owner. "self.evt" may not need to
        # be defined globally...
        self.ctr, self.evt = None, None
        
        # set background (do i need this?)
        # self.SetBackgroundColour(BackgroundColour)
        
        # bindings
        self.Bind(wxEVT_ERASE_BACKGROUND,self._onEraseBackground)
        self.Bind(wxEVT_PAINT,self._onPaint)
        
        # user constructor
        self.Start()
        
        # done
        return

    # to be overloaded by user's code
    def Start(self):
        pass

    def _onEraseBackground(self, event):
        # force bypass to avoid flicker
        pass

    def _onPaint(self, event):
        if self.BackgroundBitmap:
            dc = wxBufferedPaintDC(self)
            dc.DrawBitmap(self.BackgroundBitmap, 0, 0)
        return

    def BindEvent(self, handler):
        self.ctr, self.evt = wxNewEvent()
        self.GetParent().Bind(self.evt, handler)
        return
        # "self.evt" is only used once in the "BindEvent" method
        # can it then be defined only locally?

    def SendEvent(self):
        if self.ctr:
            event = self.ctr(caller=self, status = self.status)
            wxPostEvent(self.GetParent(), event)
        return
 