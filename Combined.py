#!/usr/bin/env python
# coding: utf-8

import requests
import shutil
import urllib
import json
import os
import io
import re
import csv
import pandas as pd
from datetime import datetime, date


def counties2():
    hist_df = pd.read_csv('Webscraping_Db.csv')

    dic = {'burl': 'https://services1.arcgis.com/X3dmaNvzWUnemDAc/arcgis/rest/services/Cases_current/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=name%20asc&resultOffset=0&resultRecordCount=50&resultType=standard&cacheHint=true',

requests.get(burl_url)
burl_response = requests.get(burl_url)

burl_response.content

burl_parsed_json = json.loads(burl_response.content)

burl_parsed_json


burl_parsed_json['features']


burl_content = ''
#vim xed visualcode
#pycharm
for city in burl_parsed_json['features']:
    cityname = (city['attributes']['name'])
    city_df = hist_df[hist_df['City'] == cityname]
    cur_data = int(city['attributes']['confirmed'])
    current = max(max(city_df['Total_Cases']), cur_data) #if Max(total)>max(confirmed) then "Call"
    county = city_df['County'].values[0]
    state = city_df['State'].values[0]
    date = datetime.fromtimestamp(int(str(city['attributes']['reportdt'])[:-3]))
    burl_content += f'{state}, {county}, {cityname}, {current}, {date.date().isoformat()}, {not (cur_data != current)}\n'

print(burl_content)

#

burl_df = pd.read_csv(io.StringIO(burl_content), header = None)
burl_df[3] = pd.to_datetime(burl_df[3])



gloc_url = 'https://services5.arcgis.com/ALQeR5k3182nooX1/arcgis/rest/services/COVID19/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outSR=102100&resultOffset=0&resultRecordCount=25&resultType=standard&cacheHint=true'


# In[12]:


gloc_req = requests.get(gloc_url)
gloc_parsed_json = json.loads(gloc_req.content)
gloc_content = ''
gloc_hist_df = pd.read_csv('Webscraping_Db.csv')

for gloc_city in gloc_parsed_json['features']:
    gcityname = (gloc_city['attributes']['MUNICIPALI'])
    #try to import name
    
    gloc_city_df = gloc_hist_df[gloc_hist_df['City'] == gcityname.upper()]
    gcur_data = int(gloc_city['attributes']['COVID'])
    gcurrent = max(max(gloc_city_df['Total_Cases']), gcur_data) #if Max(total)>max(confirmed) then "Call"
    gcounty = gloc_city_df['County'].values[0]
    gstate = gloc_city_df['State'].values[0]
    gdate = date.today().isoformat()
    gloc_content += f'{gstate}, {gcounty}, {gcityname}, {gcurrent}, {gdate}, {not(gcur_data ++ gcurrent)}\n'
    
print(gloc_content)


gloc_df = pd.read_csv(io.StringIO(gloc_content), header = None)




camden_url = 'https://datawrapper.dwcdn.net/E7uou/'
content = requests.get(camden_url).content.decode()


camden_url = re.search(r'url=(.*?)"', content).group(1)
content = requests.get(camden_url).content.decode()


d = re.search(r'<meta name="description" content="Updated: ([A-Z][a-z]+\s*\d+,\s*\d+)"', content)

date = datetime.strptime(d.group(1), "%B %d, %Y")
camd_content = []
#filename = 'covid-' + '-'.join(map(str, [date.month, date.day, date.year])), + '.csv'


# In[23]:


for m in re.findall(r';([A-Z\s*]+\s*(TOWNSHIP|BOROUGH))\s*<br>\s*([0-9]+);([0-9]+)', content, re.MULTILINE | re.DOTALL):
    camd_content.append([m[0], m[2], m[3], date])

print(camd_content)


# In[24]:


cam_df = pd.DataFrame(camd_content)
cam_df.head()


# In[25]:


cam_df.columns = ['City','Total Cases','Death', 'Date']
cam_df.insert(0,'County','Camden County', True)
cam_df.insert(0,'State','New Jersey', True)
#cam_df.insert(0,'Grain','State',True)
cam_df.head()


# In[ ]:





# In[26]:


#burl_content, gloc_content, camd_content
burl_df.head()
gloc_df.head()
cam_df.head()


# In[27]:


gloc_df.head()


# In[28]:


burl_df.head()


# In[29]:


county_df = pd.concat([burl_df,gloc_df,cam_df])


# In[30]:


county_df.head()


# In[ ]:


county_df


# In[ ]:


county_df.to_csv(r'3County_runon_6.03.2020_916.csv')


# In[ ]:


#When are dashboards getting updated??

#NJ and PA are updated every hour
#cities are getting updated (Sunday) monday to (Thursday) Friday
#US is updated at 3 AM from the states websites
#need to change to uppercase and clean borugh/township
#Regex to Burlington County remove TWP|BORO
#Regex to Camden County and Gloucester Township|Borough
#Berlin Borough and Township are different
#Glassboro
#Franklin Township
#Fieldsboro
#Gibbsboro
#Swedesboro
#Willingboro
#Washington Township is in Gloucester


# In[ ]:


#def get_output_schema():       
#  return county_df.DataFrame({
#    'Grain' : prep_int(),
#    'Supplies Subgroup Encoded' : prep_int(),
#    'Region Encoded' : prep_int(),
#    'Route To Market Encoded' : prep_int (),
#    'Opportunity Result Encoded' : prep_int (),
#    'Competitor Type Encoded' : prep_int()
#    'Supplies Group Encoded' : prep_int()
#})
#Add


# In[ ]:


#!pip install tabpy


# In[ ]:




