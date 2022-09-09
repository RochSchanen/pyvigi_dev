#!/usr/bin/python3
# file: controls.py
# content: Control class definition
# created: 2020 April 03
# modified: 2022 August 22
# modification: add vScroll control
# author: Roch Schanen
# repository: https://github.com/RochSchanen/pyvigi_dev
# comment:

# wxpython: https://www.wxpython.org/

# constants, methods and classes are imported individually
# this allows to identify clearly the package usage

# wx classes
from wx import Control              as wxControl

# wx methods
from wx import GetMousePosition     as wxGetMousePosition

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

from wx import EVT_LEFT_DOWN    as wxEVT_LEFT_DOWN
from wx import EVT_MOTION       as wxEVT_MOTION
from wx import EVT_LEFT_UP      as wxEVT_LEFT_UP
from wx import EVT_LEAVE_WINDOW as wxEVT_LEAVE_WINDOW
from wx import EVT_MOUSEWHEEL   as wxEVT_MOUSEWHEEL

# wx event methods
from wx import PostEvent as wxPostEvent
from wx.lib.newevent import NewEvent as wxNewEvent

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
        
        # bindings
        self.Bind(wxEVT_ERASE_BACKGROUND, self._onEraseBackground)
        self.Bind(wxEVT_PAINT,self._onPaint)
        
        # user constructor
        self.Start()
        
        # done
        return

    def SetBackground(self, Bitmap):
        w, h = Bitmap.GetSize()
        self.SetSize((w, h))
        self.BackgroundBitmap = Bitmap
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

class vScroll(Control):

    def Start(self):
        # control locked to mouse motion
        self.lock = False
        # default rotation
        self.rotation = 50
        # setup scroll value boundaries
        self.extr = 0, 0
        # bind events
        self.Bind(wxEVT_LEFT_DOWN,      self._LeftDown)
        self.Bind(wxEVT_MOTION,         self._Motion)
        self.Bind(wxEVT_LEFT_UP,        self._LeftUp)
        self.Bind(wxEVT_LEAVE_WINDOW,   self._Leave)
        self.Bind(wxEVT_MOUSEWHEEL,     self._Wheel)

        # done
        return

    def SetRotation(self, Value):
        # +1 is forward one pixel
        # -1 is backward one pixel
        self.rotation = Value
        return

    def _Wheel(self, event):
        # take no action if mouse locked
        if self.lock: return
        # get initial locations
        P, Q = self.GetPosition()
        # get wheel action
        r = event.GetWheelRotation()
        if r > 0: dQ = +self.rotation
        if r < 0: dQ = -self.rotation
        # compute new control position
        p, q = P, Q + dQ
        # get extrema
        MIN, MAX = self.extr
        # coerce to constraints
        if q < MIN: q = MIN
        if q > MAX: q = MAX
        # set new control position
        self.SetPosition((p, q))
        return

    def SetFrameContainerHeight(self, height):
        # get self size
        w, h = self.GetSize()
        # coerce
        if height > h: height = h
        # Parent is Panel
        # Parent.Parent is Frame
        self.Parent.Parent.SetClientSize((w, height))
        # setup boundaries
        self.extr = height - h, 0
        # done
        return

    def _LeftDown(self, event):
        # activate locking
        self.lock = True  
        # record initial control position      
        self.spos = self.GetPosition()
        # record initial mouse location
        self.mpos = wxGetMousePosition()
        # done
        return

    def _Motion(self, event):
        # process only if locked
        if self.lock:
            # get initial locations
            X, Y = self.mpos
            P, Q = self.spos
            # get current mouse position
            x, y = wxGetMousePosition()
            # compute new control position
            p, q = P, Q + y-Y
            # get extrema
            MIN, MAX = self.extr
            # coerce to constraints
            if q < MIN: q = MIN
            if q > MAX: q = MAX
            # set new control position
            self.SetPosition((p, q))
        # done
        return

    def _LeftUp(self, event):
        self._unlock(event)
        return

    def _Leave(self, event):
        self._unlock(event)
        return

    def _unlock(self, event):
        self.lock = False
        return

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

    # GetClientArea as wxGetClientArea
    class myapp(app):

        def Start(self):

            v = vScroll(self.Panel)
            v.SetBackground(imageCollect("bkgd"))
            v.SetFrameContainerHeight(350)

            # Don't use any "Frame.Panel.BackgroundBitmap"
            # when using the vscroll control. This would
            # resize the Frame to the Panel bitmap instead
            # of resizing to the vScroll bitmap.

            # done
            return

    m = myapp()
    m.Run()
