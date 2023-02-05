# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 03:01:05 2023

@author: porri
"""

from comet_targets import make_look_list
from targets import *
# from swope_targets import make_swope_list
from scheduler import make_schedule
import time


if __name__ == '__main__':
    start = time.time()
    date=None
    Tele =['moa', 'bc']
    # T = 'moa'
    
    make_look_list(name_priority=[['81P',2],['73P',2],['UN271',2]],mag_priority=[['19-17',3],['17-15',4],['15-12',5]])
    make_list()
    make_schedule(date, telescope = 'bc')
    end = time.time()
    total_time = (end - start)/60
    print('Total Time to generate schedule:', "{0:0.2f}".format(total_time), 'minutes')