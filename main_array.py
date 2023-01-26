# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 21:35:14 2023

@author: porri
"""

import numpy as np
from focus_BC_utils import *

# Data that I input. Feel free to adjust as this is a rough guide
# I will do tests to get more and better data points

focus = [181, 188, 190, 194, 198]
FWHM = [8.309, 4.475, 4.253, 5.039, 7.436]

focus_function(focus, FWHM)


# temperature = [0, 5, 10, 7, 9]