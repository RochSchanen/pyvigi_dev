#!/usr/bin/python3
# file: buttons.py
# content:
# created: 2020 April 03
# modified: 2022 August 22
# modification: use tools module
# author: roch schanen
# website: https://github.com/RochSchanen/
# comment:

# constants, methods and classes are imported individually
# this allows to identify clearly the packages usage

# from wxpython: https://www.wxpython.org/

# wx event constants
from wx import PostEvent            as wxPostEvent
from wx import EVT_LEFT_DOWN        as wxEVT_LEFT_DOWN
from wx import EVT_LEFT_UP          as wxEVT_LEFT_UP
from wx import EVT_LEFT_DCLICK      as wxEVT_LEFT_DCLICK
from wx import EVT_ENTER_WINDOW     as wxEVT_ENTER_WINDOW
from wx import EVT_LEAVE_WINDOW     as wxEVT_LEAVE_WINDOW
from wx import EVT_MOUSEWHEEL       as wxEVT_MOUSEWHEEL

# wx event methods
from wx.lib.newevent import NewEvent as wxNewEvent

# from pyvigi:
from pyvigi.display import bitmapControl

"""

    this library is still under heavy development
    it is developed in concurence with the pylvinox panel
    that should control and monitor the kelvinox box

"""

# the _btn class is used as a base for the following buttons
# (except for the wheel control that is directly based on the bitmapControl)

class _btn(bitmapControl):

    def __init__(
        self,
        parent,
        images,
        names = None):

        bitmapControl.__init__(
            self,
            parent = parent,
            images = images,
            names  = names)

        # locals
        self.radio = None
        self.ctr   = None
        self.evt   = None

        # bindings
        self.Bind(wxEVT_LEFT_DOWN,   self._onMouseDown)

        # capture double clicks events as secondary single clicks
        self.Bind(wxEVT_LEFT_DCLICK, self._onMouseDown)

        # call child _start() method
        self._start()

        # done
        return

    def _start(self):
        # to overload
        pass

    # radio feature
    def _clear(self):
        # to overload
        pass

    # on EVT_LEFT_DOWN, the event.skip()
    # method must be called to preserve
    # the focus event to be processed
    def _onMouseDown(self, event):
        event.Skip() # allow focus events
        return

    # Bind the event to the parent handler
    def BindEvent(self, handler):
        # "handler" is a reference to the handler method
        # usually defined by the parent class
        self.ctr, self.evt = wxNewEvent()
        self.GetParent().Bind(self.evt, handler)
        return

    # Sends a event to parent using "status" as parameter
    def SendEvent(self):
        if self.ctr:
            event = self.ctr(caller=self, status=self.status)
            wxPostEvent(self.GetParent(), event)
        return

# #################################################### SWITCH

# set and cleared alternatively on mouse down
# an event is sent each time
# there is no undo gesture
#
# png binary weight:
# 2^0 = 1 = on
#
# png order:
# 0 = off
# 1 = on

# to do: integration in a radio group

class Switch(_btn):

    def _onMouseDown(self, event):
        event.Skip() # allow focus events
        self.status ^= 1
        self.Refresh()
        self.SendEvent()
        return

# #################################################### LED SWITCH

# set and cleared alternatively on mouse up
# send a single event on release
# there is a cancellation gesture: leaving the button without mouse release
#
# png binary weight:
# 2^0 = 1 = on
# 2^1 = 2 = pressed
#
# png order:
# 0 = off released
# 1 = on  released
# 2 = off pressed
# 3 = on  pressed

class LEDSwitch(_btn):

    def _start(self):
        self.lock = False
        self.Bind(wxEVT_LEFT_UP, self._onMouseUp)
        self.Bind(wxEVT_LEAVE_WINDOW, self._onMouseLeave)
        return

    def _onMouseDown(self, event):
        event.Skip() # allow focus events
        self.lock = True
        if self.radio:
            self.radio.Select(self)
        self.status |= 2
        self.Refresh()
        return

    def _onMouseUp(self, event):
        if self.lock:
            self.lock = False
            self.status &= 1
            self.status ^= 1
            self.Refresh()
            self.SendEvent()
        return

    def _onMouseLeave(self, event):
        if self.lock:
            self.lock = False
            self.status &= 1
            self.Refresh()
        return

    # called by radio group
    def _clear(self):
        if self.status:
            self.status = 0
            self.Refresh()
            self.SendEvent()
        return

    def SetValue(self, Value):
        self.status = Value
        self.Refresh()
        return

# #################################################### WHEEL

# a full explanation is necessary here

