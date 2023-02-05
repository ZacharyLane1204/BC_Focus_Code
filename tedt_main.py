# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 03:01:05 2023

@author: porri
"""

# from look_targets import make_look_list
from targets import *
# from swope_targets import make_swope_list
from scheduler import make_schedule
import time


if __name__ == '__main__':
    start = time.time()
    date=None
    Tele =['moa', 'bc']
    # T = 'moa'
    
    # make_look_list(name_priority=[['81P',1],['73P',1],['UN271',1]],mag_priority=[['22-19',3],['19-17',4],['17-15',5],['15-12',6]])
    make_list()
    # make_swope_list()
    # for T in Tele:
    make_schedule(date, telescope = 'bc')
    end = time.time()
    total_time = (end - start)/60
    print('Total Time to generate schedule:', "{0:0.2f}".format(total_time), 'minutes')