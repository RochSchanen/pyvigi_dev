#!/usr/bin/python3
# file: t000.py
# content: test pyvigi local installation
# created: 2020 septemeber 27 Sunday
# modified:
# modification:
# author: roch schanen
# comment:
#   make this file executable: ">chmod u+x ./t000.py"
#   usage : ">./t000.py"

if __name__ == "__main__":

    import sys

    print("file: t000.py")
    print("content: test pyvigi local installation")
    print("created: 2020 septemeber 27 Sunday")
    print("author: roch schanen")
    print("comment:")
    print("run Python3:" + sys.version)

    import pyvigi

    print(f"pyvigi version {pyvigi.version}")

# >./pyvigi_dev/t000.py 
# file: t000.py
# content: test pyvigi local installation
# created: 2020 septemeber 27 Sunday
# author: roch schanen
# comment:
# run Python3:3.8.2 (default, Jul 16 2020, 14:00:26) 
# [GCC 9.3.0]
# pyvigi version 0.0.2
