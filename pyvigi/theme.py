#!/usr/bin/python3
# file: theme.py
# content:
# created: 2020 April 05
# modified:
# modification:
# author: roch schanen
# website: https://github.com/RochSchanen/
# comment:

# constants, methods and classes are imported individually
# this allows to identify clearly the packages usage

# from standard packages:
from sys import path                    as syspath
from os.path import isfile              as osisfile

# from wxpython: https://www.wxpython.org/

# wx bitmap methods
from wx import Bitmap                   as wxBitmap
from wx import BITMAP_TYPE_PNG          as wxBITMAP_TYPE_PNG
from wx import Rect                     as wxRect

"""

    The role of imageCollect is to collect a list
    of references to all the images found in a png
    file. The list is defined in the png.txt file.
    (filtering can be applied)

    The role of imageSelect is to select from the image
    collection a subset of images (by using keywords).
    The selection is a list of pointers to the images

    todo: add a method to set the app background image?

    todo: add more examples to illustrate the functionaly
    of the collection and selection methods.

    todo: add resources within the package.

"""

############################################ PATHS

# Get path to main application:

_APP_PATH = syspath[0]

# Resources are searched first
# in the sub-folder "resources"
# that may or not be present in
# the application folder. secondly
# resources are searched in the
# application folder itself. more
# path can be added to the list by
# the user.

_PATHS = [
    f'{_APP_PATH}/resources',   # app resources directory
    f'{_APP_PATH}',             # app local directory
    ]

# the last path added has precedence on the previous ones.
# this allow a user to easily add his own ressource files.

# the path selection, addition, substraction could
# be implemented to choose one theme amongst multiple others

# debug flag
_DEBUG = False

def DEBUG(switch):

    if switch in ["ON", "On", "on", True, 1]:
        _DEBUG = True

    if switch in ["OFF", "Off", "off", False, 0]:
        _DEBUG = False  

    if _DEBUG:
        print(f"_DEBUG flag is on")
        print(f"_APP_PATH: {_APP_PATH}")
        print(f"_PATHS:")
        for p in _PATHS:
            print(f"{' ':3}{p}")
    
    #done 
    return

# get a valid path
def _findpath(path):
    
    # default
    filepath = None
    
    # the passed parameter as priority
    # over the search results.

    if osisfile(path):
        filepath = path
    
    else:

        # look through all paths
        # and update "filepath"
        # anytime a valid path is
        # found. Thus, the last
        # path found will be the
        # path returned. if no
        # valid path is found the
        # function returns "None".

        for p in _PATHS:
            fp = f"{p}/{path}" 
            if osisfile(fp):
                filepath = fp

    # done
    return filepath


############################################ COLLECT

# collect data list from the .txt file
def _findpngs(name, *args):

    # load the definition file
    f = open(_findpath(f'{name}.png.txt'))
    if not f: return None
    t = f.read()
    f.close()

    # build library
    library = []
    for s in t.split('\n'):
        if not s: continue               # skip empty line
        if s.strip()[0] == '#': continue # skip commnent
        l = s.split(',')                 # parse at coma

        # extract values
        offset   = int(l[0]), int(l[1]) # offset values
        grid     = int(l[2]), int(l[3]) # grid values
        size     = int(l[4]), int(l[5]) # size values
        position = int(l[6]), int(l[7]) # position values

        # build tags list
        taglist = []
        for t in l[8:]:
            taglist.append(t.strip())

        # group geometric parameters
        geometry = offset, grid, size, position

        # record all parameters
        library.append((geometry, taglist))

    # collect pngs using the taglist as filter:
    # images which tags list contains all of
    # the arguments in args is added to the list  
    collection = []
    for i in library:
        geometry, taglist = i

        # filter
        valid = True
        for a in args:
            if a not in taglist:
                valid = False

        # add item to collection
        if valid:

            # remove filter tags from taglist
            for a in args:
                taglist.remove(a)

            # collect
            collection.append((geometry, taglist))

    # done
    return collection

# extract and collect bitmaps from a png file
def imageCollect(name, *args):

    # check image filepath
    fp = _findpath(f'{name}.png')
    if _DEBUG: print(f"filepath {fp}")
    if not fp: return None

    # load the bitmap file
    bm = wxBitmap(fp, wxBITMAP_TYPE_PNG)
    if _DEBUG: print(f"bitmap {bm}")

    # get image data from .txt file
    collection = _findpngs(name, *args)
    if _DEBUG: print(f"collection {collection}")
    if not collection: return None

    # clip images from the bitmap file
    # and add them to the collection
    images, taglists = [], []
    for geometry, taglist in collection:

        # get geometry
        offset, grid, size, position = geometry        

        # get parameters
        W, H = bm.GetSize()
        X, Y = offset
        p, q = grid
        w, h = size
        m, n = position                

        # compute grid size
        P, Q = W/p, H/q

        # compute clipping origin
        x = (m-1)*P + (P-w)/2 + X
        y = (n-1)*Q + (Q-h)/2 + Y
        
        # set clipping geometry
        Clip = wxRect(int(x), int(y), w, h)
        
        # clip and record
        images.append(bm.GetSubBitmap(Clip))
        taglists.append(taglist)

    # one image in the list: return a single image
    if len(images) == 1:
        return images[0]

    # more than one image: return (image, tags) list
    subCollection = []
    # make image list
    for i, t in zip(images, taglists):
        subCollection.append((i, t))

    # done
    return subCollection

############################################ SELECT

def imageSelect(collection, *args):

    # to do: None => all images returned

    # convert args to list
    # for ease of data handling
    args = list(args)

    # grab last argument if it is a list
    sortlist = None
    if args:
        if isinstance(args[-1], list):
            sortlist = args.pop()

    subCollection = []

    # filter images collection
    for image, taglist in collection:

        valid = True
        for a in args:
            if a not in taglist:
                valid = False

        if valid:
            
            # the taglist object must be
            # left unchanged so that the
            # collection object keeps its
            # integrity
            tagsublist = taglist.copy()

            for a in args:
                tagsublist.remove(a)

            subCollection.append((image, tagsublist))

    images = []

    # return an image list in the
    # order given by sortlist
    if sortlist:
        for a in sortlist:
            for i, t in subCollection:
                if a in t:
                    images.append(i)
        # done
        return images

    # build image list
    for i, t in subCollection:
        images.append(i)

    # one image in the list: return a single image
    if len(images) == 1:
        return images[0]

    return images

############################################ TEST

if __name__ == "__main__":

    from pyvigi.tools import header
    header()

    from sys import version
    print(f"run Python version {version.split(' ')[0]}")

    from pyvigi import version
    print(f"using pyvigi version {version}")

    # DEBUG("True")

    from pyvigi.base import app

    # derive a new class from app
    class myapp(app):

        def Start(self):
            # collect images from "Panels.png"
            img = imageCollect("panels", "large")
            # manually setup the background image of myapp
            self.Panel.BackgroundBitmap = img
            # done
            return
    
    # instanciate myapp
    m = myapp()

    # run myapp
    m.Run()
