#! /usr/bin/env python
# -*- coding: utf-8 -*-


# --------------------------------------------------
#  File:        recharge_adjust_spatial_ensemble_mean_warming.py
#
#  Created:     Di 07-09-2021 
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce spatial Netcdf file  of 30 years average of each Met and then average of all METS  with single indicator
#
#  Modified by: chaitanya Malla
#  Modified date:17.10.2021 
#
# --------------------------------------------------

import glob
import xclim as xc
import xarray as xr
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from xclim import ensembles




inpath= "/work/malla/sachsen_input/"
outpath="/work/malla/sachsen_output/spatial/data/"
ind="recharge"


def process(filename):
    ens = ensembles.create_ensemble(glob.glob(inpath+"*/"+filename))
    ens1= ens.resample(time="Y").sum() 
    ens2= ens1.where(ens1>0)
    ens3= ens2.mean(dim="time")                                
    ens4= ens3.median(dim="realization")
    ens3.to_netcdf(outpath+ind+"/"+"ensemble_"+filename)
    ens4.to_netcdf(outpath+ind+"/"+"ensemblemedian_"+filename)
    return ens4
    

d1= process(ind+"_adjust_historic.nc")
d2= process(ind+"_adjust_1_5K.nc")
d3= process(ind+"_adjust_2K.nc")
d4= process(ind+"_adjust_3K.nc")











# output = "/work/malla/sachsen_output/spatial/data/recharge/"
# def process(filename):
#     filename= filename
#     data_set = glob.glob("/work/malla/sachsen_input/*/"+ filename)
#     data = []
#     for d in data_set:
#         ds = xr.open_dataset(d)
#         ds1 = ds.resample(time="Y").sum()
#         ds2 = ds1.mean("time")
#         data.append(ds2)
#     j = sum(data)/len(data)

#     return j

# re_hist = process("recharge_adjust_historic.nc")
# re_1_5K = process("recharge_adjust_1_5K.nc")
# re_2K = process("recharge_adjust_2K.nc")
# re_3K = process ("recharge_adjust_3K.nc")

# re_hist.to_netcdf(output + "recharge_adjust_historic_ensemblemean.nc")
# re_1_5K.to_netcdf(output + "recharge_adjust_1_5K_ensemblemean.nc")
# re_2K.to_netcdf(output + "recharge_adjust_2K_ensemblemean.nc")
# re_3K.to_netcdf(output + "recharge_adjust_3K_ensemblemean.nc")

