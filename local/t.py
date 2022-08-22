#!/usr/bin/python3
# file: t.py
# content: test current installed version
# created: 2020 septemeber 27 Sunday
# modified: 2022 August 22 Monday
# modification: use tools module
# author: roch schanen
# comment:

if __name__ == "__main__":

    from pyvigi.tools import header
    header() # display header

    from sys import version
    print(f"run Python version {version.split(' ')[0]}")

    from pyvigi import version
    print(f"using pyvigi version {version}")
