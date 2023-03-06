# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 21:28:55 2023

@author: porri
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import interpolate

def func(x, a, b, c):
    '''
    Quadratic
    '''
    return a*x**2 + b*x + c

def focus_function(focus, FWHM):
    
    length = len(focus)
    
    sigma = 0.005*np.ones(length)
    
    sigma_1 = 0.005
    
    n_bf = 3
    bf = np.zeros((n_bf,length))
    bf[0,:] = focus**2
    bf[1,:] = focus**1
    bf[2,:] = focus**0
    
    
    
    # Create and fill A matrix and b vector - remember to use the transformed data
    A = np.zeros((n_bf,n_bf))
    b = np.zeros(n_bf)
    for k in range(n_bf):
        for j in range(n_bf):
            A[k,j] = np.sum(bf[k,:]*bf[j,:]/sigma**2) 
        b[k] = np.sum(FWHM*bf[k,:]/sigma**2)
    
    # Calculate the results
    
    A_inv = np.linalg.inv(A)
    # print(A_inv.shape)
    
    a = np.linalg.solve(A,b)
    
    # print('a (fitted values)\n', a)  # our answer
    # print('delta a (uncertainties)\n',np.sqrt(np.diag(A_inv)))
    
    x = np.linspace(min(focus),max(focus),100001)
    
    y = func(x,*a)
    
    minimum = min(y)
    y_list = y.tolist()
    minimum_x = y_list.index(min(y))
    minimum_x = x[minimum_x]
    
    print('Optimal Focus is:', "{0:0.2f}".format(minimum_x))
    
    
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
    
    #print(r'chi^2 is:', chi2)
    print(f"chi^2 is: {chi2:.3e}")
    
    '''
    Plotting
    '''
    plt.figure()
    plt.plot(x,y, color = 'k')
    plt.errorbar(focus,FWHM, sigma, fmt='.')
    plt.xlim(min(focus),max(focus)) 
    plt.xlabel('Focus value')
    plt.ylabel('FWHM')
    plt.show()