# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 04:42:37 2022

@author: porri
"""


import os
import numpy as np

def rough_exptime(mag,a=14.71317761, b=-17.04790805,  c=18.22621702):
    exp_time = a*np.exp(mag+b) + c
    return int(exp_time)


def make_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def get_today():
    from datetime import datetime
    d = datetime.now()
    date = f"{d.year:04.0f}{d.month:02.0f}{d.day:02.0f}"
    return date

def save_targs(target_list,name):
    import json
    with open(name, 'w') as fout:
        json.dump(target_list, fout,indent=2)

def make_obs_entry(exptime,filt,repeats,obj,ra,dec,priority=1,exptype='object'):
    obs = {
        "count": repeats,
        "expType": exptype,
        "object": obj,
        "filter": filt,
        "expTime": exptime,
        "ra": ra,
        "dec": dec,
        "priority":int(priority)
        }
    return obs

def coordinates_angle(x):
    x = x.split(':')
    x[0] = str(x[0])
    
    x[1] = float(x[1])
    x[1] /= 60
    
    x[2] = float(x[2])
    x[2] /= 6000
    
    x_l = x[1] + x[2]
    x_l = str(x_l)
    x = x[0] + ' ' + x_l
    x = x.split(' ')
    x[1] = x[1][1:]
    x = ''.join(x)
    x = float(x)
    return(x)

def coordinates_string_dec(x):
    x = str(x)
    x = x.split('d')
    x_l = []

    if len(x[0]) < 2:
        x[0] = '0' + x[0]
    x_l.append(x[0])
        
    x = x[1].split('m')

    if len(x[0]) < 2:
        x[0] = '0' + x[0]
    x_l.append(x[0])

    x = x[1].split('s')
    x = float(x[0])
    x = "%.1f" % x
    
    if len(x) < 4:
        x = '0' + str(x)

    x = x_l[0] + ':' + x_l[1] + ':' + x
    return x

def coordinates_string_ra(x):
    x = str(x)
    x = x.split('.')

    if len(x[0]) < 2:
        x[0] = '0' + x[0]

    x[1] = '0.' + x[1]
    x[1] = float(x[1])
    x[1] = x[1]*60
    x[1] = str(x[1])
    x[1] = x[1].split('.')

    x_l = []

    if len(x[0]) < 2:
        x[0] = '0' + x[0]
    x_l.append(x[0])

    x = x[1]
    x[1] = float('0.' + x[1])
    x[1] = x[1]*60
    x[1] = "%.1f" % x[1]

    if len(x[1]) < 4:
        x[1] = '0' + str(x[1])

    x = x_l[0] + ':' + x[0] + ':' + x[1]
    return x

# print(get_today())