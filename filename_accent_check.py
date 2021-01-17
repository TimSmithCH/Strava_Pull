#!/usr/bin/python
import os
import unicodedata

VERBOSE = False
FORCE = True
#mdir = 'tracks/3_gpx/ski'    # MapTracks directory
mdir = 'tracks'    # MapTracks directory

mpaths = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(mdir)) for f in fn]

# Walk the directory and look for filenames that contain NFD characters
# (decomposed unicode characters work on Mac but not on Unix / Github)
fok = 0
for mpath in mpaths:
    #fname = os.path.basename(mpath)
    fname = mpath
    if VERBOSE : print("Filename {0:48s}".format(fname))
    nfname = unicodedata.normalize('NFC', fname)   # Convert to Unicode composed form
    if nfname != fname :
        print("Found an NFD {0:48s}".format(fname))
        #if FORCE : print("os.rename({},{})".format(fname,nfname))
        if FORCE : os.rename(fname, nfname)
    else :
        fok = fok + 1

print("Found {} correct names".format(fok))
