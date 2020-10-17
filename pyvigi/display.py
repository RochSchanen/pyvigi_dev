#!/usr/bin/python3
# file: display.py
# content:
# created: 2020 April 02
# modified:
# modification:
# author: roch schanen
# website: https://github.com/RochSchanen/
# comment:

# todo: add the led display here
# todo: add the wheel display here
# todo: make the selection of the control
# images using simple names

# wxpython: https://www.wxpython.org/
import wx

# from theme import *

class Pngdisplay(wx.Control):

    def __init__(
        self,
        parent,
        pnglib,
        names):

        # call parent __init__()
        wx.Control.__init__(
            self,
            parent      = parent,
            id          = wx.ID_ANY,
            pos         = wx.DefaultPosition,
            size        = wx.DefaultSize,
            style       = wx.NO_BORDER,
            validator   = wx.DefaultValidator,
            name        = "")

        # PARAMETERS
        self.parent = parent

        # the set of images is defined by a name list
        self.names  = names

        # load the whole set of images:
        self.pngs   = pnglib.Get(names)

        # LOCAL variables

        # status is an index or a name
        self.status = 0

        # get png size from first image
        w, h = self.pngs[self.status].GetSize()
        self.SetSize((w, h))

        # set background color
        # self.SetBackgroundColour(BackgroundColour)

        # BINDINGS
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._onEraseBackground)
        self.Bind(wx.EVT_PAINT, self._onPaint)

        # done
        return

    def _onEraseBackground(self, event):
        # bypass method: no flicker
        pass 

    def _onPaint(self, event):
        v = self.status
        if isinstance(v, int): n = v
        if isinstance(v, str): n = self.names.index(v)
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.pngs[n], 0, 0)
        return

    def SetValue(self, Value):
        self.status = Value
        self.Refresh()
        return

    def GetValue(self):
        return self.status

# class Text(wx.StaticText):
# """
#     comment
# """
#     def __init__(self, parent, text):

#         wx.StaticText.__init__(self,
#             parent = parent,
#             label  = text,
#             id     = wx.ID_ANY,
#             pos    = wx.DefaultPosition,
#             size   = wx.DefaultSize,
#             style  = wx.NO_BORDER,
#             name   = wx.TextCtrlNameStr)

#         self.SetForegroundColour(TextColour)
#         self.SetBackgroundColour(BackgroundColour)

#         return

if __name__ == "__main__":

    print("file: display.py (from pyvigi package)")
    print("content: ")
    print("created: 2020 03 21")
    print("author: Roch Schanen")
    print("comment:")
