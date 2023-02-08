# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 01:33:59 2023

@author: porri
"""

import numpy as np
from focus_BC_utils import *
import pandas as pd
import requests
from utilly import *
from exposure_BC_utils import bc_focus
from astroquery.simbad import Simbad
from planet_position_main import planet_coordinates


# Data that I input. Feel free to adjust as this is a rough guide
# I will do tests to get more and better data points

package_directory = os.path.dirname(os.path.abspath(__file__)) + '/'

def get_target_list():
    sheet_id = "1l4JhjWdfvWFeNe-L6eJdcY93oLUa7MS4qk2H5n3-ERY"
    sheet_name = "Sheet1"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

    sheets = requests.get(url)
    open('targets.csv', 'wb').write(sheets.content)

    df = pd.read_csv('targets.csv')
    return df

def make_list(date):
    if date is None:
        date = get_today()
    date = str(date)

    save_path = package_directory + 'targets/' + date

    make_dir(save_path)

    df = get_target_list()
    df = priority(df)
    data = make_entries(date, df)
    save_targs(data,save_path + '/targets.json')
    print('!!! Made target list for ' + date + ' !!!')

def priority(data):
    
    data['Priority'] = int(1)
    return data

def make_entries(date, data, readout=5):
    obs = []
    
    for j in range(len(data)):
        
        l = data.iloc[j]
        repeats = 3
        mag = l.Magnitude
        filters = l.Filter
        filters = str(filters)
        if filters != 'nan':
            filters = filters.split(',')
        ra = str(l.RA)
        dec = str(l.DEC)
        type_obs = str(l.Type)
        name = l['Target Name']
        name = str(name)
        
        if name.lower() == 'jupiter':
            print()
            print('Finding coordinates for Jupiter')
            ra, dec = planet_coordinates('Jupiter', date, printout = False)   
        elif name.lower() == 'mercury':
            print()
            print('Finding coordinates for Mercury')
            ra, dec = planet_coordinates('Mercury', date, printout = False)             
        elif name.lower() == 'venus':
            print()
            print('Finding coordinates for Venus')
            ra, dec = planet_coordinates('Venus', date, printout = False)
        elif name.lower() == 'mars':
            print()
            print('Finding coordinates for Mars')
            ra, dec = planet_coordinates('Mars', date, printout = False)
        elif name.lower() == 'saturn':
            print()
            print('Finding coordinates for Saturn')
            ra, dec = planet_coordinates('Saturn', date, printout = False)  
        elif name.lower() == 'uranus':
            print()
            print('Finding coordinates for Uranus')
            ra, dec = planet_coordinates('Uranus', date, printout = False)  
        elif name.lower() == 'neptune':
            print()
            print('Finding coordinates for Neptune')
            ra, dec = planet_coordinates('Neptune', date, printout = False) 

        if name == 'nan':
            continue
        
        exptime = l['Exposure Time']
        if str(exptime) == 'nan':
            exptime = 60 # Default time
            exptime = int(exptime)
            print()
            print('No exposure time given. Setting "{0}" to {1}s'.format(name, exptime))
        if ra == 'nan':
            print()
            print('No RA coordinates entered, searching for "{0}"'.format(name))
            obj = Simbad.query_object(name)
    
            ra = str(obj['RA'][0])
            dec = str(obj['DEC'][0])
            ra = coordinates_space(ra)
            dec = coordinates_space(dec)
        elif dec == 'nan':
            print()
            print('No DEC coordinates entered, searching for "{0}"'.format(name))
            obj = Simbad.query_object(name)
    
            ra = str(obj['RA'][0])
            dec = str(obj['DEC'][0])
            ra = coordinates_space(ra)
            dec = coordinates_space(dec)
        else:
            ra = coordinates_angle(ra)
            dec = coordinates_angle(dec)
        
        
        if type_obs.lower() == 'nebula':
            if filters == 'nan':
                filters = ['Halpha', 'SII', 'OIII']
            exptime = 300
        elif type_obs.lower() == 'galaxy':
            if filters == 'nan':
                filters = ['g', 'r', 'i']
        elif type_obs.lower() == 'cluster':
            if filters == 'nan':
                filters = ['g', 'r', 'i'] 
        elif type_obs.lower() == 'planet':
            if filters == 'nan':
                filters = ['Halpha', 'SII', 'OIII', 
                            'Methane', 'U', 'B', 'g']   
        elif type_obs.lower() == 'star':
            if filters == 'nan':
                filters = ['g', 'r']
        else:
            if filters == 'nan':
                filters = ['g', 'r', 'i']
        exptime = int(exptime)
        priority = l['Priority']
        for f in filters:
            ob = make_obs_entry(exptime,f,repeats,name,ra,dec,priority=priority)
            obs += [ob]
    return obs    

# data = make_list()