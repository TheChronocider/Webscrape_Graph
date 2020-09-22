#!/usr/bin/env python
# coding: utf-8

# In[26]:


import datetime
import os
import csv
import requests


# In[32]:


def get_latest(fFname):    
    if os.path.exists(fFname):
        with open(fFname) as fd:
            # Read CSV
            reader = csv.reader(fd, delimiter =',')
            #skip header
            next(reader)

            #Get the latest input
            latest = -1

            for element in reader:
                if float(element[0]) > latest:
                    latest = float(element[0])

            return latest
        
    # Create file if not existing
    with open(fFname, 'w', newline='') as fd:
        writer = csv.writer(fd)
        # Write Headers
        writer.writerow(["Time Stamp", "Date", "Price"])
    return -1


# In[33]:


# Location of JSON containing petrol price values for canberra
url = 'https://www.aip.com.au/aip-api-request?api-path=public/api&call=retailNswUlp&location=Canberra'

# File to save
file = 'historic_fuel_data.csv'


# In[34]:


# Grabbing data as JSON and the specific points: ["series"][0]['data']
data = requests.get(url).json()["series"][0]['data']


# In[35]:


# Grab the latest timestamp
latest = get_latest(file)

with open(file, 'a', newline='') as fd:
    # Create filewriter
    writer = csv.writer(fd)
    
    for point in data:
        # Saved timestamps are in milliseconds
        timestamp = float(point[0])/1000
        
        # Continue if we have a new timestamp
        if timestamp > latest:
            price = float(point[1])
            
            # Put into array following headers "timestamp, date, price"
            element = [timestamp, datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d"), price]
            
            writer.writerow(element)
            


# In[ ]:




