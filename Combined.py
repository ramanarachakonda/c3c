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

burl_url = 'https://services1.arcgis.com/X3dmaNvzWUnemDAc/arcgis/rest/services/Cases_current/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=name%20asc&resultOffset=0&resultRecordCount=50&resultType=standard&cacheHint=true',
gloc_url = 'https://services5.arcgis.com/ALQeR5k3182nooX1/arcgis/rest/services/COVID19/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&outSR=102100&resultOffset=0&resultRecordCount=25&resultType=standard&cacheHint=true'

def get_max_cases(hist_df, city, current):
    
    city_df = hist_df[hist_df['City'] == city]
    new_current = max(max(city_df['Total_Cases']), current) #if Max(total)>max(confirmed) then "Call"
    county = city_df['County'].values[0]
    state = city_df['State'].values[0]

    return state, county, new_current, not(current != new_current)


def main():
    hist_df = pd.read_csv('Webscraping_Db.csv')
    content = ''

    dic = {
        'burl': (burl_url, 'name', 'confirmed', True),
        'gloc': (gloc_url, 'MUNICIPALI', 'COVID', False),
    }


    for key, t in dic.items():
        url, name, cases, has_date = t

        response = requests.get(url)
        parsed_json = json.loads(response.content)

        for city in parsed_json['features']:
            cityname = (city['attributes'][name])
            cur_data = int(city['attributes'][cases])
            state, county, new_current, changed = get_max_cases(hist_df, cityname, cur_data)
            if has_date:
                date = datetime.fromtimestamp(int(str(city['attributes']['reportdt'])[:-3])).date()
            else:
                date = date.today()

            content += f'{state}, {county}, {cityname}, {new_current}, {date.isoformat()}, {changed}\n'

    #Camden Starts here
    camden_raw_url = 'https://datawrapper.dwcdn.net/E7uou/'
    raw_content = requests.get(camden_raw_url).content.decode()

    camden_url = re.search(r'url=(.*?)"', raw_content).group(1)
    content = requests.get(camden_url).content.decode()

    d = re.search(r'<meta name="description" content="Updated: ([A-Z][a-z]+\s*\d+,\s*\d+)"', content)

    date = datetime.strptime(d.group(1), "%B %d, %Y")
    camd_content = []
    
    for m in re.findall(r';([A-Z\s*]+\s*(TOWNSHIP|BOROUGH))\s*<br>\s*([0-9]+);([0-9]+)', content, re.MULTILINE | re.DOTALL):
        city, total_cases = m[0], m[2]
        state, county, new_current, changed = get_max_cases(hist_df, city, total_cases)
        content += f'{state}, {county}, {city}, {new_current}, {date.isoformat()}, {changed}\n'

    #Adding Content to DF and Parsing dates 
    df = pd.read_csv(io.StringIO(content), header=None)
    df[3] = pd.to_datetime(df[3])

    df.columns = ['State', 'County', 'City', 'Total Cases', 'Date', 'Error']

    df.to_csv(r'3County_runon_6.03.2020_916.csv')

if __name__ == '__main__':
    main()
