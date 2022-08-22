#!/usr/bin/python3
# file: base.py
# content: App class definition
# created: 2020 March 21
# modified: 2022 August 22
# modification: use tools module
# author: Roch Schanen
# repository: https://github.com/RochSchanen/pyvigi_dev
# comment:

# wxpython: https://www.wxpython.org/
import wx

""" 
    
    Quick App:
    
    On instantiating an "App" object, a frame is
    automatically created and a panel container
    too.
    
    A "BackgroundBitmap" is created and used to
    paint the panel background when "Refreshed".

    Importantly, the "BackgroundBitmap" is used
    as a canvas by the layout class to draw the
    App decors.

"""

# Quick Panel
class _basePanel(wx.Panel):

    def __init__(self, parent):

        wx.Panel.__init__(
            self,
            parent = parent,
            id     = wx.ID_ANY,
            pos    = wx.DefaultPosition,
            size   = wx.DefaultSize,
            style  = wx.NO_BORDER,
            name   = "")

        # BackgroundBitmaps are used to draw decors
        self.BackgroundBitmap = None

        # bind paint event
        self.Bind(wx.EVT_PAINT, self._OnPaint)

        # done
        return

    def _OnPaint(self, event):

        # re-draw BackgroundBitmap if defined
        if self.BackgroundBitmap: 

            # "DCPaint" is used here.
            # maybe "BufferedPaintDC" should be used instead.
            # todo: explore documentation
            dc = wx.PaintDC(self)
            dc.DrawBitmap(self.BackgroundBitmap, 0, 0)

        #done
        return

# Quick Frame
class _baseFrm(wx.Frame):

    def __init__(self):

        wx.Frame.__init__(
            self,
            parent = None,
            id     = wx.ID_ANY,
            title  = "",
            pos    = wx.DefaultPosition,
            size   = wx.DefaultSize,
            style  = wx.DEFAULT_FRAME_STYLE
                    ^ wx.RESIZE_BORDER
                    ^ wx.MAXIMIZE_BOX,
            name   = "")

        # create the panel
        self.Panel = _basePanel(self)

        # done
        return

# When _ESCAPE = True you can use the
# ESCAPE key  to quit the Application
# (This is used for debbugging)
_ESCAPE = True

# Quick App
class App(wx.App):

    def OnInit(self):
        # create reference to App
        self.App = self
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
        self.Bind(wx.EVT_KEY_DOWN, self._OnKeyDown)
        # show the frame
        self.Frame.Show(True)
        # done
        return True

    def Start(self):
        # This has to be overloaded by the
        # user's start up code
        pass

    def _OnKeyDown(self, event):
        
        key = event.GetKeyCode()

        # catch the ESCAPE key and exit the app
        # when the _ESCAPE flag is set. This is
        # used for development purposes. It will
        # be removed at later time.

        if _ESCAPE:
            if key == wx.WXK_ESCAPE:
                wx.Exit()
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
