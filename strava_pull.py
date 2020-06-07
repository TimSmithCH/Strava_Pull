#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import stravalib
from stravaweblib import WebClient, DataFormat
import pandas as pd
import datetime
#from pprint import pprint
#import requests
import glob

# stravalib assumes logging has been configured
logging.basicConfig(filename='StravaLog/Strava_Pull.log',level=logging.INFO)

# Read all Strava secrets from file, so that they arent in the code!
OAUTH_TOKEN,EMAIL,PASSWORD = open('client.secret').read().strip().split(',')
LIMIT = 1000
my_cols =['name',
          'start_date_local',
          'type', 
          'distance',
          'total_elevation_gain',
          'elapsed_time',
          'device_name',
          'start_latlng']
types = ['time', 'distance', 'latlng', 'altitude', 'velocity_smooth', 'moving', 'grade_smooth', 'temp']

print("Authenticate with Strava")
# stravalib only needs token
#client = stravalib.client.Client(access_token=TOKEN)
# stravaweblib needs token and uname/pwd to do web scrapping
client = WebClient(access_token=OAUTH_TOKEN, email=EMAIL, password=PASSWORD)

# Retrieve the list of activities from Strava
print("Retrieve max.",LIMIT," activities")
#activities = client.get_activities(after="2020-01-01T00:00:00Z",before="2021-01-01T00:00:00Z", limit=LIMIT)
activities = client.get_activities(after="2018-01-01T00:00:00Z",before="2018-06-01T00:00:00Z", limit=LIMIT)
#activities = client.get_activities(limit=LIMIT)

# Collate the summary data
summary_data = []
for activity in activities:
    my_dict = activity.to_dict()
    summary_data.append([my_dict.get(x) for x in my_cols])

# Activities contain limited summary data, for complete summary data need to
# retrieve each activity individually
#summary_data = []
#for activity in activities:
#    my_dict = activity.to_dict()
#    act = client.get_activity(activity.id)
#    my_dict = act.to_dict()
#    data.append([my_dict.get(x) for x in my_cols])

# Store the summary data in a file
df = pd.DataFrame(summary_data, columns=my_cols)
print("Found ",df.shape[0]," to retrieve")
print(df.head(10))
f = open("StravaLog/strava_activity_log.txt", "w")
df.to_csv(f, sep=',', index=False, header=True, encoding='utf-8')
f.close()

# Retrieve the data streams for each activity from Strava
#for activity in activities:
#    stream = client.get_activity_streams(activity.id, types=types, series_type='time')
#    sdf = pd.DataFrame()
#    for item in types:
#        if item in stream.keys():
#            sdf[item] = pd.Series(stream[item].data,index=None)
#        sdf['act_id'] = activity.id
#        sdf['act_startDate']= pd.to_datetime(activity.start_date)
#        sdf['act_name'] = activity.name
#        fname = "StravaLog/Activities/%d" % activity.id
#        sf = open(fname, "w")
#        sdf.to_csv(sf, sep=',', index=False, header=True, encoding='utf-8')
#        sf.close()

# Retrieve the original data files uploaded for each activity from Strava
# Data format may be ORIGINAL, TCX or GPX
data_fmt = 'fit'
#data_fmt = 'gpx'
data = []
for activity in activities:
    # Skip if there are existing files
    fpat = "StravaLog/Activities/{0}.*.{1}".format(activity.id, data_fmt)
#    print("Searching for {0}".format(fpat))
    matched = glob.glob(fpat)
    if matched:
        print("Found {0} so skipping download".format(matched))
    else:
        try:
            data = client.get_activity_data(activity.id, fmt=DataFormat.ORIGINAL)
            # Save the activity data to disk using the server-provided filename
            fname = "StravaLog/Activities/{0}.{1}".format(activity.id, data.filename)
            print("Downloaded {0}".format(fname))
            with open(fname, 'wb') as f:
                for chunk in data.content:
                    if not chunk:
                        break
                    f.write(chunk)
        except stravalib.exc.Fault as e:
            print("ERROR trying to download {0} {1}".format(activity.id,activity.name))

#--- Alternatives ---
#    url = "https://www.strava.com/activities/%d/export_original" % activity.id
#    r = requests.get(url)
#    fname = "StravaLog/Activities/%d" % activity.id
#    open(fname, 'wb').write(r.content)
#
#    import requests as r
#    url = 'https://www.strava.com/api/v3/activities/108838256'
#    header = {'Authorization': 'Bearer access_token'}
#    r.get(url, headers=header).json()
