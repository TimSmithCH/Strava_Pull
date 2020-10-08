#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import os
from pprint import pprint
import argparse

# Parse the arguments
parser = argparse.ArgumentParser(description='Perform a comparison of Strava/GitHub tracks.')
parser.add_argument("type", help="type of activity [bike|hike|run|ski|commute]")
parser.add_argument("path", help="full path of strava only activities to use in a copy [path|none]")
args = parser.parse_args()
track_type = args.type
path = args.path

track_info = {
    "b": {"strava": "Ride", "dir": "bike"},
    "h": {"strava": "Hike", "dir": "hike"},
    "r": {"strava": "Run", "dir": "run"},
    "s": {"strava": "BackcountrySki", "dir": "ski"},
    "c": {"strava": "Ride", "dir": "commute"}
}

# Read the Strava summary data from file
f = open("StravaLog/strava_activity_log.txt", "r")
df = pd.read_csv(f, sep=',', index_col=False, encoding='utf-8')
f.close()

# Extract the list by type from Strava list
sdf = df.loc[df['type'] == track_info[track_type]["strava"]].sort_values('name')
sdf.replace(to_replace=' ', value='_', regex=True, inplace=True)
sdf.replace(to_replace='\(|\)|-|\’|\"', value='_', regex=True, inplace=True)
sdf.replace(to_replace='___', value='_', regex=True, inplace=True)
sdf.replace(to_replace='__', value='_', regex=True, inplace=True)
# Recreate the actual download filename
sdf["name"] = sdf["activity"].astype(str) + "." + sdf["name"]
# Separate the Rides into Commute/Play
if track_type == 'b':
    sdf = sdf[sdf.commute != True]
elif track_type == 'c':
    sdf = sdf[sdf.commute == True]
  
#print(sdf)

# Create list of files already in GitHub
files = []
strava_dir = "/Users/Tim/Code/Git/MapTracks/tracks/3_gpx/" + track_info[track_type]["dir"] + "/"
#for entry in os.scandir('/Users/Tim/Code/Git/MapTracks/tracks/3_gpx/hike/'):
for entry in os.scandir(strava_dir):
    if entry.is_file():
        files.append(entry.name)
gdf = pd.DataFrame(files, columns=['name'])
gdf.replace(to_replace='.gpx', value='', regex=True, inplace=True)
#print(gdf)

# Now try and diff using a merge technique
mergedStuff = pd.merge(sdf, gdf, on=['name'], how='outer', indicator=True)
rdf = mergedStuff.drop(columns=['start_date_local', 'type', 'distance', 'total_elevation_gain', 'elapsed_time', 'device_name', 'commute', 'start_latlng'])
all = rdf.sort_values('name')
print("         Strava                   Both                    Git")
for index, row in all.iterrows():
    if row['_merge'] == 'left_only':
        if path != "full": print(row['name'])
        if path == "full": print("cp StravaLog/Activities/{}.gpx tracks/3_gpx/commute/".format(row['name']))
        #if path == "full": print("StravaLog/Activities/{}.gpx".format(row['name']))
    elif row['_merge'] == 'right_only':
        if path != "full": print("                                                {}".format(row['name']))
    elif row['_merge'] == 'both':
        if path != "full": print("                        {}".format(row['name']))

#print("Strava only")
#strava = rdf.loc[rdf['_merge'] == 'left_only'].sort_values('name')
#print(strava['name'])
#print("Git only")
#git = rdf.loc[rdf['_merge'] == 'right_only'].sort_values('name')
#print(git['name'])
#print("Both only")
#both = rdf.loc[rdf['_merge'] == 'both'].sort_values('name')
#print(both['name'])
