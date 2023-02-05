# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 21:26:05 2023

@author: porri
"""

import numpy as np
from focus_BC_utils import *
import pandas as pd
import requests

sheet_id = "1MC6uRbzfPupTay3QvXSHlgwqOou4a6H2Ac3feXzrVb4"
sheet_name = "Sheet1"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
URL = "https://docs.google.com/spreadsheets/d/1MC6uRbzfPupTay3QvXSHlgwqOou4a6H2Ac3feXzrVb4/edit#gid=0"

sheets = requests.get(url)
open('focusBC.csv', 'wb').write(sheets.content)

df = pd.read_csv('focusBC.csv')

focus = df['Focus']
FWHM = df['FWHM']

focus_function(focus, FWHM)

