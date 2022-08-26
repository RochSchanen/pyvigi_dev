#!/usr/bin/python3
# file: timer.py
# content:
# created: 2022 August 24
# modified:
# modification:
# author: roch schanen
# website: https://github.com/RochSchanen/
# comment:

# constants, methods and classes are imported individually
# this allows to identify clearly the packages usage

# from wxpython: https://www.wxpython.org/

from wx import Timer as wxTimer
from wx import EVT_TIMER as wxEVT_TIMER

"""

    This is a new library which will require more
    experience to develop properly. Some more work
    will be done with a device using pyDAQmx library
    Proper integration with the library need to be
    investigated. Using the timer requires the app
    to run.

"""

# collection of running timers
_timers = {}

# setup one timer
def timeloop(owner, eventHandler, Period):

    i = 0
    n = f"TIMER{i:3}"
    while n in _timers.keys():
        i += 1
        n = f"TIMER{i:3}"

    # create timer
    _timers[n] = wxTimer()

    # bind timer to task
    owner.Bind(wxEVT_TIMER, eventHandler, _timers[n])
    
    # start automatically
    _timers[n].Start(Period)

    # done
    return
    
if __name__ == "__main__":

    from pyvigi.tools import header
    header()

    from sys import version
    print(f"run Python version {version.split(' ')[0]}")

    from pyvigi import version
    print(f"using pyvigi version {version}")

    from pyvigi.base import App

    # derive a new class from App
    class myapp(App):

        def Start(self):
            # counter
            self.n = 0
            # setup timer and start
            timeloop(self, self.update, 100)
            # done
            return

        def update(self, event):
            # increment
            self.n += 1
            # display
            print(f" {self.n:02}", end = "")
            # done
            return 
    
    # instanciate myapp
    m = myapp()

    # run amyapp
    m.Run()
