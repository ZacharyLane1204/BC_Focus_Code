# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 21:26:05 2023

@author: porri
"""

import numpy as np
from focus_BC_utils import *

# Data that I input. Feel free to adjust as this is a rough guide
# I will do tests to get more and better data points

data = np.genfromtxt('focusBC.csv', skip_header=1, delimiter = ',')

focus = data[:,0]
FWHM = data[:,1]

focus_function(focus, FWHM)

# focus = [-0.5, -0.3, 0 , 0.3, 0.5]
# FWHM = [0.2, 0.1, 0.2 , 0.3, 0.5]
# temperature = [0, 5, 10, 7, 9]
