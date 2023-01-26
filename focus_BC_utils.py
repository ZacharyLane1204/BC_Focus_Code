# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 21:28:55 2023

@author: porri
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import interpolate

def func(x, a, b, c,d ):
    '''
    Quadratic
    '''
    return a*x**2 + b*x + c

def focus_function(focus, FWHM):
    
    popt, _ = curve_fit(func, focus, FWHM) # Curve fitting
    
    x = np.linspace(min(focus),max(focus),100001) # Setting up interpolation Space
    
    
    '''
    Finding the Minimum of the curve
    '''
    y = func(x, *popt) # Running with optimal paramters
    
    minimum = min(y)
    y_list = y.tolist()
    minimum_x = y_list.index(min(y))
    minimum_x = x[minimum_x]
    
    
    '''
    Find interpolation from FWHM
    '''
    FWHM_interpolater = interpolate.interp1d(x,y, kind = 'quadratic')
    
    FWHM_list = []
    for f in focus:
        FWHM_list.append(float(FWHM_interpolater(f)))
    
    FWHM_calc = np.array(FWHM_list)
    
    # chi2 = np.sum((FWHM_calc - FWHM)**2 / (len(FWHM) - 1))
    
    chi2 = np.sum((FWHM_calc - FWHM)**2 / FWHM)
    
    '''
    Printing Scripts
    '''
    print('Optimal Focus is:', "{0:0.2f}".format(minimum_x))
    #print(r'chi^2 is:', chi2)
    print(f"chi^2 is: {chi2:.3e}")
    
    '''
    Plotting
    '''
    plt.figure()
    plt.plot(x,y, color = 'k')
    plt.scatter(focus,FWHM)
    plt.xlim(min(focus),max(focus)) 
    plt.xlabel('Focus value')
    plt.ylabel('FWHM')
    plt.show()