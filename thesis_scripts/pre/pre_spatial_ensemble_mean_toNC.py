#!/usr/bin/env python

# -*- coding: utf-8 -*-

# --------------------------------------------------
#  File:        plot_spatial_pre_allMets_warming.py
#
#  Created:     Mo 30-08-2021 
#  Author:      Chaitanya Malla
#  
# --------------------------------------------------
#
#  Description: script to produce spatial plots of 30 years average of each Met and then average of all METS  with single indicator
#
#  Modified by: 
#  Modified date: 
#
# --------------------------------------------------

import glob
import xarray as xr
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import xclim as xc
from xclim import ensembles

inpath= "/work/malla/sachsen_input/"
outpath="/work/malla/sachsen_output/spatial/data/"


ind="pre"


def process(filename):
    ens = ensembles.create_ensemble(glob.glob(inpath+"*/"+filename))
    # ens1= ens.resample(time="Y").sum() 
    # ens2= ens1.where(ens1>0)
    # ens3= ens2.mean(dim="time")                                
    # ens4= ens3.median(dim="realization")
    # ens3.to_netcdf(outpath+ind+"/"+"ensemble_"+filename)
    # ens4.to_netcdf(outpath+ind+"/"+"ensemblemedian_"+filename)
    return ens
    

d1= process("pre_historic.nc")
# d2= process("pre_1_5K.nc")
# d3= process("pre_2K.nc")
# d4= process("pre_3K.nc")

print(d1)


















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


# pre_hist = process("pre_historic.nc")
# # pre_1_5K = process("pre_1_5K.nc")
# # pre_2K = process("pre_2K.nc")
# # pre_3K = process ("pre_3K.nc")

# pre_hist.to_netcdf(output + "pre_historic_ensemblemean.nc")
# # pre_1_5K.to_netcdf(output + "pre_1_5K_ensemblemean.nc")
# # pre_2K.to_netcdf(output + "pre_2K_ensemblemean.nc")
# # pre_3K.to_netcdf(output + "pre_3K_ensemblemean.nc")

