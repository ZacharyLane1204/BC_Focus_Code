# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 11:18:54 2023

@author: porri
"""

from targets import *
from scheduler import make_schedule
import time


if __name__ == '__main__':
    start = time.time()
    date = None
    # If the date is None it grabs todays date, else you can input a date in format YYYYMMDD
    make_list(date)
    make_schedule(date, telescope = 'bc')
    end = time.time()
    total_time = (end - start)/60
    print('Total Time to generate schedule:', "{0:0.2f}".format(total_time), 'minutes')