# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 19:46:04 2023

@author: porri
"""

from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, EarthLocation
from astropy.coordinates import get_body_barycentric, get_body, get_moon
from utilly import *


def planet_coordinates(planet, date = None):
    '''
    Defines Planet positions. 
    This should be accurate to a few arcminutes
    '''

    if date is None:
        date = get_today()
    date = str(date)
    
    year = str(date[:4])
    month = str(date[4:6])
    day = str(date[6:])
    
    eph_time = '13:00' # This was chosen as an average, should be fine
    date_string = year + '-' + month + '-' + day + ' ' + eph_time
    
    t = Time(date_string)
    
    loc = EarthLocation.of_site('MJO') 
    with solar_system_ephemeris.set('builtin'):
        jup = get_body(planet, t, loc) 
        
    RA = jup.ra.hour
    RA = coordinates_string_ra(RA)
    
    DEC = jup.dec#.degree
    DEC = coordinates_string_dec(DEC)
    
    print(planet, 'Position:')
    print('Right Ascension ->', RA)
    print('Declination     ->', DEC)
    print(' ')


#date = YYYYMMDD # Format of the date

planet_list = ['Mercury', 'Venus', 'Mars', 
               'Jupiter', 'Saturn', 'Uranus',
               'Neptune']

for planet in planet_list:
    planet_coordinates(planet, date = None)
