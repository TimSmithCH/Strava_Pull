#!/usr/bin/python
import os
import fnmatch
import re

VERBOSE = False
mtdir = '/Users/Tim/Code/Git/MapTracks/tracks'    # MapTracks directory
mdir = mtdir + "/3_gpx"
gdir = mtdir + "/2_geojson"

mpaths = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(mdir)) for f in fn]
# Retain only GPX files from the mpaths list
mpaths = [ file for file in mpaths if file.endswith('.gpx') ]

gpaths = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(gdir)) for f in fn]
# Retain only GeoJson files from the gpaths list
gpaths = [ file for file in gpaths if file.endswith('.geojson') ]

print("\033[91m > Initially {} GPX Files to match to {} GeoJson files\033[00m".format(len(mpaths),len(gpaths)))

# Walk the GPX directory and look for matches in GeoJson directory
for mpath in mpaths:
    # GPX name from filename
    bname = os.path.basename(mpath)
    fname = os.path.splitext(bname)[0]
    if VERBOSE : print("GPX Filename {0:48s}".format(fname))
    # Construct GeoJson file to find
    dtype = os.path.split(os.path.split(mpath)[0])[1]
    gfile = gdir + "/" + dtype + "/" + fname + ".geojson"
    if VERBOSE : print("GeoJson Filename {0:48s}".format(gfile))
    if os.path.isfile(gfile):
        try:
            gpaths.remove(gfile)
            if VERBOSE : print("Matched {0:48s}".format(gfile))
        except:
            print("Failed to remove {0:48s}".format(gfile))
    else:
        print("Unmatched {0:48s}".format(fname))

print("\033[92m > After match  unmatched {} GeoJson files\033[00m".format(len(gpaths)))

for gpath in gpaths:
    print(gpath)
