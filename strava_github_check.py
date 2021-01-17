#!/usr/bin/python
import os
import fnmatch
import gpxpy
import re
import argparse

def extract_time(fname):
    ftime = ""
    with open(fname, 'r+') as filecont:
        for line in filecont:
            match = re.search(r'<time>(.+)</time>\n', line)
            if match:
                ftime = match.group(1)
                break;
    filecont.close()
    return ftime

# Parse the arguments
parser = argparse.ArgumentParser(description='Ensure all Strava tracks have been copied to GitHub.')
parser.add_argument("year", help="year of activity [all|14|15|16|18|19|20|21]")
parser.add_argument("verbosity", help="choose verbosity level [0|1|2|3|4]")
args = parser.parse_args()
year = args.year
verbosity = int(args.verbosity)

if year == 'a':
    sdir = '/Users/Tim/Code/ACTION/StravaPull/StravaLog'
else:
    sdir = '/Users/Tim/Code/ACTION/StravaPull/StravaLog/20'+year

mdir = '/Users/Tim/Code/Git/MapTracks/tracks/3_gpx'    # MapTracks directory

# Scan Strava download directory
print("1> Create dict of Strava file sizes")
print("   Scanning {0:48s}".format(sdir))
spaths = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(sdir)) for f in fn]
# Retain only GPX files from the spaths list
spaths = [ file for file in spaths if file.endswith('.gpx') ]
# Create list of (time,pathname) pairs and convert to dictionary
stimes = []
for spath in spaths:
    ftime = extract_time(spath)
    if ftime:
        stimes.append([ftime, spath])
dict_stimes = dict(stimes)
# Check that all the times are unique
if len(dict_stimes) > len(set(dict_stimes.values())) :
    print("ERROR: times are not unique")
    rev_dict = {}
    for key, value in dict_stimes.items():
        rev_dict.setdefault(value, set()).add(key)
    result = filter(lambda x: len(x)>1, rev_dict.values())
    print(*result,sep='\n')

# Scan MapTracks directory from GitHub
print("2> Create dict of MapTrack file sizes")
print("   Scanning {0:48s}".format(mdir))
mpaths = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(mdir)) for f in fn]
# Retain only GPX files from the mpaths list
mpaths = [ file for file in mpaths if file.endswith('.gpx') ]
# Create list of (time,pathname) pairs and convert to dictionary
mtimes = []
for mpath in mpaths:
    ftime = extract_time(mpath)
    if ftime:
        mtimes.append([mpath, ftime])
dict_mtimes = dict(mtimes)
# Check that all the times are unique
if len(dict_mtimes) > len(set(dict_mtimes.values())) :
    print("ERROR: times are not unique")
    rev_dict = {}
    for key, value in dict_mtimes.items():
        rev_dict.setdefault(value, set()).add(key)
    result = filter(lambda x: len(x)>1, rev_dict.values())
    print(*result,sep='\n')

print("\033[91m > Initially {} Strava Files to match to {} MapTrack files\033[00m".format(len(spaths),len(mpaths)))

# Walk the Strava directory and look for same size file in MapTracks directory
print("2> Iterate through StravaPull directory and look for MapTrack matches")
for mpath in mpaths:
    if verbosity >= 4 : print("Looking for {0:48s}".format(mpath))
    if os.path.isfile(mpath):
        mtime = dict_mtimes.get(mpath)
        sname = dict_stimes.get(mtime)
        if sname != None:
            syear = os.path.split(os.path.split(sname)[0])[1]
            mtype = os.path.split(os.path.split(mpath)[0])[1]
            sbname = os.path.basename(sname)
            mbname = os.path.basename(mpath)
            try:
                spaths.remove(sname)
                if verbosity >= 2 : print("Matched ({0})-{1} to ({2})-{3}".format(syear, sbname, mtype, mbname))
            except:
                print("Failed to remove {0:48s}".format(spath))
        else:
            if verbosity >= 3 : print("Unmatched {0:48s}".format(spath))

print("\033[92m > After matching; unmatched {} Strava files\033[00m".format(len(spaths)))

if verbosity >= 1 :
    for spath in spaths:
        print(spath)
