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
        total_time = 5*300
    else:
        total_time = 5*300
    return total_time

def make_look_entries(look,readout=5,filters=['g', 'r']):
    obs = []
    key = list(look.keys())
    for k in key:
        ll = look[k]
        for j in range(len(ll)):
            l = ll.iloc[j]
            rate_lim = rate_limit(l['Rate ("/min)'])
            exptime = rough_exptime(l['V Mag.'])
            if rate_lim < exptime:
                m = '!!! exposure time is too long for rate!!! \n Rescaling: {}s -> {}s'.format(exptime,rate_lim)
                print(m)
                exptime = rate_lim
            if 300 < exptime:
                m = '!!! exposure time is too long for tracking!!! \n Rescaling: {}s -> {}s'.format(exptime,500)
                print(m)
                exptime = 300
            ra,dec = format_coord(l['R.A.'],l['Dec.'])
            name = l['Target Name'].replace(' ','_').replace('/','') + '_22S01'
            priority = l['priority']
            total_time = priority_time(priority)
                    
            exptime = int(round_look_exposures(exptime))

            for f in filters:
                repeats = int(total_time / (exptime + readout))
                ob = make_obs_entry(exptime,f,repeats,name,ra,dec,priority=priority)
                obs += [ob]
    return obs    
            

def look_priority(look,names=None,mag_priority=[['19-17',3],['17-15',4],['15-12',5]]):
    looks = deepcopy(look['active'])
    looks['priority'] = int(3)
    if mag_priority is not None:
        for i in range(len(mag_priority)):
            f,b = mag_priority[i][0].split('-')
            b = float(b); f = float(f)
            if b > f:
                temp = deepcopy(f)
                f = b
                b = temp
            print(f,b)
            ind = (looks['V Mag.'].values < f) & (looks['V Mag.'].values > b)
            looks['priority'].iloc[ind] = int(mag_priority[i][1])

    if names is not None:
        for i in range(len(names)):
            name = names[i]
            for j in range(len(looks)):
                if name[0] in looks.iloc[j]['Target Name']:
                    looks['priority'].iloc[j] = int(name[1])
    look['active'] = looks
    return look



def make_look_list(name_priority,mag_priority):
    """
    Generate the target json target file for active LOOK targets. 
    """
    date = get_today()
    date = str(date)

    save_path = package_directory + 'targets/' + date

    make_dir(save_path)

    look = scrub_look_targets()
    look = look_priority(look,names=name_priority,mag_priority=mag_priority)
    looks = make_look_entries(look)
    save_targs(looks,save_path + '/look.json')

    print('!!! Made LOOK target list for ' + date + ' !!!')


if __name__ == '__main__':
    make_look_list(name_priority=[['81P',1],['73P',1],['UN271',1]],mag_priority=[['22-19',3],['19-17',4],['17-15',5],['15-12',6]])