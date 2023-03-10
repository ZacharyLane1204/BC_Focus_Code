# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 03:16:30 2023

@author: porri
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u
from copy import deepcopy
import os
from utilly import *


package_directory = os.path.dirname(os.path.abspath(__file__)) + '/'


def scrub_look_targets(maglim=18, dec_lim=15):
    looks = pd.read_html('https://neoexchange.lco.global/lookproject/')
    active = looks[0]
    new = looks[1]
    mag_ind = (active['V Mag.'].values < maglim) & (active['V Mag.'].values > 2)
    dec = np.array([int(v.split(' ')[0]) for v in active['Dec.'].values])
    dec_ind = dec < dec_lim
    active = active.iloc[mag_ind & dec_ind]
    mag_ind = new['V Mag.'].values < maglim
    dec = np.array([int(v.split(' ')[0]) for v in new['Dec.'].values])
    dec_ind = dec < dec_lim
    new = new.iloc[mag_ind & dec_ind]
    look = {'active':active,'new':new}
    return look


def rate_limit(rate,pixsize=0.6,ap_size=5):
    pixrate = rate/pixsize
    time = (ap_size / pixrate) * 60
    return int(time)



def format_coord(ra,dec):
    if type(ra) == str:
        c = SkyCoord(ra,dec,unit=(u.hourangle,u.deg))
        ra = c.ra.deg
        dec = c.dec.deg
    return ra,dec


def round_look_exposures(exptime):
    allowed = np.array([20,30,60,120,300])
    diff = abs(allowed - exptime)
    ind = np.argmin(diff)
    return allowed[ind]

def priority_time(priority):
    if priority > 3:
        total_time = 3*300
    else:
        total_time = 3*300
    return total_time

def make_look_entries(look,readout=5,filters=['g', 'r']):
    obs = []
    key = list(look.keys())
    for k in key:
        ll = look[k]
        for j in range(len(ll)):
            l = ll.iloc[j]
            rate_lim = rate_limit(l['Rate ("/min)'])
            exptime = 300
            # print(l)
            ra,dec = format_coord(l['R.A.'],l['Dec.'])
            name = l['Target Name'].replace(' ','_').replace('/','')
            # priority = l['priority']
            # print(priority)
            # total_time = priority_time(priority)
            total_time = 3*300
            
            # exptime = int(round_look_exposures(exptime))
            priority = 5
            for f in filters:
                repeats = 3
                ob = make_obs_entry(exptime,f,repeats,name,ra,dec,priority=priority)
                obs += [ob]
    return obs    
            

def look_priority(look,mag_priority=[['19-17',5],['17-15',4],['15-12',3]]):
    # looks = deepcopy(look['active'])
    look['active']['priority'] = int(3)
    if mag_priority is not None:
        for i in range(len(mag_priority)):
            f,b = mag_priority[i][0].split('-')
            b = float(b); f = float(f)
            if b > f:
                # temp = np.array(f)
                # temp = float(temp[0])
                temp = deepcopy(f)
                f = b
                b = temp
            ind = (look['active']['V Mag.'].values < f) & (look['active']['V Mag.'].values > b)
            look['active']['priority'].iloc[ind] = int(mag_priority[i][1])

    # look['active'] = looks
    return look



def make_look_list(date, mag_priority):
    """
    Generate the target json target file for active LOOK targets. 
    """
    if date is None:
        date = get_today()
    date = str(date)

    save_path = package_directory + 'targets/' + date

    make_dir(save_path)

    look = scrub_look_targets()
    look = look_priority(look, mag_priority=mag_priority)
    looks = make_look_entries(look)
    save_targs(looks,save_path + '/look.json')

    print('!!! Made LOOK target list for ' + date + ' !!!')


if __name__ == '__main__':
    make_look_list(date, name_priority=[['81P',2],['73P',2],['UN271',2]], mag_priority=[['19-17',5],['17-15',4],['15-12',3]])