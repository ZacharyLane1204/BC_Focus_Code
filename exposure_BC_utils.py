# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 01:12:32 2023

@author: porri
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import interpolate
import warnings

warnings.filterwarnings(action='ignore', category=RuntimeWarning) # setting ignore as a parameter and further adding category


def rough_exptime(mag,a, b, c):
    exp_time = a*np.exp(mag+b) + c
    return int(exp_time)

def func(x, a, b, c,d ):
    return a * np.log(b*x+d) + c

'''
Attempting my own relationship
'''

def bc_focus(entered_mag):

    # Data that I input. Feel free to adjust as this is a rough guide
    # I will do tests to get more and better data points
    time = [0.5,10, 30, 60 , 120, 300]
    magn = [-0.55, 6, 8, 10.9, 14, 17.3]
    
    popt, pcov = curve_fit(func, time, magn) # Curve fitting
    
    x = np.linspace(0,700,100001) # Setting up interpolation Space
    
    y = func(x, *popt) # Running with optimal paramters
    
    timefind_interpolater = interpolate.interp1d(y, x) # Interpolator to find times from mag
    
    '''
    Post-processing
    '''
    output_time = timefind_interpolater(entered_mag)
    print('The exposure time for target of magnitude', entered_mag, 'is:', int(output_time), 's.')
    
    plt.figure()
    # plt.plot(time, magn)
    plt.plot(x,y)
    plt.xlim(0,300)
    plt.ylim(1,19)
     
    if 300 < output_time < 700 :
        print('Over 300s. Stacking images is required.')
    elif output_time > 700:
        print('Over 20.2 Magnitudes')
    else:
        plt.axvline(output_time, color = 'purple', linestyle = '--', alpha = 0.9)
        plt.axhline(entered_mag, color = 'purple', linestyle = '--', alpha = 0.9)
    plt.xlabel('Exposure Time')
    plt.ylabel('Magnitude')
    plt.show()
