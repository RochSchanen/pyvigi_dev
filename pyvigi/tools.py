#!/usr/bin/python3
# file: tools.py
# content: small tool box
# created: 2022 august 22 Monday
# modified:
# modification:
# author: roch schanen
# comment:

# display file header of main calling script

def header():

    from os.path import realpath
    from sys import argv

    # get main script content
    fp = realpath(argv[0])  # file path
    fh = open(fp, 'r')      # file handle
    ft = fh.read()          # file text
    fh.close()              # done

    # print lines while begin with #
    L = ft.split('\n')
    for l in L[1:]:
        if not l: break
        if not l[0]=="#": break
        print(l)

    # done
    return
