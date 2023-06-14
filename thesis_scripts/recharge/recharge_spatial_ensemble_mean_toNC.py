#! /usr/bin/env python
# -*- coding: utf-8 -*-




# --------------------------------------------------
#  File:        recharge_spatial_ensemble_mean_warming.py
#
#  Created:     Di 31-08-2021 
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce spatial Netcdf file  of 30 years average of each Met and then average of all METS  with single indicator
#
#  Modified by: 
#  Modified date: 
#
# --------------------------------------------------






import glob
#import xclim as xc
import xarray as xr
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


output = "/work/malla/sachsen_output/spatial/data/recharge/"



def process(filename):
    filename= filename
    data_set = glob.glob("/work/malla/sachsen_input/*/"+ filename)
    data = []
    for d in data_set:
        ds = xr.open_dataset(d)
        ds1 = ds.resample(time="Y").sum()
        ds2 = ds1.mean("time")
        data.append(ds2)
    j = sum(data)/len(data)

    return j

re_hist = process("recharge_historic.nc")
# re_1_5K = process("recharge_1_5K.nc")
# re_2K = process("recharge_2K.nc")
# re_3K = process ("recharge_3K.nc")

re_hist.to_netcdf(output + "recharge_historic_ensemblemean.nc")
# re_1_5K.to_netcdf(output + "recharge_1_5K_ensemblemean.nc")
# re_2K.to_netcdf(output + "recharge_2K_ensemblemean.nc")
# re_3K.to_netcdf(output + "recharge_3K_ensemblemean.nc")