class Wheel(bitmapControl):

    def __init__(
        self,
        parent,
        images,
        hover = None):

        # concatenate hover images
        if hover:
            images += hover
            self.hover = True
        else:
            self.hover = False

        bitmapControl.__init__(
            self,
            parent = parent,
            images = images,
            names  = None)
        
        # LOCALS
        self.rotation = +1    # direction
        self.reset = None     # cancel operation
        self.radio = None     # radio group handle
        self.ctr   = None     # control parent
        self.evt   = None     # event handler
        self.overflow = 0     # overflow flag
        self.n = len(images)  # full cycle number
        if self.hover:        # subtract hover images
            self.n >>= 1 
        
        # BINDINGS
        self.Bind(wxEVT_ENTER_WINDOW, self._onMouseEnter)
        self.Bind(wxEVT_LEAVE_WINDOW, self._onMouseLeave)
        self.Bind(wxEVT_MOUSEWHEEL,   self._onMouseWheel)
        return

    def _onMouseEnter(self, event):
        # event.Skip() # unnecessary?
        # safely upgrade to hover
        m = self.status % self.n
        if self.hover: m += self.n
        # update state
        self.status = m
        # done
        self.Refresh()
        return

    def _onMouseLeave(self, event):
        # coerce to normal
        m = self.status % self.n
        # update state
        self.status = m
        # done
        self.Refresh()
        return

    def _onMouseWheel(self, event):
        # save state if cancellation
        self.reset = self.status
        self.overflow = 0
        # coerce to normal
        m = self.status % self.n
        # apply wheel action
        r = event.GetWheelRotation()
        if r > 0: self.step = +self.rotation
        if r < 0: self.step = -self.rotation
        m += self.step
        # set overflow flag
        if m < 0       : self.overflow = -1
        if m > self.n-1: self.overflow = +1
        # coerce (useful only when overflow)
        m %= self.n
        # upgrade to hover
        if self.hover:
            m += self.n
        # update state
        self.status = m
        # done
        self.SendEvent()
        # the caller should send a "self.Refresh()"
        # after evaluating the new state that should
        # be given to the wheel.
        return

    def SetRotation(self, Value):
        # +1 is forward
        # -1 is inverse
        self.rotation = Value
        return

    def SetValue(self, Value):
        # get value
        m = int(Value)
        # upgrade to hover
        if self.status > self.n:
            m += self.n
        # update
        self.status = m
        self.reset  = m
        self.Refresh()
        return

    def GetValue(self):
        return self.status % self.n

    def Reset(self):
        self.status = self.reset
        # self.Refresh()
        return

    # Bind the event to the parent handler
    def BindEvent(self, handler):
        # "handler" is a reference to the handler method
        # defined in the parent class
        self.ctr, self.evt = wxNewEvent()
        self.GetParent().Bind(self.evt, handler)
        return

    # Sends a event to parent using "caller" and status"
    # for parameters: caller refers to whom sends the event
    def SendEvent(self):
        if self.ctr:
            event = self.ctr(caller=self, status=self.status)
            wxPostEvent(self.GetParent(), event)
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
   
    # derive a new class from app
    class myapp(app):

        def Start(self):

            # manually setup the background image of myapp
            PANELS = imageCollect("panels")
            self.Panel.BackgroundBitmap = imageSelect(PANELS, "medium")[0]
            W, H = self.Panel.BackgroundBitmap.GetSize()

            SWITCHES = imageCollect("switches")

            # add switch
            self.p = Switch(self.Panel,
                imageSelect(SWITCHES, "blank"))
            w, h = self.p.GetSize()
            x, y = (W+0*w)/2, (H-3*h)/2
            self.p.SetPosition((int(x), int(y)))
            self.p.BindEvent(self.updatePush)

            # add green led switch to the panel
            self.l = LEDSwitch(self.Panel,
                imageSelect(SWITCHES, "green"))
            x, y = (W-3*w)/2, (H-0*h)/2
            self.l.SetPosition((int(x), int(y)))
            self.l.BindEvent(self.updateSwitch)

            # add wheel to the panel
            WHEEL = imageCollect("generator", "digit")
            self.whl = Wheel(self.Panel, 
                imageSelect(WHEEL, "normal"),
                imageSelect(WHEEL, "hover"))
            x, y = (W+3*w)/2, (H-0*h)/2
            self.whl.SetPosition((int(x), int(y)))
            self.whl.BindEvent(self.updateWheel)

            # done
            return
    
        def updatePush(self, event):
            print(["OFF", "ON"][event.caller.GetValue()])
            return

        def updateSwitch(self, event):
            print(event.status)
            return

        def updateWheel(self, event):
            print(event.caller.GetValue())
            event.caller.Refresh()
            return

    # instanciate myapp
    m = myapp()

    # run myapp
    m.Run()
