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
    data = make_entries(df)
    save_targs(data,save_path + '/targets.json')
    print('!!! Made target list for ' + date + ' !!!')

def priority(data):
    
    data['Priority'] = int(1)
    return data

def make_entries(data,readout=5):
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
        
        exptime = l['Exposure Time']
        if str(exptime) == 'nan':
            exptime = 60 # Default time
            exptime = int(exptime)
            print()
            print('No exposure time given. Setting "{0}" to {1}s'.format(name, exptime))
            print()
        if ra == 'nan':
            print()
            print('No RA coordinates entered, searching for "{0}"'.format(name))
            print()
            obj = Simbad.query_object(name)
    
            ra = str(obj['RA'][0])
            dec = str(obj['DEC'][0])
            ra = coordinates_space(ra)
            dec = coordinates_space(dec)
        elif dec == 'nan':
            print()
            print('No DEC coordinates entered, searching for "{0}"'.format(name))
            print()
            obj = Simbad.query_object(name)
    
            ra = str(obj['RA'][0])
            dec = str(obj['DEC'][0])
            ra = coordinates_space(ra)
            dec = coordinates_space(dec)
        else:
            ra = coordinates_angle(ra)
            dec = coordinates_angle(dec)
        
        if type_obs == 'Nebula':
            if filters == 'nan':
                filters = ['Halpha', 'SII', 'OIII']
            exptime = 300
        elif type_obs == 'nebula':
            if filters == 'nan':
                filters = ['Halpha', 'SII', 'OIII']
            exptime = 300
        elif type_obs == 'Galaxy':
            if filters == 'nan':
                filters = ['g', 'r', 'i']
        elif type_obs == 'galaxy':
            if filters == 'nan':
                filters = ['g', 'r', 'i']
        elif type_obs == 'Cluster':
            if filters == 'nan':
                filters = ['g', 'r', 'i']
        elif type_obs == 'cluster':
            if filters == 'nan':
                filters = ['g', 'r', 'i']     
        elif type_obs == 'Planet':
            if filters == 'nan':
                filters = ['Halpha', 'SII', 'OIII', 
                            'Methane', 'U', 'B', 'g']        
        elif type_obs == 'planet':
            if filters == 'nan':
                filters = ['Halpha', 'SII', 'OIII', 
                            'Methane', 'U', 'B', 'g']   
        elif type_obs == 'star':
            if filters == 'nan':
                filters = ['g', 'r']
        elif type_obs == 'Star':
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