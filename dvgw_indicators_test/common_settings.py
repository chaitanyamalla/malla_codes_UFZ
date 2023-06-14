#!/usr/bin/env python

# --------------------------------------------------
#  File:        common_settings.py
#
#  Created:     Di 05-10-2021
#  Author:      Friedrich Boeing
#
# --------------------------------------------------
#
#  Description: general settings for all scripts
#
#  Modified:
#
# --------------------------------------------------


import pandas as pd
import numpy as np

do_periods             = True
#  -- read metadata --------------------------------

meta                    = pd.read_csv("/data/hicam/data/processed/meteo/germany/climproj/euro-cordex/88realizations_mhm/88_main_LUT.txt",sep=" ")
met_ids                 = np.sort(pd.unique(meta["met_id"]))

if len(met_ids) < 88: # if not all simulations are in the directory
    print("Not all of {:} simulations are available. Checking for available paths in: {:}".format(len(met_ids),inpath))
    met_ids                 = np.sort(os.listdir(inpath))
# list of names of the rcps climate models
gcms                    = np.sort(pd.unique(meta["gcm"]))
# list of names of the regional climate models
rcms                    = np.sort(pd.unique(meta["inst.rcm"]))
# list of names of the hydrological models
hms                     = ['mHM']
# list of names of the rcps
rcps                    = np.sort(pd.unique(meta["rcp"]))
periods                = [       1985,        2035,        2050,        2084]  # centers for 1971-2000, 2021-2050, 2036 - 2065, 2070 - 2099

# new periods: 
periods                = [       1985,        2035,        2050,        2083]  # centers for 1971-2000, 2021-2050, 2036 - 2065, 2069 - 2098
title_periods = ['{:}-{:}'.format(periods[tt]-14,periods[tt]+15) for tt in np.arange(len(periods))]

# warming levels
# title_warm    = ['1p5','3p0', '4p0']
# title_warm = ['1.5 °C    ', '2 °C      ', '3 °C      ']
# warming levels
title_warm              = ['historical','1p5','3p0', '4p0']
if do_periods:
    title_warm      = title_periods


globalAttsFixed     = {"Conventions" : "CF-1.8",
                    "institution" : "Helmholtz Center for Environmental Research",
                    "crs"         : "ESPG:4326"}
