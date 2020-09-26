#!/usr/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
import os
from pprint import pprint
import argparse

# Parse the arguments
parser = argparse.ArgumentParser(description='Perform a comparison of Strava/GitHub tracks.')
parser.add_argument("type", help="type of activity [bike|hike|run|ski|commute]")
args = parser.parse_args()
track_type = args.type

track_info = {
    "b": {"strava": "Ride", "dir": "bike"},
    "h": {"strava": "Hike", "dir": "hike"},
    "r": {"strava": "Run", "dir": "run"},
    "s": {"strava": "BackcountrySki", "dir": "ski"},
    "c": {"strava": "Ride", "dir": "commute"}
}
#track_type = "s"

# Read the Strava summary data from file
f = open("StravaLog/strava_activity_log.txt", "r")
df = pd.read_csv(f, sep=',', index_col=False, encoding='utf-8')
f.close()

# Extract the type by type from Strava list
sdf = df.loc[df['type'] == track_info[track_type]["strava"]].sort_values('name')
sdf.replace(to_replace=' ', value='_', regex=True, inplace=True)
sdf.replace(to_replace='\(|\)|-|\’|\"', value='_', regex=True, inplace=True)
sdf.replace(to_replace='___', value='_', regex=True, inplace=True)
sdf.replace(to_replace='__', value='_', regex=True, inplace=True)
sdf["name"] = sdf["activity"].astype(str) + "." + sdf["name"]
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
#rdf = mergedStuff.drop(columns=['start_date_local', 'type', 'distance', 'total_elevation_gain', 'elapsed_time', 'device_name', 'id', 'start_latlng'])
#rdf = mergedStuff.drop(columns=['start_date_local', 'type', 'distance', 'total_elevation_gain', 'elapsed_time', 'device_name', 'start_latlng'])
rdf = mergedStuff.drop(columns=['start_date_local', 'type', 'distance', 'total_elevation_gain', 'elapsed_time', 'device_name', 'commute', 'start_latlng'])
all = rdf.sort_values('name')
print("         Strava                   Both                    Git")
for index, row in all.iterrows():
    if row['_merge'] == 'left_only':
        print(row['name'])
        print("StravaLog/Activities/",row['activity'],row['name'])
    elif row['_merge'] == 'right_only':
        print("                                                {}".format(row['name']))
    elif row['_merge'] == 'both':
        print("                        {}".format(row['name']))

#print("Strava only")
#strava = rdf.loc[rdf['_merge'] == 'left_only'].sort_values('name')
#print(strava['name'])
#print("Git only")
#git = rdf.loc[rdf['_merge'] == 'right_only'].sort_values('name')
#print(git['name'])
#print("Both only")
#both = rdf.loc[rdf['_merge'] == 'both'].sort_values('name')
#print(both['name'])
