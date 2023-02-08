# BC_Focus_Code

This is a basic script for determining the focus, exposure time and making the schedule for the Mt John B&C trip. This script reads a target list from a google sheet. It will search names from the SIMBAD database if no coordinates are given - however, this does not do non-sidereal moving objects apart from the planets yet (planned for a future update).

Please git clone the following directory first!

https://github.com/CheerfulUser/astroplan

Git clone this directory for this to work as well

Requires numpy, pandas, matplotlib, astropy, astroquery

Remember to use conda or pip install depending if you have an anaconda environment installed.

## Main Scripts:

### exposure_main.py

Determines the exposure, just modify the magnitude. Notice that this will only work for broadband filters. Use this number to edit the Target List as in the example sheet:

https://docs.google.com/spreadsheets/d/1l4JhjWdfvWFeNe-L6eJdcY93oLUa7MS4qk2H5n3-ERY/edit

, once you are done with a target list you can duplicate the sheet (rename it with the UTC date), rename the copy, delete all entries of 'Sheet1'. The name must be 'Sheet1' for this code to work!!

### focus_main_csv.py

Determines the focus. Choose a bright (but not over-saturated) star and analyse the profile with ctrl+i on Maxim DL6 and hover the mouse over the target star. Note the FWHM and Focus in the following sheet as in the example sheet:

https://docs.google.com/spreadsheets/d/1MC6uRbzfPupTay3QvXSHlgwqOou4a6H2Ac3feXzrVb4/edit#gid=0

; once you are done with a focus list you can duplicate the sheet (rename it with the UTC date), and please please please note the outside temperature in this document (from http://www2.phys.canterbury.ac.nz/~physweb/node1/belchertown/ )!!!! Then rename the copy; delete all entries of 'Sheet1'. The name must be 'Sheet1' for this code to work!!


### general_main.py

Generates a target list and plot for the night. Draws from:

https://docs.google.com/spreadsheets/d/1l4JhjWdfvWFeNe-L6eJdcY93oLUa7MS4qk2H5n3-ERY/edit

### scheduler_main.py

Generates a target list and plot for the night, this also draws from the LOOK target list. Draws from:

https://docs.google.com/spreadsheets/d/1l4JhjWdfvWFeNe-L6eJdcY93oLUa7MS4qk2H5n3-ERY/edit

## Utility Scripts:

comet_targets.py (Creating Comet Targets)

exposure_BC_utils.py (Calculations for determining exposure time, will be further improved as we extend further)

scheduler.py (Schedules base operations)

targets.py (Creates target list .json file)

utilly.py (General utility file)

planet_position_main.py (Generates Ephemerides for the planet on a specific date and allows the planet name to be a searchable target from target list).
